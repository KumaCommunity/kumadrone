# KumaDrone

```text
██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗███████╗
██║ ██╔╝██║   ██║████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗████╗  ██║██╔════╝
█████╔╝ ██║   ██║██╔████╔██║███████║██║  ██║██████╔╝██║   ██║██╔██╗ ██║█████╗
██╔═██╗ ██║   ██║██║╚██╔╝██║██╔══██║██║  ██║██╔══██╗██║   ██║██║╚██╗██║██╔══╝
██║  ██╗╚██████╔╝██║ ╚═╝ ██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║ ╚████║███████╗
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
```

KumaDrone is a 3D-printed recreational RC airplane with a 1.30 m fixed wing, a V-tail and a rear pusher propeller. It's being developed as a line-of-sight bench prototype with optional FPV equipment.

**Current revision: V6.2.** The recorded CAD run produced 51 watertight single-solid parts and passed 18 fit checks. The prototype still needs physical fit, structural testing, measured balance, control and propulsion checks before a maiden flight.

## Start here

| If you want to… | Open |
| --- | --- |
| See what changed and how the parts fit | [V6.2 design notes](engineering/designs/v6.2/README.md) |
| Open the model in OpenSCAD | [V6.2 source](engineering/designs/v6.2/Kuma_FPV_V6_2_Configuration_B.scad) |
| Find the meshes and material assignments | [STLs](engineering/designs/v6.2/STL/) and [mesh report](engineering/designs/v6.2/data/mesh_verification.csv) |
| Start a parts list or wire up a bench setup | [Starting BOM](engineering/designs/v6.2/reference/starting_bom.csv) and [wiring and bench plan](engineering/designs/v6.2/WIRING_AND_BENCH.md) |
| Inspect the engineering results | [CAD checks](engineering/designs/v6.2/data/fit_verification.csv), [mass and balance](engineering/designs/v6.2/data/mass_balance.csv) and [aero screen](engineering/designs/v6.2/data/vspaero_screen.csv) |

For a first fit article, print the insert coupon, one collar pair, one servo plate and a representative hinge station before committing to the full airframe. The mesh report identifies the aluminum reference parts and their quantities.

## Run the checks

Create a Python environment and install the dependencies. Install OpenSCAD with the Manifold backend for CAD checks. OpenVSP is only needed for the aerodynamic screen.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
make check
```

`make check` writes fresh meshes, fit results and mass calculations to `build/v6.2/`. On Apple Silicon, if the native OpenSCAD build fails with a Qt or NEON error, run the Intel binary through Rosetta if installed:

```sh
make check V62_OPENSCAD='/usr/bin/arch -x86_64 /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'
```

Use `make aero` to run the V6.2 OpenVSP screen. Override `V62_VSPSCRIPT` with your executable path when needed. Solver outputs go to a fresh directory under `build/`. Use `make validate` for the original V5/V6.1 regression suite or `make help` for the complete command list.

## Repository guide

- [Current design](engineering/designs/v6.2/) contains CAD, print meshes, bench instructions and reproducible evidence.
- [Earlier V6 design](engineering/designs/v6/) and [V5 baseline](engineering/baselines/v5/) document prior revisions.
- [V5 audit](engineering/audits/v5-configuration-b/) contains the independent engineering review.
- [Contributor guide](AGENTS.md) explains change and verification conventions. The [original handoff](docs/history/v5-v6-handoff.md) records the earlier workflow and decisions.
