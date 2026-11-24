#!/usr/bin/env python3
"""
Build the V6 aero model in OpenVSP (Python API) and run a VSPAERO alpha sweep to
get CL_alpha / Cm_alpha (=> static margin / neutral point).
Run with OpenVSP's python packages on PYTHONPATH, e.g.:
  R=/Applications/OpenVSP.app/Contents/Resources/python
  PYTHONPATH=$R/openvsp:$R/degen_geom:$R/utilities python3 -u run_vspaero_v6.py
Outputs land in ./run/ (V6.vsp3, *.polar/.stab/.lod).
"""
import os
import openvsp as vsp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run")
os.makedirs(OUT, exist_ok=True)
os.chdir(OUT)

vsp.ClearVSPModel()

# ---- wing (NACA 2412 planform; VLM ignores section thickness) ----
w = vsp.AddGeom("WING", "")
vsp.SetGeomName(w, "wing")
vsp.SetParmVal(w, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
vsp.SetParmVal(w, "X_Rel_Location", "XForm", 0.496)
vsp.SetParmVal(w, "Z_Rel_Location", "XForm", 0.056)
vsp.SetDriverGroup(w, 1, vsp.SPAN_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER)
vsp.SetParmVal(w, "Root_Chord", "XSec_1", 0.200)
vsp.SetParmVal(w, "Tip_Chord", "XSec_1", 0.150)
vsp.SetParmVal(w, "Span", "XSec_1", 0.650)
vsp.SetParmVal(w, "Sweep", "XSec_1", 2.115)
vsp.SetParmVal(w, "Dihedral", "XSec_1", 7.0)

# ---- upright V-tail (V6: span 0.270, dihedral 45) ----
t = vsp.AddGeom("WING", "")
vsp.SetGeomName(t, "vtail")
vsp.SetParmVal(t, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
vsp.SetParmVal(t, "X_Rel_Location", "XForm", 0.770)
vsp.SetParmVal(t, "Y_Rel_Location", "XForm", 0.012)
vsp.SetParmVal(t, "Z_Rel_Location", "XForm", 0.026)
vsp.SetDriverGroup(t, 1, vsp.SPAN_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER)
vsp.SetParmVal(t, "Root_Chord", "XSec_1", 0.200)
vsp.SetParmVal(t, "Tip_Chord", "XSec_1", 0.150)
vsp.SetParmVal(t, "Span", "XSec_1", 0.270)
vsp.SetParmVal(t, "Sweep", "XSec_1", 4.289)
vsp.SetParmVal(t, "Dihedral", "XSec_1", 45.0)

# ---- fuselage pod ----
p = vsp.AddGeom("POD", "")
vsp.SetParmVal(p, "Length", "Design", 0.970)
vsp.SetParmVal(p, "FineRatio", "Design", 11.55)
vsp.Update()
vsp.WriteVSPFile(os.path.join(OUT, "V6.vsp3"))

# ---- VSPAERO alpha sweep ----
a = "VSPAEROSweep"
vsp.SetAnalysisInputDefaults(a)


def D(n, v):
    vsp.SetDoubleAnalysisInput(a, n, [v])


def I(n, v):
    vsp.SetIntAnalysisInput(a, n, [v])


D("Sref", 0.2275); D("bref", 1.30); D("cref", 0.17619)
D("Xcg", 0.560); D("Ycg", 0.0); D("Zcg", 0.0)
D("AlphaStart", -4.0); D("AlphaEnd", 8.0); D("AlphaNpts", 7)
D("BetaStart", 0.0); D("BetaEnd", 0.0); D("BetaNpts", 1)
D("MachStart", 0.035); D("MachEnd", 0.035); I("MachNpts", 1)
D("ReCref", 1.4e5); D("Vinf", 12.0)
I("GeomSet", vsp.SET_ALL)
try:
    vsp.SetVSPAERORefWingID(w)
except Exception as e:
    print("refwing note:", e)
vsp.Update()

try:
    rid = vsp.ExecAnalysis(a)
    print("ExecAnalysis returned:", str(rid)[:24])
except Exception as e:
    print("ExecAnalysis FAILED:", e)

print("FILES:", sorted(os.listdir(OUT)))
