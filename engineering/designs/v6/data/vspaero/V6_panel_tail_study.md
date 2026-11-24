# V6 panel‑method + V‑tail study (VSPAERO, fuselage INCLUDED)

Method: VSPAERO **panel** (thick set = ALL, i.e. wing + V‑tail + fuselage pod), alpha sweep
(SM/NP) and beta sweep (Cnβ/Clβ), Xcg = 0.560 m, Sref 0.2275, cref 0.17619, Vinf 12 m/s.

| Config | tail span | dihedral | chords | **SM %MAC** | **x_np** | **Cnβ /rad** | **Clβ /rad** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **base (V6 as built)** | 0.270 | 45° | 200/150 | **−3.90** | 553.1 mm | **≈ 0.00** | 0.34 |
| vv1 | 0.300 | 45° | 220/160 | +1.42 | 562.5 mm | 0.041 | 0.37 |
| vv3 | 0.330 | 47° | 230/170 | **+2.72** | 564.8 mm | 0.077 | 0.41 |
| vv2 | 0.330 | 50° | 230/170 | −0.02 | 560.0 mm | **0.085** | 0.42 |

## Key findings
1. **The fuselage is the dominant destabiliser.** Wing+tail VLM (no body) gave SM **+8.3 %**;
   adding the fuselage (panel) drops it to **−3.9 %** at the same CG (560 mm). The body's
   Munk moment costs ≈ **12 % MAC of pitch margin** and ≈ **0.07 /rad of yaw stiffness**.
2. **At the current CG (30.7 % MAC) the aircraft is marginally UNSTABLE in pitch and
   essentially NEUTRAL in yaw** once the fuselage is modelled. The VLM‑only "+8 %" was
   optimistic; it is not a valid stability claim.
3. **Bigger tail helps both axes** (vv1→vv3 raise NP and Cnβ). **More dihedral** (vv2, 50°)
   buys more yaw (Cnβ 0.085) at the cost of pitch (Sh↓, NP forward). **vv3 (47°, big)** is the
   best compromise tested.

## To reach a healthy margin (+6…+8 % SM) the CG must move forward
`CG_target = x_np − 0.08·MAC` (MAC 176.19 → 14.1 mm):
| config | x_np | CG for +8 % SM | (%MAC) |
|---|---:|---:|---:|
| base | 553.1 | 539.0 mm | 17.9 % |
| vv1 | 562.5 | 548.4 mm | 23.2 % |
| vv3 | 564.8 | **550.7 mm** | **24.6 %** |
| vv2 | 560.0 | 545.9 mm | 21.8 % |

## Recommendation (V6.1)
- Enlarge the tail to ~**span 0.33 m, chords 0.23/0.17, dihedral ~47°** (vv3).
- Move CG forward to **~24–27 % MAC** (e.g. battery forward ~10 mm from the current 375 mm,
  to ≈365 mm, trim to CG≈555 mm) → SM ≈ **+5.6 %** with vv3.
- Accept **Cnβ ≈ 0.077 /rad** (still modest) and validate by flight; if spiral/gust behaviour
  is poor, add a small **ventral fin** or raise dihedral further (trading pitch), or lengthen
  the tail arm.
- Re‑run this study after the change and re‑verify CG with weighed mass.
