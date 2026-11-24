# Manufacturing & Printability Review — Kuma FPV V5 Configuration B

**Reference printer:** ordinary consumer FDM, bed ≈ 220 × 220 × 250 mm. *No slicer was
run in this environment*; printability is assessed from verified mesh geometry, wall
dimensions, and orientation, and must be confirmed by slicing the actual meshes.

## 1. Build-volume fit (verified from STL bounding boxes)

All 32 meshes fit a 220 × 220 × 250 mm envelope. Largest footprints:

| Part | Bbox X×Y×Z (mm) | Fit | Print note |
|---|---|---|---|
| wing_L1/R1 | 197 × 202 × 47 | ✅ | 202 mm span — tight; ~9 mm margin/side |
| wing_L2/R2 | 181 × 202 × 46 | ✅ | |
| wing_L3/R3 | 166 × 202 × 44 | ✅ | |
| wing_center | 200 × 88 × 29 | ✅ | |
| tail_L/R | 142 × 194 × 167 | ✅ | tall V panel |
| ruddervator_L/R | 65 × 189 × 161 | ✅ | |
| fuselage_1/2 | 180 × 84 × 84 | ✅ | best printed standing on the round end |
| dorsal_fairing | 214 × 51 × 7 | ✅ | 214 mm long, flat |
| saddle_plate | 166 × 67 × 13 | ✅ | |

**Conclusion:** no part exceeds the reference bed. Only the wing panels and dorsal
fairing are near the ~200–220 mm limit (leave a skirt-free brim).

## 2. Mesh integrity

- **32/32 STLs watertight** (Trimesh). ✅
- **Wing panels, wing_center, tail panels, ruddervators are NOT single-manifold**: each
  contains an outer skin shell plus multiple internal *void* shells (wing panel = 1 outer
  + 3 chambers). This is the normal result of an OpenSCAD `difference()` of a cavity:
  the part prints correctly in mainstream slicers (nested surfaces → material between),
  but the non-stitched coincident faces can produce non-manifold edges. **Slice-preview
  and repair/unite before committing a load-bearing print** (as the source warns).
- **No self-intersection / normal audit was run** here — must be checked in the slicer.

## 3. Wall & feature integrity

- Fuselage shell wall = **1.25 mm** ≈ 3 perimeters at 0.4 mm — acceptable, but thin for
  LW-PLA; confirm with the chosen line width.
- Wing skins: shell = difference of outer loft and a 0.88-thickness / 0.96-chord inner
  loft → skins ~2–3 mm; webs ~2.7–4 mm — robust for LW-PLA.
- Key clearance 0.35 mm, coupler radial gap 0.30 mm — sensible FDM fits.
- M3/M4 pilot holes (4.0 / 5.7 mm) require the proven insert; the supplied
  `insert_fit_coupon.stl` is exactly the right first print.

## 4. Orientation / overhangs / supports

- **Wing panels:** the airfoil cross-section is a curved thin shell. Printed flat
  (span horizontal) the lower skin overhangs the leading edge; printed on-edge (span
  vertical, 202 mm tall) it is a tall thin curved wall prone to wobble. Best is to
  **split each panel into upper/lower halves or print leading-edge-down with support on
  the concave skin**, then bond. This is a real slicer decision, not shown in the CAD.
- **Fuselage sections:** stand them on the round end with the x-axis vertical → near-
  vertical walls (gentle taper) = very printable; the radial M3 holes are small horizontal
  features that bridge easily.
- **Tail panels / ruddervators:** canted thin surfaces — print on the flattest face;
  the 40° cant means one side overhangs.
- **Dorsal fairing:** flat, easy.
- **Trays / saddle / couplers / keys:** flat or ring parts, easy.

## 5. LW-PLA-specific behaviour

- **Foaming** means effective density (~0.25–0.55 g/cm³) is a *printer/setting outcome*,
  not a constant. Mass, CG, and even stiffness vary run-to-run. **Calibrate flow and
  weigh coupons before trusting any mass figure.**
- LW-PLA is **softer and more creep-prone** than PLA/PETG; thin skins dent and cold-flow
  under sustained bolt preload. Heat-set inserts must be in **PETG**, not LW-PLA.
- Foaming increases wall thickness slightly — holes/pockets shrink; print the insert
  coupon to measure the real hole before mass-producing couplers.

## 6. Does PETG reinforcement actually help?

- **Couplers, saddle plate, keys, tail saddle/shoes, trays:** PETG in the load-bearing
  interfaces is the right call (better insert retention and toughness than LW-PLA).
- **But** at ~310 g, the PETG fittings are ~24 % of empty mass for hardpoints that are, in
  several cases (saddle-to-fuselage, tail shoes), not yet connected. Until the joints are
  designed, the PETG mass buys **potential**, not proven durability. Once joints are
  defined, move inserts into fewer, thicker PETG bosses rather than many thin ones.
- **Material inconsistency (I-23):** the `wing_center` is annotated "Hollow PETG center
  section" in the SCAD but costed as LW-PLA in the mass tables. If it is PETG, add ≈114 g.
  For the part holding the spar bores and the M4 wing-mount, PETG is the sensible material —
  so treat the current mass budget as a **lower bound** on `wing_center`.

## 7. Assembly / disassembly verification

| Step | Feasible in CAD? | Issue |
|---|---|---|
| Fuse sections align | ✅ conceptually | couplers define alignment; to be print-tested |
| Wing attach | ⚠️ partial | M4 into saddle; saddle not attached to fuselage |
| Tail install | ⚠️ partial | shoes/saddle exist; panel registration undefined |
| Fastener access | ⚠️ | radial screws OK on fuselage; wing/tail need driver clearance |
| Electronics install | ⚠️ | no hatches; must open sections |
| Battery access / charging | ❌ poor | must unbolt sections to remove pack for charging |
| Camera replacement | ❌ | closed nose, no aperture/mount |
| Servo replacement | ❌ | no servo bay/linkage |
| Propulsion service | ⚠️ | motor envelope only; no mount/bulkhead |
| Disassembly for transport | ✅ | modular concept; wing/tail removable by design |

**Assembly-order interference** cannot be fully tested without the mechanisms, but the
wing-outboard-panel + key + through-spar assembly requires the spar to be inserted
*through* pre-assembled panels — verify the rod can actually be threaded in the intended
order (it must enter before the keys/screws lock).

## 8. Manufacturing verdict

Geometry is **printable on a 220-class printer with care**, but three things must be
proven on the bench before any structural claim: (1) slicer handling of the nested void
meshes, (2) wing-panel print orientation/splitting, (3) LW-PLA flow → real mass. The
biggest *assembly* gaps are service access (battery, camera, servos) and the undefined
wing/tail/motor joints.
