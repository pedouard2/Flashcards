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

.PHONY: setup
setup: link install-hooks
