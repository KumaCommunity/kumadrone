# Kuma FPV V5 — Configuration B CAD / presentation package

This package is a **civilian educational RC airplane CAD study, not a flight-ready design**.

## Contents

- `Kuma_FPV_V5_Configuration_B.scad`: editable parametric OpenSCAD design.
- `STL/`: 32 exported individual part meshes (one is a *test coupon*; the wing key is printed in multiple copies).
- `CAD_Views/`: orthographic and exploded views directly rendered from CAD.
- `Kuma_FPV_V5_Configuration_B_OpenVSP.vspscript`: simplified native OpenVSP geometry generator; unexecuted/unverified in this environment.
- `NACA_2412_Wing_Root_200mm.dxf` / `NACA_0010_Tail_Root_190mm.dxf`: 2D airfoil outlines for CAD interchange.
- `Kuma_FPV_V5_ConfigB_CAD_Review.png`: CAD-derived technical poster.
- `Kuma_FPV_V5_ConfigB_Stylized_Infographic.png`: artistic presentation illustration, not a measurement reference.
- `Kuma_FPV_V5_Configuration_B_Engineering_Review.md`: calculations, assumptions, unresolved items.
- `geometry_mass_screen.csv`, `mass_budget.csv`, `loading_scenarios.csv`, `lift_screen.csv`, `sensitivity.csv`, `hardware_schedule.csv`, `metrics.json`: supporting engineering screens.

## OpenSCAD workflow

1. Open the `.scad` file and inspect `part="assembly"` or `part="exploded"`.
2. For individual model preview, change `part` to `fuselage_0`, `wing_R1`, `ruddervator_L`, `wing_key`, etc.
3. Confirm the printed insert hole dimensions using `part="insert_fit_coupon"`.
4. Do **not** treat exported meshes as structurally qualified: some STL files contain multiple closed disconnected components; check fit, load paths and slicer output.

V5 Configuration B is a **fixed wing**; the SCAD `payload_mass_g` switch only displays an illustrative equipment envelope, not a sliding wing station or validated mass capacity. The 500 g case assumes retained mass centered near x=556 mm rather than directly behind the camera.

## Export caveats

- No `.step` was exported: full native parametric STEP conversion from OpenSCAD is not verified in this environment.
- No new `.vsp3` was exported: the available earlier OpenVSP file describes prior V4/V5 geometry and must not be represented as this revision. Run the included `.vspscript` in OpenVSP to generate a provisional native model. The script was not executed or VSPAERO-validated here.
- CAD render and mass math were performed locally; aerodynamic and structural simulations were **not**.
