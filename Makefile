VAULT_CARDS ?= $(error Set VAULT_CARDS to your Obsidian All_Cards path)

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

.PHONY: sync
sync:
	git add -A
	git diff --cached --quiet || git commit -m "sync $$(date +%F)"
	git push

.PHONY: install-cron
install-cron:
	(crontab -l 2>/dev/null | grep -qF "flashcards sync") || \
	(crontab -l 2>/dev/null; echo "0 21 * * * make -C $(CURDIR) sync") | crontab -
	@echo "Cron job installed"

.PHONY: setup
setup: link install-hooks install-cron
