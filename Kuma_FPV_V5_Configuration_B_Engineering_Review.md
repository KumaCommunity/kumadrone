# Kuma FPV V5 — Configuration B

**Mechanical and aerodynamic screening | 22 November 2026**  
**Status: CAD concept, not flight validated.** Intended for a conventional civilian recreational RC airplane; no launcher, release mechanism, or automatically deployed wing is modeled.

## 1. Executive engineering assessment

The revision replaces the prior wing-position-changing, aileron-equipped V5 with **one fixed, transport-removable high wing**, 7° dihedral on each side, and **only the two upright V-tail ruddervators** as conceptual control surfaces. An optional **non-releasing retained-equipment envelope** has moved from x=205 mm toward the wing region at x=556 mm to reduce its fore–aft mass moment. The battery center moves toward the wing, from x=342 to x=410 mm in the CAD concept. The outside profile remains NACA 2412 for the wing and NACA 0010 for the tail.

**Passing arithmetic checks**: trapezoid wing geometry; internal mass summation; CG sensitivity given specified stations; lift-coefficient arithmetic; part-mesh closure. **Not passing / not assessed**: neutral point and static margin, rudder-only roll response, actual CLmax, structural spar continuity, repeated assembly fit, load-bearing fastener interfaces, propeller loads, control-servo adequacy, and flight endurance.

## 2. Grounded sources and design assumptions

- **Source model**: `Kuma_FPV_V5_loaded_primary.scad`, revised rather than replaced from scratch.
- **Original mass assumptions**: purchased-part placeholder masses and x stations inherited from the earlier V5 mass budget, updated for Configuration B. These are **not measured actual electronics**.
- **New estimated printed weights**: CAD export volumes from `geometry_mass_screen.csv` multiplied by 0.35 g/cm³ for foaming LW-PLA and 1.27 g/cm³ for PETG. This is **not slicer or scale data**.
- **Reference coordinate system**: x=0 at nose, x positive aft; y lateral; z upward. CAD dimensions in millimeters.
- **Optional 500 g envelope**: mass *scenario* only. No payload delivery or release system exists and no structural carrying capacity is established.

## 3. Geometry and airfoil review

| Quantity | Configuration B |
|---|---:|
| Fuselage nominal length | 970 mm |
| Full wing span, b | 1300 mm |
| Wing root chord / tip chord | 200 / 150 mm |
| Half-wing dihedral | 7° (hypothesis, not flight validated) |
| Geometric planform area, S | 0.22750 m² |
| Wing aspect ratio, b²/S | 7.43 |
| Wing taper ratio | 0.75 |
| Mean aerodynamic chord (MAC) | 176.19 mm |
| Wing root leading edge | x=496 mm |
| MAC leading-edge reference | x=507.43 mm |
| 28%-MAC illustration station | x=556.76 mm |
| Airfoil wing / tail | NACA 2412 / NACA 0010 |
| Upright V-tail inclination | 40° each from horizontal (CAD) |
| V-tail total geometric area | 0.0792 m² |
| Approx. projected horizontal-equivalent area | 0.0465 m² |
| Approx. projected vertical-equivalent area | 0.0327 m² |
| Approx. tail aerodynamic-center arm | 0.269 m |
| Simplified horizontal tail volume | 0.31 |
| Simplified vertical tail volume | 0.030 |

**Wing calculations**:  
`S = b (Cr + Ct) / 2 = 1.30(0.200 + 0.150)/2 = 0.2275 m²`.  
`AR = b² / S = 1.30² / 0.2275 = 7.43`.  
`MAC = (2 Cr / 3) × (1 + λ + λ²)/(1 + λ) = 176.19 mm`.  
The 28%-MAC point is only a convenient geometry marker. **It is neither the neutral point nor an established allowable CG location.**

**Airfoil decision:** Retain NACA 2412 and NACA 0010 as explicit analytic *geometry*. No evidence here demonstrates they are the best-drag or best-stall choices at the relevant Reynolds numbers (~120,000–191,000 for 10–16 m/s). Low-Reynolds airfoil and whole-aircraft analysis is required before that conclusion. The 7° dihedral is likewise a hypothesis for yaw-to-roll response with no ailerons.

**V-tail note:** The simple projected-area approximation applies `cos²(40°)` and `sin²(40°)` to the two tail panels. It is a first-order area proxy, not a stability-derivative model, and cannot prove control authority.

## 4. Packaging and preliminary mass balance

| Item | Station x (mm) | Preliminary role |
|---|---:|---|
| Camera | 38 | Forward analog FPV module |
| VTX and antenna | 130 | Near-front electronics |
| Receiver | 290 | Central avionics |
| ESC | 400 | Accessible electronics station |
| Battery center | 410 | Moved back toward leading-edge wing region |
| Optional retained-equipment compartment center | 556 | Adjacent to nominal wing balance region; does not discharge |
| Motor and prop | 970 | Rear pusher depiction only |

**Estimated assembled masses (from CAD volumes plus hypothetical purchased parts):**

| Mass source | Estimate |
|---|---:|
| LW-PLA shell parts | about 521 g |
| PETG fittings, trays and six wing keys | about 310 g |
| Hypothetical purchased components and hardware | 477 g |
| **No optional equipment** | **1,307.9 g** |
| **With 500 g additional retained equipment** | **1,807.9 g** |

`xCG = Σ(mᵢ xᵢ) / Σmᵢ`, with the 500 g center at x=556 mm. This result is sensitive to all mass assumptions, including the support structure needed to retain equipment.

| Added equipment | Estimated mass | Estimated CG x | Wing loading | Indicative stall speed* |
|---:|---:|---:|---:|---:|
| 0 g | 1,307.9 g | 560.0 mm | 57.5 g/dm² | 9.59 m/s |
| 100 g | 1,407.9 g | 559.7 mm | 61.9 g/dm² | 9.95 m/s |
| 250 g | 1,557.9 g | 559.4 mm | 68.5 g/dm² | 10.47 m/s |
| 500 g | 1,807.9 g | 558.9 mm | 79.5 g/dm² | 11.28 m/s |

*Stall-speed arithmetic assumes **CLmax = 1.0**, air density 1.225 kg/m³, and level, unaccelerated flow. CLmax and actual stall behavior are unverified. For the 500 g case, varying CLmax from 0.9 to 1.2 changes this arithmetic estimate from **11.89 to 10.30 m/s**, without establishing which value is realistic.*

This approach avoids relying on two unengineered wing-mounting stations. **It works arithmetically only if optional equipment can be packaged at the near-wing station**. Putting 500 g back at x≈205 mm recreates a significant forward CG shift; the present analysis does not support that layout.

## 5. Lift screening and endurance

Required level-flight lift: `L = m g`. At the illustrative masses, empty ~12.83 N; with 500 g ~17.73 N. Lift coefficient requirement uses `CL = 2 m g / (ρ V² S)`. The coefficient is an aerodynamic *requirement*, not the actual lift supplied at a particular pitch/trim.

| Airspeed | CL required unloaded | CL required +500 g | Chord Reynolds number |
|---:|---:|---:|---:|
| 10 m/s | 0.920 | 1.272 | 119,000 |
| 12 m/s | 0.639 | 0.884 | 143,000 |
| 14 m/s | 0.470 | 0.649 | 167,000 |
| 16 m/s | 0.360 | 0.497 | 191,000 |

No validated polar curves, thrust/power measurements or propulsive efficiency values are available, so **no credible endurance, safe cruise speed, or loaded payload capability can be asserted**. Enlarging the wing increased theoretical area 6.2% relative to previous V5 (0.2142 → 0.2275 m²), but may add structure and parasite drag; it is not proof of better flight time.

## 6. Modular printing and fastener review

- 6 separately exported fuselage shells; 5 PETG interface sleeves.
- One wing-center component and 3 removable panel sections per side. Fixed-wing full-chord panels replace prior separate aileron sections.
- Two V-tail panels and two separately exported ruddervator representations.
- PETG wing keys and center saddle; M3/M4 pilot holes retained from the source concept.
- Print-fit coupon and separate dorsal fairing added to the export inventory.
- Camera plate, near-wing equipment tray, and battery tray are removable conceptual modules.

**Mesh check:** 32/32 exported STLs are watertight according to Trimesh. But some wing and tail STLs contain **more than one disconnected closed body**. Watertight does not mean they will form a bonded, strong part after printing. Check slicer preview and repair unions before using these as load-bearing pieces.

**Interface check:** The M3 and M4 openings are nominal; threaded insert dimensions are unverified for the user's specific inserts. M3 PETG pockets shown as ~4.0 mm pilot / 6.8 mm depth and M4 as ~5.7 mm pilot / 9.2 mm depth. These are test-coupon dimensions, not universal specifications. Nose-camera brackets and fairing screw locations lack fully validated mating hardpoints. The wing spar, saddle, and V-tail joint load paths are **incomplete**; no assertion is made that these parts can carry flight loads.

## 7. Sensitivity checks

The file `sensitivity.csv` varies effective LW-PLA density from 0.25 to 0.55 g/cm³ and the assumed battery station by ±40 mm. Under those assumptions, the CG spans approximately **550–570 mm** unloaded, depending on material and battery arrangement. The 500 g scenario spans approximately **552–567 mm**. That is a much wider uncertainty range than the 1.1 mm center shift from varying equipment alone, and shows why measured part masses matter.

Real components may have additional mounting structure, different battery mass, wiring location and shell-density gradients that expand this interval.

## 8. Engineer review: required before any flight

1. Establish the neutral point, static margin, and usable CG range from an aircraft stability method. Do not assume 28% MAC is a stable design target.
2. Assess whether a 7°-dihedral wing with no ailerons and only V-tail ruddervators can produce acceptable yaw-to-roll coupling and disturbance recovery across the mass range.
3. Evaluate the V-tail's approximately 0.31 horizontal-volume / 0.030 vertical-volume *proxies*, including pitch/yaw mixing and tail control effectiveness.
4. Review airfoil polar behavior at ~120–190k Reynolds number, with realistic printed surface finish and wing/fuselage interference.
5. Check spar bending/torsion loads, root interfaces, threaded insert tearout, layer adhesion, repeated assembly and vibration; the pilot-hole and keyed geometry are not qualified joints.
6. Verify ruddervator hinge and linkage geometry, real servo torque and travel, motor mounting, rear-prop clearance and crash loads.
7. Weigh initial printed coupons and selected batteries/ESC/receiver, verify fit of the central equipment envelope, and update the mass spreadsheet.
8. Treat the 500 g case solely as a **hypothetical additional-equipment mass**, not a validated capacity or flight approval.

## 9. Validation conducted here

**Performed**: OpenSCAD CSG evaluation; exported part geometry; watertight mesh check for 32 STLs; CAD-volume estimate; theoretical mass-moment budget; wing planform, Reynolds number, basic lift arithmetic, stall-speed sensitivity, approximate projected V-tail volume.

**Not performed**: OpenVSP/VSPAERO solver run, validated neutral point, CFD, wind-tunnel tests, printer/slicer verification, fastener test fitting, static load testing, control-system or propulsion hardware specification, physical flights, actual endurance measurements.

The included stylized infographic is an **artistic concept illustration** and must not be used to measure parts. The CAD-derived view sheet and editable `.scad` are the dimensioned geometry references.
