# AGENTS.md — Kuma FPV V5 → V6 project handoff

**Purpose of this file:** let another agent (or human) pick up this project, reproduce
every result, and **validate** prior work without re-deriving it. It is the authoritative
"how it is organised, how to run it, what is true, and what is still unknown" document.

> **Golden rule:** treat every number as *provisional* unless this file or a generated CSV
> labels it verified. Never upgrade an assumption to a fact. Never report a simulation,
> test, or measurement that was not actually run. The V5 source files are **read-only**.

---

## V6.2 bench prototype — 2026-11-23

The current bench-design handoff is [engineering/designs/v6.2/README.md](engineering/designs/v6.2/README.md).
Use that directory's CAD, part meshes, validation runner, BOM and wiring plan for V6.2.
It introduces split collars and bored spar sockets, serviceable ruddervators, a forward battery hatch with a strap tray, working cooling openings, and a raised motor pylon and firewall.
The V6.2 validator reports fresh CAD evidence. The root Makefile and prior checks cover V5/V6.1; section numbers and historical results below retain that meaning.
V6.2 remains a bench prototype pending physical fit, structural, control, propulsion and flight gates.

## 1. What this project is
A **civilian, recreational, hand-launched, FPV, fixed-wing RC airplane** (3D-printed).
Version **V5 Configuration B** was supplied as a CAD/engineering package; an independent
**audit** was performed and a revised **V6** design was produced. Not flight-certified; this
is an engineering/concept exercise. No launcher, payload release, or military function.

Nameplate: high-mounted fixed wing, **no ailerons**, **upright V-tail (2 ruddervators)**,
**rear pusher**, forward-facing nose FPV camera, modular/removable, LW-PLA shell + PETG
hardpoints, M3/M4 inserts, optional secured equipment (≤500 g *to evaluate*).

## 2. Golden rules for agents (read before touching anything)
1. **Do not modify the V5 originals** at the repo root (`*.scad`, `*.csv`, `*.dxf`,
   `STL/`, `CAD_Views/`, `README.md`). They are the reference baseline. Work in `engineering/`.
2. **Never fabricate** test results, measured masses, material strengths, or tool outputs.
   If a tool isn't available, say so and do only what is possible.
3. **Label provenance** for every number: `verified · calculated · estimated · unverified · not-run`.
4. **Don't move files the scripts depend on.** Many scripts resolve `ROOT` via `../../..`
   and read root CSVs (`mass_budget.csv`, `geometry_mass_screen.csv`, `STL/`). Keep them.
5. **Re-run the validation suite** (`engineering/tools/run_validation.py`) after changes;
   update expected values only when a change is intentional and documented.
6. Prefer **one change + re-measure** over bulk edits. Several parts are structural; mass
   and CG are sensitive.

## 3. Repository map (organised)
```
<root>/
├─ AGENTS.md                     ← THIS handoff doc
├─ README.md                     ← original V5 package readme (read-only)
├─ Kuma_FPV_V5_Configuration_B.scad        (V5 original, read-only)
├─ Kuma_FPV_V5_Configuration_B_Engineering_Review.md (V5, read-only)
├─ Kuma_FPV_V5_Configuration_B_OpenVSP.vspscript       (V5, read-only)
├─ NACA_2412_Wing_Root_200mm.dxf / NACA_0010_Tail_Root_190mm.dxf
├─ mass_budget.csv geometry_mass_screen.csv hardware_schedule.csv
│  loading_scenarios.csv lift_screen.csv sensitivity.csv metrics.json   (V5, read-only)
├─ STL/ (32 V5 meshes) · CAD_Views/ (6 PNG) · *.png (V5 posters)        (read-only)
└─ engineering/
   ├─ audits/v5-configuration-b/     ← CANONICAL V5 audit (the reference review)
   │  ├─ AUDIT_SUMMARY.md FULL_ENGINEERING_AUDIT.md DESIGN_ISSUES.md
   │  ├─ RECOMMENDED_CHANGES.md REQUIREMENTS_TRACEABILITY.md
   │  ├─ CALCULATION_VERIFICATION.md STRUCTURAL_REVIEW.md MANUFACTURING_REVIEW.md
   │  ├─ HARDWARE_REVIEW.md ELECTRICAL_REVIEW.md
   │  ├─ ASSUMPTIONS_REGISTER.csv GEOMETRY_VERIFICATION.csv
   │  ├─ MASS_AND_BALANCE.csv MASS_RANGE.csv AERODYNAMIC_SCREENING.csv
   │  ├─ scripts/ (8 *.py) · data/ (CSV/JSON) · graphics/ (4 PNG) · openvsp/
   ├─ designs/v6/                    ← CANONICAL V6 design
   │  ├─ Kuma_FPV_V6_Configuration_B.scad   (compiles; 43 parts)
   │  ├─ V6_SUMMARY.md DESIGN_CHANGES.md
   │  ├─ STL/ (43 meshes) · graphics/ (ortho + iso + exploded + poster + dark renders)
   │  ├─ data/ (v6_*.csv, mass_range) · data/vspaero/ (polars, results, panel/tail study)
   │  ├─ scripts/ (v6_calcs, verify_v6_stl, v6_mass_range, plot_ortho, render_dark, make_poster)
   │  └─ openvsp/ (vspscripts + vsp_study.py + run_vspaero_v6.py)
   ├─ tools/run_validation.py       ← ONE-COMMAND VALIDATION (see §7)
   └─ _archive/                     ← superseded duplicate audit (do not use)
```
The two **canonical** trees are `engineering/audits/v5-configuration-b/` and

## 4. Environment & prerequisites
- **OS:** macOS (Apple silicon). **Python:** 3.15 (`/opt/homebrew/bin/python3`).
- **Python packages** (installed): numpy 2.5.5, matplotlib 3.11.2, trimesh 5.2.2,
  networkx 3.7, Pillow 13.0.0. Fresh install (PEP‑668 blocks system pip):
  ```
  python3 -m pip install --break-system-packages numpy matplotlib trimesh networkx pillow
  ```
- **OpenSCAD:** `/opt/homebrew/bin/openscad` (**2026.10.11**). Export a single part:
  ```
  openscad -D 'part="wing_R1"' -o out.stl engineering/designs/v6/Kuma_FPV_V6_Configuration_B.scad
  ```
  Use **single quotes** around `-D 'part="..."'`. `part` defaults to `assembly` and is
  CLI‑overridable in the V6 SCAD (`part = is_undef(part) ? "assembly" : part;`).
- **OpenVSP:** `/Applications/OpenVSP.app` (v7.2.2). Two ways to script it:
  - **Headless (WORKS):** the `vspscript` CLI.
    ```
    R=/Applications/OpenVSP.app/Contents/Resources
    ( cd /tmp/vsp_run && $R/vspscript -script /ABS/PATH/to/Kuma_V6_vspaero_run.vspscript )
    ```
    Outputs (`.polar`, `.vsp3`, `.lod`, …) land in the **current directory**.
  - **Python API (DO NOT use for geometry):** setting
    `PYTHONPATH=$R/python/openvsp:$R/python/degen_geom:$R/python/utilities` makes
    `import openvsp` work, but **`AddGeom` segfaults (exit 139)** headless. Use the
    `vspscript` CLI instead. `run_vspaero_v6.py` is kept only as a template.

## 5. Reproduce everything (order matters)
```bash
# 0) sanity / validate prior work (no OpenSCAD/OpenVSP needed)
python3 engineering/tools/run_validation.py

# 1) V5 audit numbers + figures
python3 engineering/audits/v5-configuration-b/scripts/verify_stl.py
python3 engineering/audits/v5-configuration-b/scripts/verify_airfoil.py
python3 engineering/audits/v5-configuration-b/scripts/audit_calcs.py
python3 engineering/audits/v5-configuration-b/scripts/launch_lateral.py
python3 engineering/audits/v5-configuration-b/scripts/structural_screen.py
python3 engineering/audits/v5-configuration-b/scripts/plot_graphics.py

# 2) V6 mass / CG / stability / envelope
python3 engineering/designs/v6/scripts/v6_calcs.py
python3 engineering/designs/v6/scripts/v6_mass_range.py

# 3) Export V6 STLs (OpenSCAD) then measure real volumes/mass
SCAD=engineering/designs/v6/Kuma_FPV_V6_Configuration_B.scad
for p in fuselage_0 fuselage_1 fuselage_2 fuselage_3 fuselage_4 fuselage_5 \
         coupler_0 coupler_1 coupler_2 coupler_3 coupler_4 wing_center \
         wing_R1 wing_R2 wing_R3 wing_L1 wing_L2 wing_L3 wing_key tail_R tail_L \
         ruddervator_R ruddervator_L tail_saddle tail_shoe_R tail_shoe_L saddle_plate \
         camera_plate camera_cradle dorsal_fairing battery_tray forward_equipment_tray \
         secured_tray battery_hatch_lid motor_bulkhead wing_saddle_clamp \
         centre_spar_joiner wing_center_spar_sleeve control_horn_R control_horn_L \
         ruddervator_hinge_R ruddervator_hinge_L insert_fit_coupon; do
  openscad -D "part=\"$p\"" -o engineering/designs/v6/STL/$p.stl $SCAD; done
python3 engineering/designs/v6/scripts/verify_v6_stl.py

# 4) VSPAERO (headless via vspscript). One config per command (each ~25 s).
R=/Applications/OpenVSP.app/Contents/Resources
S=/ABS/PROJECT/engineering/designs/v6/openvsp        # <-- set to your absolute path
mkdir -p /tmp/vsp_a && ( cd /tmp/vsp_a && $R/vspscript -script "$S/Kuma_V6_vspaero_run.vspscript" )
mkdir -p /tmp/vsp_b && ( cd /tmp/vsp_b && $R/vspscript -script "$S/Kuma_V6_vspaero_beta.vspscript" )
python3 engineering/audits/v5-configuration-b/scripts/parse_vspaero.py /tmp/vsp_a/V6_run.polar 0.560
# panel tail study (one config per invocation): python3 "$S/vsp_study.py" base 0.270 45 0.200 0.150

# 5) Renders + poster (no GUI)
python3 engineering/designs/v6/scripts/plot_ortho.py top   # also side/front/rear
python3 engineering/designs/v6/scripts/render_dark.py      # hero/iso/exploded (silver)
python3 engineering/designs/v6/scripts/make_poster.py      # graphics/v6_poster.png
```
> Some sandboxes cap a single shell command at ~30 s. **Run VSPAERO and the multi‑render
> steps separately** if so; `vsp_study.py` does one tail config (~25 s) per invocation.


## 6. Test / validation suite
**One command:** `python3 engineering/tools/run_validation.py` → prints a PASS/FAIL table,
exits `0` if all pass. It needs only numpy/trimesh and the **already‑generated** STLs and
saved polars (does **not** invoke OpenSCAD/OpenVSP). Current result: **13/13 PASS**.

| # | Check | Expected | Notes |
|---|-------|----------|-------|
| 1 | wing area | 0.2275 m² | from `audit_calcs.wing_geometry()` |
| 2 | aspect ratio | 7.43 | |
| 3 | MAC | 176.19 mm | |
| 4 | NACA 2412 t/c | 12.0 % | DXF vs analytic |
| 5 | NACA 0010 t/c | 10.0 % | |
| 6 | V6.1 tail Vv | 0.051 | span 300 @47 |
| 7 | V6.1 tail Vh | 0.330 | |
| 8 | VSPAERO panel x_np | 557 mm | `V6.1_alpha.polar` |
| 9 | V6.1 empty mass | 1366.2 g, 0 over‑bed | STL volumes × assumed density |
| 10 | V5 32 STLs watertight | 32/32 | trimesh |
| 11–12 | V5 & V6 SCAD delimiters balanced | true | crude syntax guard |
| 13 | V6 STL count | 44 | exported parts |

**What it does NOT cover (must be checked separately):** re‑compiling SCAD from scratch,
print/fit/interference, material strength, thrust, flight, or re‑running VSPAERO (it reads
the saved polar). Per‑area scripts (run individually) provide deeper checks:
`verify_stl`, `verify_airfoil`, `audit_calcs`, `launch_lateral`, `structural_screen`,
`v6_calcs`, `v6_mass_range`, `verify_v6_stl`, `parse_vspaero`, `vsp_study`.

**If you change a number intentionally:** update the expected value inside
`run_validation.py` **and** add a row to the Change Log (§13). Do not loosen a tolerance to
make a check pass without documenting why.

## 7. Established results (with provenance)
Provenance: **V**=verified (independently recomputed), **C**=calculated, **E**=estimated
(assumption‑dependent), **U**=unverified, **X**=not run.

| Quantity | Value | Prov. | Where / note |
|---|---|---|---|
| Wing span / area / AR | 1300 mm / 0.2275 m² / 7.43 | V | CAD + recompute |
| Root/tip chord, taper | 200/150 mm, 0.75 | V | |
| MAC / MAC‑LE / wing AC(25%) | 176.19 / 507.4 / 551.5 mm | V/C | |
| LE sweep / dihedral / incidence | 2.11° / 7° / 0° | V/C | no twist |
| Airfoils | NACA 2412 (12%,2%), NACA 0010 (10%) | V | DXF vs analytic |
| V5 tail area / Vh / Vv | 0.0792 m² / 0.31 / 0.030 | V | |
| V6.1 tail (span 300, 200/150, 47°) Vh / Vv | 0.330 / 0.051 | V | `v6_calcs` |
| V6 empty mass | **1351.8 g** | V(vols)+E(density) | STL × 0.35/1.27; LW 559.1, PETG 308.6, hw 16, purchased 477 |
| V6 empty CG | ~561.6 mm (30.7 % MAC) | E | battery at x=375 (moved from 410) |
| V6 mass envelope (density sweep) | empty 1099–1752 g; +500 g 1599–2252 g | E | `MASS_RANGE`/`v6_mass_range` |
| VLM (wing+tail, NO fuselage) SM / NP | +8.31 % / 574.6 mm | V | VSPAERO alpha |
| VLM Cnβ / Clβ | ~0.075 / ~0.21 per rad | V | VSPAERO beta |
| **Panel (incl. fuselage) SM / NP** | **−3.9 % / 553 mm** | V | **fuselage destabilises** |
| Panel Cnβ (V6 tail) | ~0 per rad | V | near‑neutral yaw |
| Tail study (panel) vv3 | SM +2.7 %, Cnβ 0.077 | V | bigger tail 0.33/47° |
| Stall empty / +500 g (CLmax 1.0) | 9.75 / 11.39 m/s | C | ↑/↓ with CLmax |
| Hand launch | empty feasible; +500 g demanding (not a conflict) | C | throw + T/W dependent |

> **The single most important caveat:** VLM (wing+tail) says stable (+8.3 %), but the
> **panel‑method run including the fuselage says marginal/unstable at CG 30.7 % MAC**.
> The fuselage Munk moment removes ≈12 % MAC of pitch margin and ≈0.07/rad of yaw. Any
> stability claim must include the fuselage. Recommended fix (from tail study): **bigger
> tail (~span 0.33, 220/170, ~47°) + CG forward to ~24–27 % MAC → SM ≈ +5.6 %**.


**V6.1 (current CAD/revision):** V-tail span 270→**300 mm** at **47°** (span capped so each
panel fits a 220 mm bed; TE stays ≤970 mm before the prop) + battery 375→**285 mm** ⇒ CG
≈**551 mm (25 % MAC)**. Panel (incl. fuselage) **NP 557 mm, SM ≈ +3 %** (was −3.9 % at
CG 560). **Yaw is still weak (Cnβ ≈ 0.014 /rad)** → next step is a small **ventral fin**.
Mass **1366.2 g** (incl. optional ventral fin +5.4 g); validation updated (13/13).
  **Optional removable ventral fin** added (yaw): a fin large enough to help will STRIKE on a
  belly landing, and the headless VSPAERO did **not** capture the added surface (polars
  identical) → validate in the OpenVSP GUI; the effective fix remains a larger/split V-tail.

## 8. Assumptions (top of the register)
Full register: `engineering/audits/v5-configuration-b/ASSUMPTIONS_REGISTER.csv` (A01–A27).

| ID | Assumption | Value (range) | Sens. | Validation |
|----|-----------|---------------|-------|------------|
| A01 | foaming LW‑PLA effective density | 0.35 (0.20–0.60) g/cm³ | **High** | weigh coupons |
| A03 | printed mass = CAD volume × density | — | High | slicer mass/part |
| A04 | battery mass/station | 185 g, x=375 (V5 410) | High | weigh + fit |
| A07 | CLmax | 1.0 (0.9–1.2) | **Critical** | low‑Re polar/flight |
| A09–12 | NP method (slopes, downwash, η) | nominal | High | VSPAERO (done), flight |
| A13/14 | CD0 / Oswald e | 0.038 / 0.85 | Med | glide test |
| A18 | LW‑PLA layer strength | unknown | High | coupons |
| A19 | M3/M4 insert pull‑out | unverified | High | insert coupon test |
| A20 | dihedral Clβ | 0.08–0.16 (VSPAERO ~0.21) | High | flight |
| A23 | load factor | +3/+4.5 g | High | structural test |
| A25 | main spar | 8 mm carbon (assumed) | High | specify + bond test |

## 9. Known issues & current status
Register: `engineering/audits/v5-configuration-b/DESIGN_ISSUES.md` (I‑01…I‑23).
"CAD added" = geometry exists, **not validated**.

| ID | Issue | V6 status |
|----|-------|-----------|
| I‑01 | wing↔fuselage load path | CAD added (clamp+straps); fit/pull test |
| I‑02 | centre spar joiner | CAD added |
| I‑03 | tail registration | CAD added |
| I‑05 | ruddervator mechanism | CAD added; **bench test needed** |
| I‑06 | rear‑only lateral | VSPAERO: Clβ strong, **Cnβ weak**; flight test |
| I‑07 | nose camera | CAD added (aperture + cradle) |
| I‑08 | service access | CAD added (hatch+flange, servo bays) |
| I‑09 | motor bulkhead | CAD added |
| I‑10 | secured 500 g | CAD added (tray bosses+slots); retention test |
| I‑11/12 | cooling / battery restraint | vents + strap slots; test |
| I‑13 | hand launch | handled risk (not a conflict) |
| I‑18 | NP/derivatives | **DONE** (VSPAERO VLM+panel) |
| I‑19/21 | fairing / infographic | fairing removed (lightening); spine TODO |
| I‑23 | wing_center material | resolved (LW + local PETG sleeve) |

**Blocking‑for‑flight until tested:** joint strength (I‑01/02/03/09), control function
(I‑05), and **pitch margin with fuselage included (panel run)**.

## 10. Next steps / TODO (prioritised)
1. **V6.1 DONE (this revision):** tail span 270→**300 mm** @47° (printable; TE≤970) + battery
   375→**285 mm** ⇒ CG ≈551 mm (25 % MAC); panel **NP 557 mm, SM ≈ +3 %** (was −3.9 %).
   Remaining: **add a small ventral fin** to lift yaw (Cnβ≈0.014), then print/bench.
2. **Print & fit** V6.1 parts; check interferences (grip recess vs belly clamp, hatch vs
   battery, hinge vs registration); print & pull‑test `insert_fit_coupon`.
3. **Material coupons:** LW‑PLA tensile/beam by orientation; PETG insert pull‑out.
4. **Propulsion/electrical:** pick motor/ESC/prop/battery; thrust stand → T/W; cooling,
   EMI layout, battery restraint, failsafe.
5. **Flight (only after 1–4):** bench controls → throw‑speed test → ground hops at a safe
   segregated site → progressive flight. Keep mass in the hand‑launchable band.
6. Update validation expected values + this file after each accepted change.


## 11. Conventions
- **Coordinates:** x = nose→aft (0…~970), y = span (+right), z = up; **mm**; fuselage centred
  y=0,z=0; wing chord line z=56; tail root z≈26.
- **Materials:** `LW` = foaming LW‑PLA (assumed 0.35 g/cm³); `PETG` = 1.27 g/cm³.
- **Part export:** change `part="..."` (or `-D 'part="..."'`). Full list in §5.
- **Evidence labels:** V / C / E / U / X (§7). Apply to every figure you add.
- **No silent carries:** if governs geometry or mass changed, recompute and note it.
- **File hygiene:** keep scratch in `/tmp`; `.gitignore` excludes `.DS_Store`,
  `__pycache__`, VSPAERO scratch.

## 12. Trust / provenance model
1. **Verified (V)** — independently recomputed from source (CAD volumes, analytic formulas,
   or a captured tool run in `data/`). Reliable within stated assumptions.
2. **Calculated (C)** — deterministic formula from stated inputs.
3. **Estimated (E)** — assumption‑dependent (density, battery, thrust); use as a band.
4. **Unverified (U)** — quoted, not checked (e.g., example component masses).
5. **Not run (X)** — explicitly absent (CFD, wind tunnel, flight, material tests).

Canonical sources on disagreement: geometry → SCAD + `STL/` volumes; mass/CG →
`verify_v6_stl.py` + `MASS_RANGE`; stability → `data/vspaero/` (panel run); narrative →
`engineering/audits/v5-configuration-b/`.

## 13. Change log
- **2026‑11‑22** — V5 audit; V6 SCAD created from V5 (structural/mechanism modules; fixed
  left‑side loft topology via mirror); 43 parts compile.
- **2026‑11‑23** — hatch flange; pushrod exits; rejected 80 g solid dorsal spine;
  **lightening 1403→1351.8 g**; verified mass envelope; **VSPAERO headless** (VLM + panel;
  tail study → panel shows fuselage destabilises pitch); multi‑view/exploded/**poster**;
  **validation suite 13/13**; repo reorganised (duplicates archived, `.DS_Store` removed);
  this AGENTS.md.

- **2026‑11‑23 (V6.1)** — V-tail span 270→300 @47° (printable; Vv 0.043→0.051, Vh 0.320→0.330),
  battery 375→285 (CG≈551, 25 % MAC); panel NP 553→557, SM −3.9 %→≈+3 %; Cnβ→~0.014 (still
  weak, ventral fin TODO); mass 1351.8→1360.8 g; VSPAERO V6.1 polars saved; validation updated
  (13/13); added `run_all.sh` + `Makefile` one‑command pipeline.

- **2026‑11‑23 (V6.1 + fin)** — added OPTIONAL removable ventral fin (LW, 15.4 cm³, +5.4 g,
  mass 1360.8→1366.2 g); 44 STLs; validation 13/13. Caveats: belly‑landing strike + headless
  VSPAERO did not register the fin surface (identical polars) — aero gain is analytic/provisional.

## 14. Quick reference
- Validate: `python3 engineering/tools/run_validation.py`
- Mass/CG: `python3 engineering/designs/v6/scripts/v6_calcs.py`
- Envelope: `python3 engineering/designs/v6/scripts/v6_mass_range.py`
- Export one part: `openscad -D 'part="wing_R1"' -o out.stl engineering/designs/v6/Kuma_FPV_V6_Configuration_B.scad`
- VSPAERO: `R=/Applications/OpenVSP.app/Contents/Resources; (cd /tmp/x && $R/vspscript -script <abs>/Kuma_V6_vspaero_run.vspscript)`
- Poster: `python3 engineering/designs/v6/scripts/make_poster.py`
- Trust first: `engineering/designs/v6/data/vspaero/V6_results.md` and
  `.../V6_panel_tail_study.md`.

---
_This document is the single source of truth for onboarding, running, and validating the
project. Update it (and the validation expected values) whenever the design or results change._

`engineering/designs/v6/`. Everything else is baseline, input, or archived.
