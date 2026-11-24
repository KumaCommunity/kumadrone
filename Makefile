# Kuma FPV pipeline convenience wrapper. Uses inline recipes (no tabs needed).
# Usage: make [all|validate|calcs|export|render|vspaero|clean]
SHELL := /bin/bash
.PHONY: all validate calcs export render vspaero clean help
help: ; @echo "make all|validate|calcs|export|render|vspaero|clean"
all: ; @bash run_all.sh all
validate: ; @bash run_all.sh validate
calcs: ; @bash run_all.sh calcs
export: ; @bash run_all.sh export
render: ; @bash run_all.sh render
vspaero: ; @bash run_all.sh vspaero
clean: ; @find . -name __pycache__ -prune -exec rm -rf {} + ; @rm -rf build
