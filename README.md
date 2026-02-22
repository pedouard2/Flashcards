# Flashcards

Personal flashcard collection written in Obsidian, automatically synced to this repo daily.

## Setup

Set `VAULT_CARDS` to the folder containing your card decks, then run:

```bash
export VAULT_CARDS=/path/to/your/obsidian/All_Cards
make setup
```

This creates a symlink from `cards/` to your vault and installs the pre-commit hook.

## Auto-sync

A cron job commits and pushes any changes daily at 9pm, installed automatically by `make setup`. Only runs a commit if there are actual changes.

## Card Format

Two card types are supported.

**Q&A:**
```
Q: Question
A: Answer
```

**Cloze** (blanks in `[...]`):
```
C: The [term] is defined as [its definition].
```

Both support multi-line content and LaTeX math (`$...$` inline, `$$...$$` display).

## Pre-commit Hook

Collapses multiple consecutive blank lines between cards into one. Runs automatically on commit after `make install-hooks`.
