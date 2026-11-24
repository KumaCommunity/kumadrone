# KumaDrone checks and historical pipeline targets.
SHELL := /bin/bash
PYTHON ?= python3
V62_OPENSCAD ?= openscad
V62_VSPSCRIPT ?= /Applications/OpenVSP.app/Contents/Resources/vspscript
V62_DIR := engineering/designs/v6.2
V62_BUILD := build/v6.2

.PHONY: all check aero validate calcs export render vspaero clean help
help:
	@echo "V6.2: make check | make aero"
	@echo "Historical: make validate | all | calcs | export | render | vspaero"
	@echo "Cleanup: make clean"

check:
	$(PYTHON) $(V62_DIR)/scripts/validate.py --openscad "$(V62_OPENSCAD)" --output "$(V62_BUILD)"
	$(PYTHON) $(V62_DIR)/scripts/mass_balance.py --data "$(V62_BUILD)/data"

aero:
	@mkdir -p build
	@run_dir=$$(mktemp -d build/v62-aero.XXXXXX) && \
	  $(PYTHON) $(V62_DIR)/openvsp/run_panel.py --vspscript "$(V62_VSPSCRIPT)" --out "$$run_dir"
all: ; @bash run_all.sh all
validate: ; @bash run_all.sh validate
calcs: ; @bash run_all.sh calcs
export: ; @bash run_all.sh export
render: ; @bash run_all.sh render
vspaero: ; @bash run_all.sh vspaero
clean: ; @find . -name __pycache__ -prune -exec rm -rf {} + ; @rm -rf build
