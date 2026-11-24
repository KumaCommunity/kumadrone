# OpenVSP / VSPAERO workflow — Kuma V5 Config B

Purpose: obtain **stability derivatives** (CLα, Cmα, Cnβ, Clβ) so the neutral
point and static margin can replace the audited analytical estimate
(x_np ≈ 573.8 mm, SM ≈ +7.8 % MAC). This is the proper method the audit recommended.

> These files are authored to OpenVSP conventions but were **NOT executed in the
> audit environment** (OpenVSP is not installed there). Function names vary slightly
> by OpenVSP version — verify against your build. The geometry builder is modelled on
> the supplied, previously-working `.vspscript`.

## Files
- `Kuma_V5B_vspaero.vspscript` — builds wing + upright V-tail + fuselage (fixes the
  supplied model's fuselage diameter bug: FineRatio 23.095 → **11.55**).
- `../scripts/parse_vspaero.py` — reads VSPAERO `.polar` / `.stab` output, computes
  CLα, Cmα, **static margin = −Cmα/CLα**, **x_np = X_ref + SM·cref**, plus Cnβ/Clβ,
  and compares to the audit values.

## Step 1 — build the model
OpenVSP → **File ▸ Run Script…** → `Kuma_V5B_vspaero.vspscript`. It writes
`Kuma_V5B_vspaero.vsp3`. Confirm in the 3-D view: wing ~1.30 m span with 7° dihedral,
V-tail ~40°, fuselage ~84 mm max diameter, nose at x=0.

## Step 2 — set VSPAERO reference values (CRITICAL)
Open **Analysis ▸ VSPAERO** (or the VSPAERO tool panel). Set:

| Parameter | Value | Why |
|---|---|---|
| Sref | 0.2275 m² | wing area |
| bref | 1.300 m | span |
| cref | 0.17619 m | MAC |
| Xcg, Ycg, Zcg | 0.560, 0, 0 m | **moment reference = CG** (the NP is measured from here) |
| Wake/flow | defaults OK | |
| Ref velocity / Re | e.g. 12 m/s, Re based on cref (~140k) | representative |

`x_np = Xcg + SM·cref`. If you also change CG later, re-run with the new Xcg.

## Step 3 — run the analysis (choose one)

**Option A — Stability run (fastest).** In VSPAERO, choose **Stability**, one
condition (e.g. α=2°, β=0, M≈0.035). VSPAERO writes `<name>.stab` containing
derivatives (CLα, Cmα, Cnβ, Clβ, …). Feed it to the parser.

**Option B — Sweeps (more robust, recommended if `.stab` columns differ).**
- AoA sweep: β=0, α = −4…+8° (say 7 points). Writes a `.polar` with CLtot, CDtot,
  Cmtot vs α. → CLα, Cmα by regression → SM, x_np, and the drag polar.
- Beta sweep: fixed α≈2°, β = −8…+8°. Gives Cn(β), Cl(β) → Cnβ, Clβ (lateral).

## Step 4 — parse and interpret
```
python3 ../scripts/parse_vspaero.py path/to/Kuma_V5B_vspaero.polar
python3 ../scripts/parse_vspaero.py path/to/Kuma_V5B_vspaero.stab
```
The parser prints the columns it detected (so you can confirm the format), the fitted
slopes, **static margin**, **neutral point**, and lateral derivatives, and compares to
the audit numbers. Results are written to `../data/vspaero_derivatives.csv`.

## What the answer means
- **SM > 0** (x_np aft of CG) = longitudinally stable. Audit predicted ~+8 %; a proper
  run near that validates the design. If VSPAERO gives **SM < 0**, the CG must move
  forward (battery forward) before flight.
- **Cnβ > 0** = directionally stable (weathercock). **Vv is only ~0.030** — expect a
  small Cnβ; the audit flags weak directional stability.
- **Clβ < 0** (with this sign convention) indicates a stabilising dihedral effect from
  the 7°. If |Clβ| is small, rudder-only roll control is even weaker than feared.
- VSPAERO is **inviscid + VLM** — it will **not** predict CLmax or stall. Use XFLR5 or
  experiment for CLmax; use VSPAERO for slopes/NP/derivatives.

## Limitations (state these in any report)
- VLM (no viscous drag, no separation) → CLα slightly high, CD optimistic.
- Simplified geometry (no fuselage camber/boattail detail, no camera/VTX, no prop).
- Propeller wash and pusher interference are **not** modelled.
