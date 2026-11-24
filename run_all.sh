#!/usr/bin/env bash
# One-command pipeline for the Kuma FPV project.
#   ./run_all.sh            # validate + calcs + export STLs + renders + poster
#   ./run_all.sh all        # same
#   ./run_all.sh validate   # just the validation suite
#   ./run_all.sh vspaero    # build+run VSPAERO via vspscript (needs OpenVSP.app)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PY="${PYTHON:-python3}"
SCAD="engineering/designs/v6/Kuma_FPV_V6_Configuration_B.scad"
STL="engineering/designs/v6/STL"
VSP="engineering/designs/v6/openvsp"
R="/Applications/OpenVSP.app/Contents/Resources"

PARTS="fuselage_0 fuselage_1 fuselage_2 fuselage_3 fuselage_4 fuselage_5 \
coupler_0 coupler_1 coupler_2 coupler_3 coupler_4 wing_center \
wing_R1 wing_R2 wing_R3 wing_L1 wing_L2 wing_L3 wing_key tail_R tail_L \
ruddervator_R ruddervator_L tail_saddle tail_shoe_R tail_shoe_L saddle_plate \
camera_plate camera_cradle dorsal_fairing battery_tray forward_equipment_tray \
secured_tray battery_hatch_lid motor_bulkhead wing_saddle_clamp \
centre_spar_joiner wing_center_spar_sleeve control_horn_R control_horn_L \
ruddervator_hinge_R ruddervator_hinge_L insert_fit_coupon"

stage(){ printf '\n=== %s ===\n' "$*"; }

validate(){ stage validate; "$PY" engineering/tools/run_validation.py; }

calcs(){
  stage "calcs (audit + V6)"
  "$PY" engineering/audits/v5-configuration-b/scripts/audit_calcs.py >/dev/null
  "$PY" engineering/audits/v5-configuration-b/scripts/launch_lateral.py >/dev/null
  "$PY" engineering/designs/v6/scripts/v6_calcs.py
  "$PY" engineering/designs/v6/scripts/v6_mass_range.py
}

export_stl(){
  stage "export STLs"
  if ! command -v openscad >/dev/null 2>&1; then echo "openscad not found; skip"; return; fi
  mkdir -p "$STL"
  for p in $PARTS; do
    openscad -D "part=\"$p\"" -o "$STL/$p.stl" "$SCAD" >/dev/null 2>&1 || echo "  FAIL $p"
  done
  echo "exported $(ls "$STL"/*.stl | wc -l | tr -d ' ') parts"
}

render(){
  stage "renders + poster"
  for v in top side front rear; do "$PY" engineering/designs/v6/scripts/plot_ortho.py "$v" >/dev/null; done
  "$PY" engineering/designs/v6/scripts/render_dark.py >/dev/null
  "$PY" engineering/designs/v6/scripts/make_poster.py
}

vspaero(){
  stage "VSPAERO (headless via vspscript)"
  if [ ! -x "$R/vspscript" ]; then echo "OpenVSP vspscript not found at $R; skip"; return; fi
  mkdir -p build/vsp_a build/vsp_b
  ( cd build/vsp_a && "$R/vspscript" -script "$ROOT/$VSP/Kuma_V6_vspaero_run.vspscript" >/dev/null )
  ( cd build/vsp_b && "$R/vspscript" -script "$ROOT/$VSP/Kuma_V6_vspaero_beta.vspscript" >/dev/null )
  "$PY" engineering/audits/v5-configuration-b/scripts/parse_vspaero.py build/vsp_a/V6_run.polar 0.560 || true
}

case "${1:-all}" in
  validate) validate ;;
  calcs)    calcs ;;
  export)   export_stl ;;
  render)   render ;;
  vspaero)  vspaero ;;
  all)      validate; calcs; export_stl; render; stage done ;;
  *) echo "usage: ./run_all.sh [all|validate|calcs|export|render|vspaero]"; exit 1 ;;
esac
