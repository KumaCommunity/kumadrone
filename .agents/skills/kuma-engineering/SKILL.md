---
name: kuma-engineering
description: Work on the KumaDrone recreational RC aircraft repository. Use for revision selection, OpenSCAD or STL changes, fit checks, mass and balance, VSPAERO, parts sourcing, BOM updates, and bench-readiness handoffs.
---

# KumaDrone engineering workflow

1. Read the repository's `AGENTS.md` and confirm the revision. Default to `engineering/designs/v6.2/` unless the user names another version. Read only the relevant design notes, wiring plan or recorded data.
2. Establish which inputs govern the request. Check CAD modules and export names for fit, the BOM and installed hardware stations for component changes, and the solver template and geometry tags for aerodynamic claims.
3. For CAD and mass-input edits, run `make check` from the repo root. Compare `build/v6.2/data/` with the active revision's saved results. Look for changes in single-solid status, mesh dimensions, interfaces, mass and CG. Exercise affected fit probes and add a focused probe when the existing checks miss the interface.
4. For stability changes, run `make aero` and inspect the fresh case logs and geometry tags. Record the model configuration, measured or estimated CG, and the limits of the simulated envelope before interpreting derivatives.
5. For a BOM substitution, check the manufacturer's dimensions, ratings, mounting and connector data. Update installation notes and mass stations when the candidate affects them. Keep measured and estimated masses distinguishable.
6. Update revision notes and evidence together after an intentional geometry change. Report the specific checks run, assumptions made and unresolved bench items. Describe mechanical clearance in CAD separately from physical assembly and flight evidence.
