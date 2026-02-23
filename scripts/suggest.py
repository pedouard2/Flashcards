#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["litellm", "pydantic"]
# ///
"""
AI-powered flashcard review.

Usage:
  uv run scripts/suggest.py diff [--since=HASH] [--dir=PATH] [--dry]
  uv run scripts/suggest.py all [--dir=PATH] [--dry]

Environment:
  SUGGEST_MODEL   LiteLLM model string (default: claude-sonnet-4-6)
  ANTHROPIC_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY / etc.
"""

import os
import json
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel
from typing import Literal

import litellm
litellm.drop_params = True

REPO_ROOT = Path(__file__).parent.parent
CARDS_DIR = REPO_ROOT / "cards"
VAULT_DIR = Path(os.path.realpath(CARDS_DIR)).parent
SUGGESTIONS_FILE = VAULT_DIR / "Suggestions.md"
RULES_FILE = VAULT_DIR / "Flashcard Rules.md"
MODEL = os.environ.get("SUGGEST_MODEL", "gpt-5-mini")

IssueType = Literal[
    "multi_blank_cloze",    # cloze card has multiple independent blanks
    "bundled_answer",       # Q&A answer contains multiple independent facts
    "missing_reverse",      # term→definition exists but not definition→term
    "missing_list_card",    # individual definition cards exist but no overview list card
    "missing_qa_for_cloze", # important cloze has no Q&A counterpart
]


class Suggestion(BaseModel):
    original: str
    issue_type: IssueType
    explanation: str
    improved: list[str]


class DeckReview(BaseModel):
    suggestions: list[Suggestion]


SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "system.txt").read_text(encoding="utf-8")


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


def call_llm(deck_name: str, content: str) -> DeckReview:
    prompt = f"Review this flashcard deck and return only the JSON object.\n\n## Deck: {deck_name}\n\n{content}"
    response = litellm.completion(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return DeckReview.model_validate_json(response.choices[0].message.content)


def flush_suggestion(deck_name: str, review: DeckReview, first: bool) -> None:
    if not review.suggestions:
        print(f"  No issues found.")
        return

    with open(SUGGESTIONS_FILE, "a", encoding="utf-8") as f:
        if first:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write(f"# Review — {timestamp}\n\n")

        f.write(f"## {deck_name}\n\n")
        for s in review.suggestions:
            f.write(f"**Issue:** `{s.issue_type}`  \n")
            f.write(f"**Original:**\n```\n{s.original}\n```\n")
            f.write(f"**Why:** {s.explanation}  \n")
            f.write(f"**Improved:**\n")
            for card in s.improved:
                f.write(f"```\n{card}\n```\n")
            f.write("\n---\n\n")

    print(f"  {len(review.suggestions)} suggestion(s) written.")


def run_diff(since: str | None, dir_filter: str | None, dry: bool) -> None:
    files = changed_files(since)
    if dir_filter:
        files = [f for f in files if dir_filter in str(f)]
    if not files:
        print("No changed card files found.")
        return

    if dry:
        print("Files that would be reviewed:")
        for f in files:
            print(f"  {f.relative_to(REPO_ROOT)}")
        return

    for i, f in enumerate(files):
        print(f"Reviewing {f.name}...")
        review = call_llm(f.stem, f.read_text(encoding="utf-8"))
        flush_suggestion(str(f.relative_to(REPO_ROOT)), review, first=i == 0)

    print(f"Written to {SUGGESTIONS_FILE}")


def run_all(dir_filter: str | None, dry: bool) -> None:
    base = Path(dir_filter) if dir_filter else CARDS_DIR
    groups = group_by_subfolder(base)
    if not groups:
        print("No card files found.")
        return

    if dry:
        print("Subfolders that would be reviewed:")
        for subfolder, files in sorted(groups.items()):
            print(f"  {subfolder}/")
            for f in files:
                print(f"    {f.name}")
        return

    for i, (subfolder, files) in enumerate(sorted(groups.items())):
        print(f"Reviewing {subfolder}...")
        content = "\n\n---\n\n".join(
            f"### {f.stem}\n{f.read_text(encoding='utf-8')}" for f in files
        )
        review = call_llm(subfolder, content)
        flush_suggestion(subfolder, review, first=i == 0)

    print(f"Written to {SUGGESTIONS_FILE}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["diff", "all"])
    parser.add_argument("--since", help="Git ref to diff from, e.g. HEAD~1 (diff mode only)")
    parser.add_argument("--dir", help="Limit to a specific directory")
    parser.add_argument("--dry", action="store_true", help="List what would be reviewed without calling the LLM")
    args = parser.parse_args()

    if args.mode == "diff":
        run_diff(args.since, args.dir, args.dry)
    else:
        run_all(args.dir, args.dry)


if __name__ == "__main__":
    main()
