#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["litellm"]
# ///
"""
AI-powered flashcard review.

Usage:
  python scripts/suggest.py diff [--since=HASH] [--dir=PATH]
  python scripts/suggest.py all [--dir=PATH]

Environment:
  SUGGEST_MODEL   LiteLLM model string (default: claude-sonnet-4-6)
  ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY / etc.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

try:
    import litellm
except ImportError:
    print("litellm not installed. Run: pip install litellm")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
CARDS_DIR = REPO_ROOT / "cards"
VAULT_DIR = Path(os.path.realpath(CARDS_DIR)).parent
SUGGESTIONS_FILE = VAULT_DIR / "Suggestions.md"
RULES_FILE = VAULT_DIR / "Flashcard Rules.md"
MODEL = os.environ.get("SUGGEST_MODEL", "claude-sonnet-4-6")

SYSTEM_PROMPT = """You are a spaced repetition expert reviewing Anki flashcards.

Suggest improvements based on these principles:
- Atomic: each card tests exactly one thing
- Two-way: if term→definition exists, also write definition→term
- One blank per cloze card
- Split answers that list multiple facts into separate cards
- Groups/sequences need a list card separate from individual definition cards
- Pair important cloze cards with a Q&A version

For each suggestion: show the original card, briefly explain the issue, then show the improved version(s).
Be concise and specific. Skip cards that are already well-written."""


def get_rules() -> str:
    if RULES_FILE.exists():
        return RULES_FILE.read_text(encoding="utf-8")
    return ""


def changed_files(since: str | None) -> list:
    cmd = ["git", "diff", "--name-only", since or "HEAD"]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
    files = []
    for line in result.stdout.splitlines():
        p = REPO_ROOT / line
        if p.suffix == ".md" and "cards" in p.parts and p.exists():
            files.append(p)
    return files


def group_by_subfolder(base: Path) -> dict:
    groups = {}
    for md in sorted(base.rglob("*.md")):
        key = str(md.parent.relative_to(base))
        groups.setdefault(key, []).append(md)
    return groups


def call_llm(deck_name: str, content: str, rules: str) -> str:
    prompt = f"""Review the following flashcard deck and suggest improvements.

## Rules Reference
{rules}

## Deck: {deck_name}

{content}"""
    response = litellm.completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM_PROMPT,
    )
    return response.choices[0].message.content


def append_suggestions(entries: list) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# Review — {timestamp}\n"]
    for deck_name, suggestion in entries:
        lines.append(f"## {deck_name}\n\n{suggestion}\n")
    lines.append("---\n")

    with open(SUGGESTIONS_FILE, "a", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Written to {SUGGESTIONS_FILE}")


def run_diff(since: str | None, dir_filter: str | None) -> None:
    files = changed_files(since)
    if dir_filter:
        files = [f for f in files if dir_filter in str(f)]
    if not files:
        print("No changed card files found.")
        return

    rules = get_rules()
    entries = []
    for f in files:
        print(f"Reviewing {f.name}...")
        suggestion = call_llm(f.stem, f.read_text(encoding="utf-8"), rules)
        entries.append((str(f.relative_to(REPO_ROOT)), suggestion))

    append_suggestions(entries)


def run_all(dir_filter: str | None) -> None:
    base = Path(dir_filter) if dir_filter else CARDS_DIR
    groups = group_by_subfolder(base)
    if not groups:
        print("No card files found.")
        return

    rules = get_rules()
    entries = []
    for subfolder, files in sorted(groups.items()):
        print(f"Reviewing {subfolder}...")
        content = "\n\n---\n\n".join(
            f"### {f.stem}\n{f.read_text(encoding='utf-8')}" for f in files
        )
        suggestion = call_llm(subfolder, content, rules)
        entries.append((subfolder, suggestion))

    append_suggestions(entries)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["diff", "all"])
    parser.add_argument("--since", help="Git ref to diff from, e.g. HEAD~1 (diff mode only)")
    parser.add_argument("--dir", help="Limit to a specific directory")
    args = parser.parse_args()

    if args.mode == "diff":
        run_diff(args.since, args.dir)
    else:
        run_all(args.dir)


if __name__ == "__main__":
    main()
