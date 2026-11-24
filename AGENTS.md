# KumaDrone contributor guide

- Treat [V6.2](engineering/designs/v6.2/README.md) as the active bench prototype. Read its design notes and the [wiring and bench plan](engineering/designs/v6.2/WIRING_AND_BENCH.md) for the subsystem you are changing.
- Use the repo-local [kuma-engineering skill](.agents/skills/kuma-engineering/SKILL.md) for CAD, BOM, mass and stability work.
- Keep V5 input files at their established paths and preserve the V5 and V6.1 reference geometry. The [baseline index](engineering/baselines/v5/README.md) explains the split between reference inputs and historical material.
- Use x aft from the nose, y right and z up, in millimeters. Put part names, quantities and material changes in the active revision's mesh manifest. Keep the OpenSCAD dispatcher, export list, documentation and mass inputs aligned.
- Run `make check` for V6.2 after CAD or mass-input edits. Compare its `build/v6.2/` reports with the checked-in evidence and review changed meshes before refreshing them. Run `make validate` when changing historical validation or its inputs.
- Distinguish verified geometry, calculated values, estimates and tests that have yet to run. Report the solver configuration, mass assumptions and actual verification scope. Flight readiness depends on physical evidence.
- Use the [historical handoff](docs/history/v5-v6-handoff.md) for prior choices and procedures. Its commands and numerical results apply to the revisions it describes.
