# Calculation Verification — Kuma FPV V5 Configuration B

**Purpose:** Independently recompute every important numerical claim in the supplied
engineering review and CSV outputs, from the SCAD parameters and raw STL meshes.
Reproduce with `scripts/audit_calcs.py`, `scripts/verify_stl.py`, `scripts/verify_airfoil.py`.

Legend: **MATCH** = within rounding; **CALCULATED** = derived here, not stated in source.

## 1. Wing planform

| Quantity | Method | Source value | Recomputed | Verdict |
|---|---|---:|---:|---|
| Wing area S | b(Cr+Ct)/2 | 0.22750 m² | 0.22750 m² | MATCH |
| Aspect ratio | b²/S | 7.43 | 7.429 | MATCH |
| Taper ratio | Ct/Cr | 0.75 | 0.750 | MATCH |
| MAC | (2/3)Cr(1+λ+λ²)/(1+λ) | 176.19 mm | 176.19 mm | MATCH |
| MAC span station | 650(1+2λ)/(3(1+λ)) | — | 309.5 mm | CALCULATED |
| Root LE x | 310+186 | 496 mm | 496 mm | MATCH |
| MAC LE x | derived | 507.43 mm | 507.43 mm | MATCH |
| 28% MAC station | LE_MAC+0.28MAC | 556.76 mm | 556.76 mm | MATCH |
| Wing AC (25% MAC) | LE_MAC+0.25MAC | — | 551.48 mm | CALCULATED |
| LE sweep | atan((520−496)/650) | — | 2.11° | CALCULATED |

**Finding:** Wing arithmetic is correct and reproducible. The 28%-MAC station is
correctly labelled in the source as a geometry marker, not an allowable CG.

## 2. V-tail

| Quantity | Method | Source | Recomputed | Verdict |
|---|---|---:|---:|---|
| Panel / total area | trap | 0.0792 m² | 0.0396 / 0.0792 m² | MATCH |
| Sh (cos²Γ) | 0.0792cos²40° | 0.0465 m² | 0.04648 m² | MATCH |
| Sv (sin²Γ) | 0.0792sin²40° | 0.0327 m² | 0.03272 m² | MATCH |
| Area projection (cosΓ) | 0.0792cos40° | — | 0.06067 m² | CALCULATED |
| Horizontal span / AR | — | — | 391.7 mm / 3.301 | CALCULATED |
| Tail AC x | — | — | 820.1 mm | CALCULATED |
| Tail arm | tail AC−wing AC | 0.269 m | 0.2686 m | MATCH |
| Vh / Vv | Sh·l/(S·MAC); Sv·l/(S·b) | 0.31 / 0.030 | 0.3115 / 0.0297 | MATCH |

**Finding:** All tail arithmetic reproduces. The cos²/sin² "equivalence" is a
first-order proxy; the pure *area* projection (0.0607 m²) differs from the cos²
proxy by ~30%. Defensible band: **Vh ≈ 0.31–0.41, Vv ≈ 0.030–0.040**.

## 3. Mass

| Quantity | Source | Recomputed | Verdict |
|---|---:|---:|---|
| LW-PLA printed | ~521 g | 520.55 g | MATCH |
| PETG printed | ~310 g | 310.38 g | MATCH |
| Purchased placeholders | 477 g | 477.0 g | MATCH |
| Empty / +500 g total | 1307.9 / 1807.9 g | 1307.94 / 1807.94 g | MATCH |

**Finding:** Printed totals were recomputed independently from the 32 STL meshes
(signed-tetrahedron volume) and reproduce the source to <0.1 g. Arithmetic sound;
the density assumption (0.35 g/cm³) is the weak link (ASSUMPTIONS A01/A03).

## 4. Center of gravity

| Case | Source CG | Recomputed | Verdict |
|---|---:|---:|---|
| Empty | 560.0 mm | 560.02 mm | MATCH |
| 100 g @556 | 559.7 mm | 559.74 mm | MATCH |
| 250 g @556 | 559.4 mm | 559.38 mm | MATCH |
| 500 g @556 | 558.9 mm | 558.91 mm | MATCH |

**Finding:** Mass-moment summation is correct. Because added equipment is placed at
x=556 mm (essentially on the CG), the CG shifts only ~1 mm across 0–500 g — *by
construction*. This is a modelling choice, not an aerodynamic result. If the same
500 g sits forward (x≈205 mm), the CG moves materially forward (see `sensitivity.csv`).


## 5. Aerodynamics & Reynolds number

| Quantity | Source | Recomputed | Verdict |
|---|---:|---:|---|
| CL req empty @10 m/s | 0.920 | 0.9205 | MATCH |
| CL req +500 g @10 m/s | 1.272 | 1.2724 | MATCH |
| Re @10 / @16 m/s | 119k / 191k | 119,245 / 190,792 | MATCH |
| Lift empty / +500 g | 12.83 / 17.73 N | 12.827 / 17.73 N | MATCH |
| Stall empty / +500 g (CLmax1.0) | 9.59 / 11.28 m/s | 9.59 / 11.28 m/s | MATCH |
| Wing loading empty / +500 g | 57.5 / 79.5 g/dm² | 57.49 / 79.47 g/dm² | MATCH |

**Finding:** All lift/Re/stall arithmetic correct; conclusions correctly conditioned
on unverified CLmax=1.0 (loaded stall 11.89→10.30 m/s over CLmax 0.9–1.2).

## 6. Quantities the source does NOT compute (added by this audit)

| Quantity | Result | Basis |
|---|---|---|
| Wing aerodynamic center x | 551.48 mm | 25% MAC |
| Neutral point x | **573.8 mm** (571–580 sweep) | lift-slope + tail-volume method |
| Static margin empty / +500 g | **+7.8 % / +8.5 % MAC** | (x_np−x_cg)/MAC |
| Fuselage internal volume | 3339.8 cm³ | body of revolution, 1.25 mm wall |
| Trim note | CG aft of wing AC ⇒ tail carries download in trim | qualitative |

Full grid in `data/stability.csv`. Static margin is **positive but thin and
method-dependent**; the pusher fuselage Munk moment (not modelled) would reduce it.
Confirm by a proper method before flight.

## 7. Discrepancies found

1. **`sensitivity.csv` CG spread is dominated by density/battery, not equipment.**
   Empty CG spans ~550–570 mm as LW-PLA density varies 0.25–0.55 g/cm³. This is the
   dominant uncertainty and should be emphasised over the ±1 mm equipment effect.
2. **The 500 g case is CG-neutral by assumption** (placed at 556 mm ≈ CG). The doc is
   honest about this, but the 254 cm³ envelope is small for 500 g (~2.0 g/cm³ packing)
   and has no modelled structural retention.
3. **No arithmetic errors** were found in the published wing/tail/mass/lift/stall
   numbers. Discrepancies are in *method completeness and assumption provenance*.
4. **`wing_center` material inconsistency (found by this audit).** The SCAD comment calls it
   a **"Hollow PETG center section"** (line 205), but `geometry_mass_screen.csv` and
   `mass_budget.csv` classify it **LW-PLA at 0.35 g/cm³** (43.47 g). If it is actually PETG
   (the engineering-sensible choice, since it houses the 8 mm spar bores and M4 wing-mount
   bolts), its mass is **124.209 cm³ × 1.27 = 157.75 g**, i.e. **+114.3 g**. That raises empty
   mass to ≈1422 g and moves CG aft by ~1.7 mm (to ≈561.7 mm) — worsening wing loading and
   hand-launch margin. **Resolve the material assignment before trusting the mass budget.**

## 8. Reproducibility

```
python3 scripts/verify_stl.py         # 32 STLs: volume, watertight, bodies, fit
python3 scripts/verify_airfoil.py     # DXF vs analytic NACA
python3 scripts/audit_calcs.py        # geometry, mass, CG, aero, stability
python3 scripts/launch_lateral.py     # hand-launch + lateral screening
python3 scripts/structural_screen.py  # loads, spar, fasteners, hinge moments
python3 scripts/plot_graphics.py      # review graphics
```
