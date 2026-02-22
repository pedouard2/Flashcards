# Flashcards

Personal flashcard collection written in Obsidian, automatically synced to this repo daily.

## Setup

Set `VAULT_CARDS` to the folder containing your card decks, then run:

```bash
export VAULT_CARDS=/path/to/your/obsidian/cards
make setup
```

This creates a symlink from `cards/` to your vault, installs the pre-commit hook, and registers the daily cron job.

## Auto-sync

A cron job commits and pushes any changes daily at 9pm, installed automatically by `make setup`. Only runs a commit if there are actual changes.

## Card Format

Two card types are supported.

**Q&A:**
```
Q: Question
A: Answer
```

**Cloze** (blanks in `{...}`):
```
C: The {term} is defined as {its definition}.
```

Both support multi-line content and LaTeX math (`$...$` inline, `$$...$$` display).

## Pre-commit Hook

Collapses multiple consecutive blank lines between cards into one. Installed automatically by `make setup`.

## AI Suggestions

Requires [uv](https://docs.astral.sh/uv/) and an API key for your chosen model.

```bash
export SUGGEST_MODEL=claude-sonnet-4-6   # or gpt-4o, gemini/gemini-2.0-flash, etc.
export ANTHROPIC_API_KEY=...             # or OPENAI_API_KEY, GEMINI_API_KEY, etc.
```

Review uncommitted changes:
```bash
make suggest
make suggest SINCE=HEAD~1               # last commit
make suggest DIR=cards/technical/ai-engineering
```

Review everything, chunked by subfolder:
```bash
make suggest-all
make suggest-all DIR=cards/technical/az-204
```

Suggestions are appended to `Suggestions.md` in your vault with a timestamp header each run.
