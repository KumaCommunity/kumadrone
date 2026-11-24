# Kuma FPV V6 — Configuration B (first revision after audit)

**Status: parametric CAD revision — COMPILED & volume-verified (OpenSCAD 2026.10.11). Not flight‑ready.**
V6 takes the V5 concept and addresses the audit's Critical/High findings. **All 43 parts now
compile manifold with `Status: NoError`**, STLs are exported to `STL/`, and the empty mass is
measured at **1403 g**, then **lightened to 1351.8 g** (−51 g). Mechanical
fit iteration and testing are still required; this is not airworthiness.

## V6.1 (current revision — supersedes the V6 baseline numbers below where they differ)
- **V-tail:** span 270→**300 mm**, dihedral 45→**47°** (span capped so each panel fits a 220 mm
  bed; TE stays ≤970 mm). **Vh 0.320→0.330, Vv 0.043→0.051.**
- **Battery** 375→**285 mm** ⇒ CG ≈ **551 mm (25 % MAC)**.
- **Panel (incl. fuselage): NP 557 mm, SM ≈ +3 %** (V6 baseline was −3.9 % at CG 560).
  **Cnβ still weak (~0.014/rad)** → next: small **ventral fin**.
- **Mass 1360.8 g** (V6 lightened 1351.8 + ~9 g bigger tail). Validation updated (13/13).
- **Optional removable ventral fin** added (LW, 15.4 cm³, +5.4 g): yaw aid for flight test only.
  Caveats: a fin tall enough to help will strike on a belly landing; headless VSPAERO did **not**
  capture the added fin surface (identical polars), so its Cnβ gain is analytic/provisional (~+10 %).
- Historical V6 baseline values remain documented below and in `data/vspaero/V6_results.md`.

## Additional refinements (post first compile)
- **Hatch registration flange** added to the battery lid (+2.8 g) so it locates in the opening.
- **Pushrod exit holes** added in `fuselage_4` so the ruddervator pushrods reach the horns.
- **Dorsal spine trialled and REJECTED:** a solid `hull()` fairing came out **~80 g**, too heavy
  for a cosmetic part; a thin *shelled* spine is the correct future approach (noted in the SCAD).
- **Verified mass envelope** (`scripts/v6_mass_range.py`, measured volumes, density swept):
  empty **1099–1752 g** (nominal **1351.8 g** after lightening), +500 g **1599–2252 g**;
  empty WL 50.4–79.4 g/dm², Vs 8.98–11.28 m/s; +500 WL 72.4–101.4 g/dm², Vs 10.76–12.74 m/s.
- **VSPAERO ran headless** (OpenVSP 7.2.2 `vspscript`; the Python geometry API segfaults
  but the script CLI works). **Wing+tail VLM** → SM +8.31 % / NP 574.6 mm (matches analytical).
  **Panel method incl. fuselage** → **SM −3.9 % / NP 553 mm** — see IMPORTANT below.
- **IMPORTANT (panel method, fuselage included):** the fuselage's Munk moment removes
  ≈12 % MAC of pitch margin and ≈0.07 /rad of yaw. **At the current CG (30.7 % MAC) the
  aircraft is marginally unstable in pitch and ~neutral in yaw.** The VLM‑only "+8 %" is
  optimistic and is NOT a valid stability claim. A tail study (`data/vspaero/V6_panel_tail_study.md`)
  shows a **bigger tail (span 0.33, chords 0.23/0.17, ~47°)** plus **CG ≈24–27 % MAC** restores
  SM ≈ +5.6 %; Clβ ≈ 0.4/rad (strong), Cnβ still modest (~0.08/rad).
- **Lightening pass (verified):** removed redundant camera plate (−9 g) and floating dorsal
  fairing (−11 g), battery tray → LW‑PLA (−20 g), shoe/key lightening pockets (−12 g) →
  **1403.0 → 1351.8 g (−51 g)**; empty WL 61.7→59.4 g/dm², Vs 9.93→9.75 m/s.
- **Render sheet:** `graphics/v6_front.png`, `v6_side.png`, `v6_top.png`, `v6_rear.png`
  (orthographic, from exported STLs) + `v6_iso.png` + `v6_exploded.png`.
- **Stylized concept poster:** `graphics/v6_poster.png` (dark "concept sheet": silver
  CAD-derived hero + ortho views + internal layout + exploded + spec panels + CONCEPT badge).
  Built by `scripts/render_dark.py` (silver/transparent views, incl. iso & exploded) and
  `scripts/make_poster.py` (PIL layout). It is a technical concept sheet from CAD geometry —
  **not a photoreal render** (no materials/lighting engine).

## Compilation & verification (done)
- Renderer: **OpenSCAD 2026.10.11** (`/opt/homebrew/bin/openscad`).
- **43/43 parts export manifold/NoError**; 0 parts exceed a 220×220×250 bed.
- A **real defect was found and fixed**: building lofted surfaces with `s=-1` produced a
  topology blow‑up on this OpenSCAD (e.g. `wing_L1` 1346 cm³ / 6423 bodies / genus 106). The
  **same happens to the original V5 file** on this version (the shipped V5 left‑side STLs must
  have come from an older toolchain). V6 fixes it by making `wing_loft`, `wing_web`, `tail_loft`
  build the +y half and `mirror([0,1,0])` for the left side → clean, watertight, symmetric
  (L1 = R1 = 181.86 cm³, tail_L = tail_R, etc.).
- Assembly renders to `graphics/v6_iso.png`.

## Files
- `Kuma_FPV_V6_Configuration_B.scad` — revised parametric model.
- `DESIGN_CHANGES.md` — every change traced to an audit issue ID, with before/after numbers.
- `scripts/v6_calcs.py` — runnable geometry/mass/CG/stability recalculation (verified).
- `data/v6_geometry.csv`, `v6_loading.csv`, `v6_mass_detail.csv` — outputs.
- `openvsp/Kuma_V6_vspaero.vspscript` — V6 aero model (corrected fuselage + enlarged tail)
  for the derivative/neutral‑point run; use with `engineering/audits/.../scripts/parse_vspaero.py`.

## What changed (headline)
| Area | V5 | V6 |
|---|---|---|
| Wing | span 1300, AR 7.43, 7° | **unchanged** (verified good) |
| Tail | 240 / 190·140 / 40°, Vv 0.030 | **270 / 200·150 / 45°, Vv 0.043** (better directional + ruddervator authority) |
| Wing→fuselage | saddle floating | **clamp + 4 straps + under‑belly + 4×M4** to fuselage |
| Centre spar | half‑spars butt | **bonded joiner + cross‑pin** |
| Controls | cosmetic shells | **hinge pin+knuckles, horns, servo bays, pushrods** |
| Nose camera | closed, floating plate | **13 mm aperture + camera cradle** |
| Access | unbolt sections | **battery hatch + lid, servo bays** |
| Motor | envelope | **PETG bulkhead + 4×M3 mount** |
| 500 g load | illustrative tray | **secured tray (bosses + strap slots)** |
| Cooling | sealed | **nose inlet + aft exit** |
| Battery | x=410 | **x=375 (CG margin), hatch, strap** |
| Mass | 1308 g | **1351.8 g verified** (lightened) |
| Static margin | +7.8 % | **+7.5 %** est · **+8.3 % VSPAERO** |

## Rendering / exporting (verified working)
1. Open `Kuma_FPV_V6_Configuration_B.scad`. Set `part="assembly"` and press **F5/F6**. It
   compiles clean; `part` is CLI-overridable: `openscad -D 'part="wing_R1"' -o out.stl file.scad`.
2. Export each STL by changing `part=`. New part names:
   `wing_saddle_clamp`, `centre_spar_joiner`, `wing_center_spar_sleeve`, `motor_bulkhead`,
   `camera_cradle`, `battery_hatch_lid`, `secured_tray`, `ruddervator_hinge_R/L`,
   `control_horn_R/L`. Existing names unchanged; `fuselage_0/2/3/4/5` now carry the nose
   aperture / battery hatch / grip / cooling+servo / motor cuts respectively.
3. Slice‑preview especially: wing panels (nested void shells — repair if needed), the new
   clamp and hatch (clearances), and the nose aperture vs camera cradle alignment.

## Test plan (in order)
1. **Weigh V6 parts** → replace the +92 g estimate → re‑run `v6_calcs.py`.
2. **Fit‑check** clamp/hinges/bulkhead/hatches/cradle; tune M4/M3 clearances and insert depths
   (`insert_fit_coupon`).
3. **Bench the ruddervator mechanism**: travel, slop, centering, blow‑back speed.
4. **Thrust stand** the motor → T/W; **wing pull‑up** to ≥1.5× ultimate; **tail pull**.
5. ~~VSPAERO~~ **DONE** (headless): SM +8.31 %, NP 574.6 mm, Cnβ ~0.075/rad (weak),
   Clβ ~0.21/rad — see `data/vspaero/V6_results.md`. (Directional stiffness remains the
   weak axis; consider more Vv if flight test shows poor spiral/gust behaviour.)
6. **Throw‑speed test** at the real mass (see mass range) before a loaded launch.

## Important caveats
- **Compiles, but not fit‑tested.** CSG is clean (all parts manifold/NoError, verified mass
  1351.8 g); interferences (e.g., grip recess vs belly clamp) and clearances still need a
  physical print/fit check. Treat V6 as a design proposal, not a proven airframe.
- **Mass is up ~92 g** for real structure; empty WL 57.5→61.5 g/dm², +500 g WL → 83.5 g/dm²
  (Vs 11.56 m/s). Hand launch is closer to its limit — trim PETG or accept a firmer throw
  ("redesign the launch system if needed").
- **Estimated** new‑part masses (±30 %); measure before trusting CG.
- Wing planform, airfoils, and 7° dihedral intentionally unchanged; still to be validated by
  VSPAERO/flight test (derivatives, low‑Re CLmax).
- V6 is a **civilian recreational RC concept**; not airworthiness‑certified.
