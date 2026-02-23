ifneq (,$(wildcard .env))
  include .env
  export
endif

VAULT_CARDS ?= $(error Set VAULT_CARDS to your Obsidian All_Cards path)

# ------------------------------------------------------------
# Help
# ------------------------------------------------------------
.PHONY: help
help:
	@printf "\nAvailable targets:\n\n"
	@printf "  make setup       - Symlink cards/, install git hook and cron job\n"
	@printf "  make sync        - Commit and push any changes\n"
	@printf "\n  make suggest     - Review uncommitted card changes with AI\n"
	@printf "       SINCE=HEAD~1   Review last commit instead\n"
	@printf "       DIR=path       Limit to a specific subdirectory\n"
	@printf "\n  make suggest-all - Review all cards, chunked by subfolder\n"
	@printf "       DIR=path       Limit to a specific subdirectory\n"
	@printf "\n  For dry runs (no LLM calls):\n"
	@printf "       uv run scripts/suggest.py diff --dry\n"
	@printf "       uv run scripts/suggest.py all --dry\n\n"

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------
.PHONY: setup
setup: link install-hooks install-cron

.PHONY: link
link:
	rm -rf cards
	ln -s "$(VAULT_CARDS)" cards
	@echo "Linked cards -> $(VAULT_CARDS)"

.PHONY: install-hooks
install-hooks:
	cp hooks/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Installed pre-commit hook"

.PHONY: install-cron
install-cron:
	(crontab -l 2>/dev/null | grep -qF "flashcards sync") || \
	(crontab -l 2>/dev/null; echo "0 21 * * * make -C $(CURDIR) sync") | crontab -
	@echo "Cron job installed"

# ------------------------------------------------------------
# Sync
# ------------------------------------------------------------
.PHONY: sync
sync:
	git add -A
	git diff --cached --quiet || git commit -m "sync $$(date +%F)"
	git push

# ------------------------------------------------------------
# AI suggestions
# ------------------------------------------------------------
.PHONY: suggest
suggest:
	uv run scripts/suggest.py diff $(if $(SINCE),--since=$(SINCE),) $(if $(DIR),--dir=$(DIR),)

.PHONY: suggest-all
suggest-all:
	uv run scripts/suggest.py all $(if $(DIR),--dir=$(DIR),)

