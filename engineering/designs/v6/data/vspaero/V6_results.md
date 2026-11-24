# V6 VSPAERO results (headless via OpenVSP 7.2.2 / vspscript)

Model: wing (NACA planform) + upright V-tail (V6: span 0.270 m, dihedral 45°). **Fuselage
pod excluded from the VLM** (a thin-tessellated body corrupts the forces). VLM is
camberless/inviscid → CL0 = 0; fuselage drag/contribution not captured.

## Alpha sweep (x_ref = moment centre = 0.560 m)
| AoA | CL | CMytot (pitch) |
|---:|---:|---:|
| -4 | -0.380 | +0.0285 |
| -2 | -0.190 | +0.0259 |
| 0 | 0.000 | +0.0179 |
| 2 | +0.191 | +0.0047 |
| 4 | +0.382 | -0.0138 |
| 6 | +0.572 | -0.0376 |
| 8 | +0.761 | -0.0663 |

- CLα = **0.0951 /deg** (5.45 /rad)
- Cmα = **−0.0079 /deg** (pitch-stable)
- **Static margin = −Cmα/CLα = +8.31 % MAC**
- **Neutral point x_np = 574.6 mm** (from Xcg=560)
- Analytical audit predicted SM +7.8 %, x_np 573.8 mm → **confirmed.**

## Beta sweep (AoA = 2°)
| Beta | CMx (roll) | CMz (yaw) |
|---:|---:|---:|
| -8 | -0.0296 | +0.0104 |
| -4 | -0.0151 | +0.0052 |
| 0 | 0.000 | 0.000 |
| +4 | +0.0151 | -0.0052 |
| +8 | +0.0296 | -0.0104 |

- **Cnβ ≈ −0.0013 /deg = −0.075 /rad** → directionally stable in sign but **weak**
  (typical good values 0.10–0.20 /rad; fuselage would reduce it further) → confirms the
  weak-directional / spiral-tendency concern (I‑06, low Vv).
- **Clβ ≈ +0.0037 /deg = +0.213 /rad** → **strong dihedral effect** (better than the
  audit's 0.08–0.16 estimate), so rudder→sideslip→roll coupling is likely **adequate**;
  the limiting factor is weak yaw stiffness, not roll authority. (Signs per VSPAERO axes;
  confirm in GUI.)
- Net: rear-only control is more plausible than the analytical screen suggested for ROLL,
  but directional stiffness is marginal → flight-test with care; consider more Vv if
  spiral/gust behaviour is poor.

## Reproduce
```
R=/Applications/OpenVSP.app/Contents/Resources
PYTHONPATH=$R/python/openvsp:$R/python/degen_geom:$R/python/utilities \
  $R/vspscript -script engineering/designs/v6/openvsp/Kuma_V6_vspaero_run.vspscript   # alpha
  $R/vspscript -script engineering/designs/v6/openvsp/Kuma_V6_vspaero_beta.vspscript  # beta
python3 engineering/audits/v5-configuration-b/scripts/parse_vspaero.py <out>.polar 0.560
```
