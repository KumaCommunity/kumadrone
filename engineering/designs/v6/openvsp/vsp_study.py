#!/usr/bin/env python3
"""
Parametric VSPAERO study (panel method incl. fuselage) for V6.
Usage: python3 vsp_study.py <name> <tail_span> <tail_dihedral> <tail_rc> <tail_tc>
Runs a panel-method alpha sweep (SM/NP) + beta sweep (Cn_beta/Cl_beta) headlessly.
"""
import os
import subprocess
import sys
import glob

VSP = "/Applications/OpenVSP.app/Contents/Resources/vspscript"
AUD = "/Users/jacksonchandler/Downloads/Kuma_FPV_V5_Configuration_B_Engineering_Package/engineering/audits/v5-configuration-b/scripts"
sys.path.insert(0, AUD)
import parse_vspaero as p  # noqa
import numpy as np

TEMPLATE = r'''void main(){
 ClearVSPModel();
 string wing=AddGeom("WING",""); SetGeomName(wing,"wing");
 SetParmVal(wing,"Sym_Planar_Flag","Sym",SYM_XZ);
 SetParmVal(wing,"X_Rel_Location","XForm",0.496);
 SetParmVal(wing,"Z_Rel_Location","XForm",0.056);
 SetDriverGroup(wing,1,SPAN_WSECT_DRIVER,ROOTC_WSECT_DRIVER,TIPC_WSECT_DRIVER);
 SetParmVal(wing,"Root_Chord","XSec_1",0.200);
 SetParmVal(wing,"Tip_Chord","XSec_1",0.150);
 SetParmVal(wing,"Span","XSec_1",0.650);
 SetParmVal(wing,"Sweep","XSec_1",2.115);
 SetParmVal(wing,"Dihedral","XSec_1",7.0);
 string tail=AddGeom("WING",""); SetGeomName(tail,"vtail");
 SetParmVal(tail,"Sym_Planar_Flag","Sym",SYM_XZ);
 SetParmVal(tail,"X_Rel_Location","XForm",0.770);
 SetParmVal(tail,"Y_Rel_Location","XForm",0.012);
 SetParmVal(tail,"Z_Rel_Location","XForm",0.026);
 SetDriverGroup(tail,1,SPAN_WSECT_DRIVER,ROOTC_WSECT_DRIVER,TIPC_WSECT_DRIVER);
 SetParmVal(tail,"Root_Chord","XSec_1",@@RC@@);
 SetParmVal(tail,"Tip_Chord","XSec_1",@@TC@@);
 SetParmVal(tail,"Span","XSec_1",@@SPAN@@);
 SetParmVal(tail,"Sweep","XSec_1",4.289);
 SetParmVal(tail,"Dihedral","XSec_1",@@DIH@@);
 string pod=AddGeom("POD","");
 SetParmVal(pod,"Length","Design",0.970);
 SetParmVal(pod,"FineRatio","Design",11.55);
@@FIN@@
 Update();
 WriteVSPFile("V6_run.vsp3",SET_ALL);
 string cg="VSPAEROComputeGeometry"; SetAnalysisInputDefaults(cg);
 array<int> th; th.push_back(SET_TYPE::SET_ALL); SetIntAnalysisInput(cg,"GeomSet",th,0);
 array<int> ti; ti.push_back(SET_TYPE::SET_NONE); SetIntAnalysisInput(cg,"ThinGeomSet",ti,0);
 string cgr=ExecAnalysis(cg);
 string an="VSPAEROSweep"; SetAnalysisInputDefaults(an);
 array<int> gs; gs.push_back(0); SetIntAnalysisInput(an,"GeomSet",gs,0);
 array<int> rf; rf.push_back(1); SetIntAnalysisInput(an,"RefFlag",rf,0);
 array<string> wid; wid.push_back(wing); SetStringAnalysisInput(an,"WingID",wid,0);
 array<double> d(1,0.0);
 d[0]=0.2275; SetDoubleAnalysisInput(an,"Sref",d,0);
 d[0]=1.300; SetDoubleAnalysisInput(an,"bref",d,0);
 d[0]=0.17619; SetDoubleAnalysisInput(an,"cref",d,0);
 d[0]=0.560; SetDoubleAnalysisInput(an,"Xcg",d,0);
 d[0]=0.0; SetDoubleAnalysisInput(an,"Ycg",d,0);
 d[0]=0.0; SetDoubleAnalysisInput(an,"Zcg",d,0);
 d[0]=@@ASTART@@; SetDoubleAnalysisInput(an,"AlphaStart",d,0);
 d[0]=@@AEND@@; SetDoubleAnalysisInput(an,"AlphaEnd",d,0);
 d[0]=@@BSTART@@; SetDoubleAnalysisInput(an,"BetaStart",d,0);
 d[0]=@@BEND@@; SetDoubleAnalysisInput(an,"BetaEnd",d,0);
 d[0]=0.035; SetDoubleAnalysisInput(an,"MachStart",d,0);
 d[0]=0.035; SetDoubleAnalysisInput(an,"MachEnd",d,0);
 d[0]=1.4e5; SetDoubleAnalysisInput(an,"ReCref",d,0);
 d[0]=12.0; SetDoubleAnalysisInput(an,"Vinf",d,0);
 array<int> n(1,@@ANPTS@@); SetIntAnalysisInput(an,"AlphaNpts",n,0);
 n[0]=@@BNPTS@@; SetIntAnalysisInput(an,"BetaNpts",n,0);
 n[0]=1; SetIntAnalysisInput(an,"MachNpts",n,0);
 string rid=ExecAnalysis(an);
 while(GetNumTotalErrors()>0){ ErrorObj e=PopLastError(); Print(e.GetErrorString()); }
 Print("done");
}
'''


FIN_CODE = '''// ventral fin (vertical surface below rear fuselage) for yaw stiffness
 string fin=AddGeom("WING",""); SetGeomName(fin,"ventral");
 SetParmVal(fin,"Sym_Planar_Flag","Sym",SYM_XZ);
 SetDriverGroup(fin,1,SPAN_WSECT_DRIVER,ROOTC_WSECT_DRIVER,TIPC_WSECT_DRIVER);
 SetParmVal(fin,"Root_Chord","XSec_1",0.140);
 SetParmVal(fin,"Tip_Chord","XSec_1",0.080);
 SetParmVal(fin,"Span","XSec_1",0.120);
 SetParmVal(fin,"Sweep","XSec_1",20.0);
 SetParmVal(fin,"Dihedral","XSec_1",-90.0);
 SetParmVal(fin,"X_Rel_Location","XForm",0.800);
 SetParmVal(fin,"Z_Rel_Location","XForm",-0.020);
'''


def gen(path, span, dih, rc, tc, astart, aend, anpts, bstart, bend, bnpts, fin=0):
    s = TEMPLATE
    s = s.replace("@@FIN@@", FIN_CODE if fin else "")
    for k, v in [("@@SPAN@@", span), ("@@DIH@@", dih), ("@@RC@@", rc), ("@@TC@@", tc),
                 ("@@ASTART@@", astart), ("@@AEND@@", aend), ("@@ANPTS@@", anpts),
                 ("@@BSTART@@", bstart), ("@@BEND@@", bend), ("@@BNPTS@@", bnpts)]:
        s = s.replace(k, str(v))
    with open(path, "w") as fh:
        fh.write(s)


def run(workdir, script):
    os.makedirs(workdir, exist_ok=True)
    subprocess.run([VSP, "-script", script], cwd=workdir,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pol = glob.glob(os.path.join(workdir, "*.polar"))
    return pol[0] if pol else None


def slope(x, y):
    return float(np.polyfit(x, y, 1)[0]) if len(set(x)) > 1 else float("nan")


def main():
    name, span, dih, rc, tc = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    fin = int(sys.argv[6]) if len(sys.argv) > 6 else 0
    os.makedirs("/tmp/vspstudy", exist_ok=True)
    base = "/tmp/vspstudy/" + name
    sa = base + "_alpha.vspscript"; gen(sa, span, dih, rc, tc, -4, 8, 7, 0, 0, 1, fin)
    sb = base + "_beta.vspscript";  gen(sb, span, dih, rc, tc, 2, 2, 1, -8, 8, 5, fin)
    pa = run(base + "_a", sa); pb = run(base + "_b", sb)
    out = dict(name=name, span=span, dih=dih, rc=rc, tc=tc)
    if pa:
        hdr, rows = p.read_table(pa)
        i_a=p.col(hdr,'aoa'); i_cl=p.col(hdr,'cltot'); i_cm=p.col(hdr,'cmytot')
        A=[r[i_a] for r in rows]; cla=slope(A,[r[i_cl] for r in rows]); cma=slope(A,[r[i_cm] for r in rows])
        out['CLa']=round(cla,5); out['Cma']=round(cma,5)
        sm=-cma/cla; out['SM_pct']=round(sm*100,2); out['x_np_mm']=round(560+sm*176.19,1)
    if pb:
        hdr, rows = p.read_table(pb)
        i_b=p.col(hdr,'beta'); i_cmx=p.col(hdr,'cmxtot'); i_cmz=p.col(hdr,'cmztot')
        B=[r[i_b] for r in rows]
        out['Cnb_rad']=round(slope(B,[r[i_cmz] for r in rows])*57.2958,4)
        out['Clb_rad']=round(slope(B,[r[i_cmx] for r in rows])*57.2958,4)
    print("RESULT", out)


if __name__ == "__main__":
    main()
