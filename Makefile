# ------------------------------------------------------------
# Project‑wide Makefile
# ------------------------------------------------------------
# Adjust these if you use different names
# default collection
CARDS_DIR        := cards
# submodule with the Hashcards source
EXTERNALS_DIR    := external/hashcards
BIN_DIR          := $(EXTERNALS_DIR)/target/release
HASHCARDS_BIN    := $(BIN_DIR)/hashcards

# ------------------------------------------------------------
# Top‑level convenience targets
# ------------------------------------------------------------
.PHONY: all
all: help                                 # default target shows help

.PHONY: help
help:
	@printf "\nAvailable make targets:\n\n"
	@printf "  make update-hashcards   - Build (or rebuild) the hashcards binary\n"
	@printf "  make update-externals   - Pull latest upstream for the submodule\n"
	@printf "  make drill DIRS=\"dir1 dir2 …\" [extra‑options]\n"
	@printf "       - Start a drill session on one or more collections.\n"
	@printf "         If DIRS is omitted the default $(CARDS_DIR) is used.\n"
	@printf "  make stats DIRS=\"...\"   - Collection statistics (JSON)\n"
	@printf "  make check DIRS=\"...\"   - Verify integrity\n"
	@printf "  make orphans-list DIRS=\"...\"\n"
	@printf "  make orphans-delete DIRS=\"...\"\n"
	@printf "  make export DIRS=\"...\"   - Export to JSON (stdout)\n"
	@printf "\nYou can pass any Hashcards flag after the target, e.g.:\n"
	@printf "  make drill DIRS=\"cards/python cards/rust\" --card-limit=20\n\n"

# ------------------------------------------------------------
# Build / update the hashcards binary
# ------------------------------------------------------------
.PHONY: update-hashcards
update-hashcards: $(HASHCARDS_BIN)

$(HASHCARDS_BIN):
	@echo "▶ Building hashcards binary …"
	@cd $(EXTERNALS_DIR) && $(MAKE)          # runs the Makefile shipped with hashcards
	@echo "✅ Built $(HASHCARDS_BIN)"

# ------------------------------------------------------------
# Update the external submodule(s)
# ------------------------------------------------------------
.PHONY: update-externals
update-externals:
	@echo "▶ Updating submodule(s)…"
	@git submodule update --remote $(EXTERNALS_DIR)
	@git add $(EXTERNALS_DIR)
	@git commit -m "chore: sync hashcards submodule to latest upstream" || true
	@echo "✅ Submodule updated and pointer committed (if changed)"

# ------------------------------------------------------------
# Helper variables / functions
# ------------------------------------------------------------
# If the caller does not supply DIRS, fall back to the default collection.
DIRS ?= $(CARDS_DIR)

# Turn a space‑separated list into a series of arguments for the CLI.
# Example: DIRS="a b c" → "a b c"
# (We simply expand the variable; the shell will split on spaces.)
HASHCARDS_ARGS = $(filter-out $@,$(MAKECMDGOALS))

# Generic runner - used by the specific commands below.
# $(1) = sub‑command (drill, stats, …)
define RUN_HASHCARDS
	@$(HASHCARDS_BIN) $(1) $(DIRS) $(HASHCARDS_ARGS)
endef

# ------------------------------------------------------------
# Wrapper targets for the hashcards CLI
# ------------------------------------------------------------
.PHONY: drill
drill:
	$(call RUN_HASHCARDS,drill)

.PHONY: stats
stats:
	$(call RUN_HASHCARDS,stats --format=json)

.PHONY: check
check:
	$(call RUN_HASHCARDS,check)

.PHONY: orphans-list
orphans-list:
	$(call RUN_HASHCARDS,orphans list)

.PHONY: orphans-delete
orphans-delete:
	$(call RUN_HASHCARDS,orphans delete)

.PHONY: export
export:
	$(call RUN_HASHCARDS,export)

# ------------------------------------------------------------
# Clean up build artefacts (optional)
# ------------------------------------------------------------
.PHONY: clean
clean:
	@echo "▶ Cleaning hashcards build artefacts…"
	@cd $(EXTERNALS_DIR) && $(MAKE) clean
	@echo "✅ Clean complete"

# ------------------------------------------------------------
# End of Makefile
# ------------------------------------------------------------