# Full Engineering Audit — Kuma FPV V5 Configuration B

**Audit date:** 22 Nov 2026 · **Basis:** independent review of the supplied CAD, exported
STLs, DXFs, CSVs and documentation. **No original V5 CAD was modified.** All recomputation
is in `scripts/`; intermediates in `data/`; figures in `graphics/`.

## 1. Method, sources and tool limitations

**Sources inspected:** `Kuma_FPV_V5_Configuration_B.scad` (primary geometry), 32 STL
meshes, two NACA DXFs, the engineering-review `.md`, six CSVs, `metrics.json`, the
OpenVSP `.vspscript`, six CAD view PNGs, and the stylised infographic.

**Performed:** STL volume/watertight/body/fit analysis (Trimesh); analytic NACA check;
planform, tail, V-volume and neutral-point recomputation; mass/CG rebuild; lift/Re/stall/
drag screens; hand-launch and lateral screening; spar/fastener/hinge screening; CAD views
and infographic review; parameter-derived plots.

**Not possible in this environment (stated, not fabricated):**
- **OpenSCAD not installed** → model not re-evaluated; geometry read from source parameters
  and cross-checked against exported STLs instead.
- **No slicer** → printability assessed from mesh/wall geometry, not actual toolpaths.
- **OpenVSP script not run, no VSPAERO, no XFLR5, no CFD, no wind tunnel, no flight test.**
- **No material testing** of printed LW-PLA/PETG. No measured component masses.

All aerodynamic and stability numbers are **analytical estimates / screens**, not CFD or
test data.

## 2. Geometry audit

Independently recomputed (detailed in `GEOMETRY_VERIFICATION.csv`, `CALCULATION_VERIFICATION.md`):

| Quantity | Value | Note |
|---|---:|---|
| Fuselage length / max diameter | 970 / 84 mm | body-section table |
| Wingspan / area / AR | 1300 mm / 0.2275 m² / 7.43 | verified |
| Root / tip chord, taper | 200 / 150 mm, 0.75 | verified |
| MAC / MAC LE / wing AC | 176.19 / 507.43 / 551.48 mm | AC derived |
| Root LE / tip LE / LE sweep | 496 / 520 mm, 2.11° | verified |
| Dihedral / tip rise | 7° / 79.8 mm | hypothesis, not validated |
| Incidence / twist | 0° / 0° | none modelled |
| Tail total area | 0.0792 m² | 2 panels |
| V-angle / Sh(cos²) / Sv(sin²) | 40° / 0.0465 / 0.0327 m² | proxy |
| Tail AC / arm | 820.1 mm / 268.6 mm | verified |
| Vh / Vv | 0.31 / 0.030 | verified |
| Fuselage internal volume | 3339.8 cm³ | discretised |

**Findings:** Geometry is internally consistent and matches the docs; no unintended
asymmetry (L/R meshes mirror-identical); coordinate convention (x nose→aft, y span, z up)
consistent. Additions: the wing AC is at 551.5 mm and the LE sweep is 2.11°; neither is in
the docs. **Wing incidence and twist are both zero and no decalage between wing and tail is
modelled** — a real design degree of freedom not exercised.

### Airfoil verification (DXF vs analytic) — `scripts/verify_airfoil.py`
- NACA 2412: 12.006 % t/c at x/c≈0.30, 2.0 % camber at 0.4, chord 200.03 mm ✅
- NACA 0010: 10.002 % t/c at x/c≈0.30, 0 % camber, chord 190.0 mm ✅
- **Open trailing edge** (0.10-coefficient, ~0.25 % chord gap) — fine for printing.
- **Caveat:** these are *familiar* profiles, not demonstrated *optimal* at Re≈100–200k.
  A cambered 4-digit section is a reasonable low-speed choice, but low-Re behaviour
  (laminar separation, hysteresis) is unverified; do not assume optimality.

## 3. Mass & balance

| Category | Mass (g) | Basis |
|---|---:|---|
| LW-PLA printed | 520.5 | CAD solid volume × 0.35 g/cm³ |
| PETG printed | 310.4 | CAD volume × 1.27 g/cm³ |
| Purchased placeholders | 477.0 | example components |
| **Empty** | **1307.9** | |
| **+500 g** | **1807.9** | |

| Case | CG x (mm) | % MAC | WL (g/dm²) | Vs CLmax1.0 |
|---|---:|---:|---:|---:|
| Empty | 560.0 | 29.9 | 57.5 | 9.59 m/s |
| 100 g | 559.7 | 29.7 | 61.9 | 9.95 m/s |
| 250 g | 559.4 | 29.5 | 68.5 | 10.47 m/s |
| 500 g | 558.9 | 29.2 | 79.5 | 11.28 m/s |

**Findings:**
- Arithmetic reproduces exactly. **But the printed mass rests on an assumed 0.35 g/cm³
  foaming density** — the single largest uncertainty. Over 0.25–0.55 g/cm³ the empty mass
  spans ~1160–1605 g and CG ~550–566 mm (`sensitivity.csv`).
- **The 500 g case is CG-neutral only because the load is placed at x=556 mm ≈ CG.** This
  is an assumption, not a capability. Placed forward, CG shifts substantially.
- **CG at ≈30 % MAC is aft of the wing AC (25 %).** With the provisional neutral point at
  ≈37.7 % MAC, static margin ≈+8 % — positive, but the aircraft trims with a small tail
  *download*. Moving CG to ~26–27 % MAC (battery forward) would raise SM and cut trim drag.
- Empty CG is credible *given the assumptions*, but is driven by battery station and LW-PLA
  density more than by the airframe.

## 4. Aerodynamics

Lift/Re/stall recomputation matched the source exactly (`AERODYNAMIC_SCREENING.csv`).
Additions:

- **Wing loading 5.75 kg/m² empty, 7.95 kg/m² loaded** — high for a hand-launched model.
- **Stall 9.59 / 11.28 m/s** (CLmax 1.0) empty/loaded; CLmax 0.9–1.2 moves loaded stall
  11.89→10.30 m/s. **CLmax unverified.**
- **Re ≈ 95k–215k** over the flight envelope — low-Re regime where 4-digit polars are
  uncertain and printed surface roughness matters.
- **Analytical polar** (CD0=0.038, e=0.85): best L/D ≈11.4 both cases (UNVALIDATED). This
  is a *screen*, not a measured glide ratio; exposed VTX/antenna, camera, and FDM texture
  will lower it.
- **Induced-drag factor** dCDi/dCL² = 1/(π·AR·e) ≈ 0.0505 — AR 7.43 is healthy for the span.
- The 1.3 m span is *reasonable* for ~1.3 kg but *marginal* at 1.8 kg. Do not optimise one
  metric (e.g. span) without checking structural and handling penalties.


## 5. Stability and flight control

### Longitudinal
- Wing AC 551.5 mm; tail AC 820.1 mm; arm 0.269 m; **Vh ≈ 0.31** (up to ~0.41 using area
  projection instead of cos²) — low-to-adequate.
- **Neutral point ≈ 573.8 mm** by lift-slope + tail-volume method; sweeps 571–580 mm for
  dε/dα 0.10–0.40 and tail-effectiveness 0.7–1.0 (`data/stability.csv`, figure
  `graphics/static_margin_sensitivity.png`).
- **Static margin ≈ +7.8 % MAC empty, +8.5 % loaded** — positive and adequate *for pitch*,
  but **method-limited** (no Munk moment, no wing-body interference, empirical a_t). Treat
  as provisional; confirm before flight.
- Trim: CG aft of wing AC ⇒ tail download ⇒ slightly higher effective wing loading.

### Lateral/directional (the weak axis)
- **Vv ≈ 0.030** — low end of acceptable; weak directional stability/soft rudder.
- **Cl_β ≈ 0.08–0.16 /rad** (high wing + 7° dihedral) — plausibly adequate to convert
  sideslip to bank.
- **No ailerons** ⇒ roll only via rudder→yaw→sideslip→dihedral roll. Response likely
  **sluggish**, poor in gusts/crosswind, demanding to fly. 7° dihedral does **not**
  guarantee acceptable turning — unproven, must be validated.
- Differential ruddervator couples yaw↔pitch; mix setup is sensitive.

### Mechanical controls
- **None functional in CAD:** no hinge, horn, servo, pushrod, or travel limit. Ruddervators
  are cosmetic shells (I-05) — the single biggest flight-readiness gap.
- *Sizing:* hinge moments 0.5–1 N·cm ⇒ a standard micro servo has ample torque; the deficit
  is mechanism, not power.

### Verdict
**Rear-only control is a credible *direction* only if** (a) the mechanism is designed, (b) Vv
is increased or flight-tested to show acceptable yaw/roll, (c) a 6-DOF sim + flight test
confirm handling across the mass range. As it stands it is **a hypothesis, not a
substantiated control concept.**

## 6. Structures
See `STRUCTURAL_REVIEW.md`. The twin-spar/full-depth-web wing and coupler-ring fuselage
joints are **credible concepts**; the 8 mm carbon spar is adequately sized (FS≈3 at +4.5 g).
But **four load paths are undefined in CAD** — centre spar joiner, wing-saddle-to-fuselage,
tail-panel-to-shoe, ruddervator hinge — plus the motor thrust bulkhead. No material data for
printed orientation ⇒ **no defensible FS** on printed structure. Not flight-safe as drawn.

## 7. Manufacturing
See `MANUFACTURING_REVIEW.md`. All 32 parts fit a 220×220×250 bed; all watertight. Wing/tail
meshes are **nested multi-shell** (outer skin + void chambers) — slicer must handle/repair;
wing print orientation must be chosen (may split panels). LW-PLA density is a slicer outcome.
Service access is the weak point. PETG reinforcement is the right material for inserts but
currently buys "potential" until joints exist.

## 8. Electrical & propulsion
See `ELECTRICAL_REVIEW.md`. A **placeholder list, not a design**: no motor/ESC/prop/servo
ratings, no power distribution, no cooling, no EMI layout, no battery restraint, no failsafe.
Compatibility and endurance **cannot** be assessed. Cooling and battery retention are
safety-relevant omissions.

## 9. Hand launch and landing

| | Empty 1.31 kg | +500 g 1.81 kg |
|---|---:|---:|
| Wing loading | 5.75 kg/m² | 7.95 kg/m² |
| Stall (CLmax 1.0) | 9.59 m/s | 11.28 m/s |
| Safe launch (1.15–1.3 Vs) | 11.0–12.5 m/s | 13.0–14.7 m/s |
| Launch KE (1.3 Vs) | ~100 J | ~150–190 J |
| Achievable hand throw | 8–10 m/s (hard) | ~6–8 m/s |

- **Empty: marginal.** Needs a hard, well-aimed throw; under-throws stall.
- **+500 g: not hand-launchable** by a person; no launcher permitted ⇒ **requirement
  conflict** (Critical).
- **Landing:** belly lander on LW-PLA; nose camera (if integrated) and rear prop vulnerable;
  repeated belly landings abrade LW-PLA. Grip near CG (Ø76 mm fuselage) plausible, but the
  1.8 kg one-hand throw is not.

## 10. Design efficiency & DFM

- **Redundancy:** six fuselage sections + five couplers is a lot of jointing for a 970 mm
  airframe; the coupler scheme is sound but every seam is a mass/wear/assembly cost. Consider
  merging the mid sections.
- **Heavy plates:** the ~310 g of PETG is ~24 % of empty mass, concentrated in couplers,
  saddle, shoes, keys, trays. Much of it is bought for joints that are not yet connected.
- **Fastener count** (~50+ M3/M4, some M2) is high because access = unbolt sections. A single
  large hatch would cut both count and service time.
- **Segmentation vs repairability:** the modular scheme genuinely aids repair/transport
  (a strength), but over-segmenting the fuselage and the tiny 202 mm wing panels add joints.
- **Standardise:** mostly M3 is good; drop M2 if the camera bracket allows.
- **Benchmark:** conventional 3D-printed hand-launch trainers (e.g. LW-PLA plank wings with a
  single spar and 2–4 fuselage sections, aileron+elevator or RE config) achieve similar span
  at **less mass and fewer joints**. The current design is heavier and more fragmented than
  the practice norm — a candidate for simplification, but **not by removing material before
  joints are proven.**

## 11. Exterior & visual review (CAD vs infographic)

The **CAD is authoritative**; the infographic is aspirational. Discrepancies:

| Feature | Infographic | CAD | Status |
|---|---|---|---|
| Nose | sleek, tapered | blunt rounded cone | differ |
| Fuselage–wing blend | smooth fillet/saddle | thin flat saddle plate | **missing in CAD** |
| Dorsal spine to tail | continuous spine | floating 445–605 mm fairing, gap to tail | **missing in CAD** |
| Spinner/motor fairing | spinner cone | flat prop disc + motor cylinder | **missing in CAD** |
| Tail | refined V + center fin-ish blend | chunky separate V panels + shoe blocks | cruder in CAD |
| Cameras/lens | integrated nose lens | plate inside closed nose (no aperture) | **missing in CAD** |
| Surface continuity | smooth | hard panel breaks | cruder in CAD |

**Findings:** proportions (span/length/tail) are consistent and read well; left/right parts
are symmetric. The infographic implies features that do not exist in CAD (fillet, spine,
spinner, integrated lens). Recommend reconciling — either add the features to CAD or amend
the infographic. Cosmetic only; separate from engineering-critical gaps.

## 12. Assumptions, uncertainty & sensitivity (see `ASSUMPTIONS_REGISTER.csv`)

Highest-impact unknowns, ranked:

1. **CLmax (A07)** — sets stall/launch; swings loaded Vs 10.3–11.9 m/s.
2. **LW-PLA density (A01) / printed mass (A03)** — swings empty mass ~±20 % and CG ~±8 mm.
3. **Neutral point method (A09–A12)** — SM could be a few % lower; Munk moment unmodelled.
4. **Dihedral effect / lateral derivatives (A20)** — decides whether rear-only control works.
5. **500 g loading station & packaging (A16/A17)** — decides whether the load is even
   carryable; and it conflicts with launch regardless.
6. **Spar material & joint strength (A25/A19)** — decides structural feasibility.
7. **Motor/prop/ESC (A08)** — decides climb, launch assist (none), endurance.

**Measurements that would most reduce uncertainty before the next prototype:**
(a) weigh printed coupons at the chosen LW-PLA flow; (b) weigh the actual battery/RX/camera/
VTX/servos; (c) measure the real CG of the assembled airframe; (d) print & pull-test an insert
coupon; (e) confirm CLmax/derivatives via XFLR5/AVL + a throw-speed test.

## 13. Cross-validation (CAD ↔ docs ↔ infographic ↔ calculations)

- **CAD vs docs:** dimensions and masses agree (verified to <0.1 g / <0.05 mm). Docs
  correctly flag incomplete joints, unverified CLmax, and the 28 %-MAC caveat.
- **Calculations vs docs:** every published number reproduced; no arithmetic errors. New
  values added: wing AC, neutral point, static margin, internal volume, lateral screening.
- **Infographic vs CAD:** significant aspirational-only features (see §11). Infographic not a
  measurement reference.
- **STL vs CAD parameters:** mesh volumes/bboxes consistent with the parametric model;
  L/R symmetric; nested-shell structure explained.

## 14. Final assessment & action plan

**Assessment: REQUIRES SIGNIFICANT DESIGN REVISIONS.**
The configuration is a geometrically coherent, arithmetically correct **concept** with a
sound *structural* and *aerodynamic* skeleton (two-spar wing, coupler joints, reasonable
span/AR, positive provisional pitch margin). It is **not** a flight-ready design: the flight-
control mechanism, four load paths, the nose camera, and the electrical system are absent or
undefined, and the **500 g / hand-launch requirements are in direct conflict.** A favourable
verdict here is **not** airworthiness certification.

### Smallest set of changes/measurements to resolve the largest uncertainties

**Do first (days):**
1. Weigh LW-PLA & PETG coupons → real printed mass & CG. (Kills the biggest CG/launch
   uncertainty.)
2. Decide the 500 g vs hand-launch requirement (redefine equipment mass or launch method).
3. Print & pull-test the insert coupon.

**Design (weeks):**
4. Design the ruddervator hinge/horn/servo/pushrod + mix (sizing already shown adequate).
5. Design wing carry-through + centre spar splice + saddle-to-fuselage bolts; motor bulkhead.
6. Cut the nose camera aperture/cradle; add battery/camera/servo hatches.

**Verify before flight:**
7. Neutral point & lateral derivatives via VSPAERO/AVL/XFLR5; 6-DOF handling check.
8. Wing static pull-up to ≥1.5× ultimate; tail/control bench rig; throw-speed test.
9. Full electrical definition (ratings, cooling, EMI, battery restraint, failsafe).

Only after steps 1–9 should flight testing be considered — and then progressively (ground
range, low hops at a safe segregated site, then flight), with the mass kept at the hand-
launchable (≈≤1.2 kg) condition.
