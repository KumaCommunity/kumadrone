#!/usr/bin/env python3
"""
Best-effort VSPAERO runner via the OpenVSP Python API.

REQUIRES the `openvsp` Python package (ships with the OpenVSP install) on PYTHONPATH.
Parameter/analysis names follow the VSPAERO API but VARY by OpenVSP version — if a
call errors, use the GUI workflow in README.md (authoritative) and then run
parse_vspaero.py on the output. This script was NOT executed in the audit
environment (OpenVSP absent there).

    python3 run_vspaero.py                 # reads Kuma_V5B_vspaero.vsp3
    python3 run_vspaero.py model.vsp3
"""
import os
import sys


def main():
    try:
        import openvsp as vsp
    except Exception as exc:  # noqa
        raise SystemExit(
            "OpenVSP Python API not importable (%s).\n"
            "Set PYTHONPATH to your OpenVSP install, or use the GUI workflow in "
            "openvsp/README.md." % exc)

    model = sys.argv[1] if len(sys.argv) > 1 else "Kuma_V5B_vspaero.vsp3"
    if not os.path.exists(model):
        raise SystemExit(f"Model not found: {model}. Run Kuma_V5B_vspaero.vspscript first.")

    vsp.ReadVSPFile(model)

    # --- configure a VSPAERO sweep (AoA) + beta sweep for lateral derivatives ---
    analysis = "VSPAEROSweep"
    vsp.SetAnalysisInputDefaults(analysis)

    def dset(name, val):
        vsp.SetDoubleAnalysisInput(analysis, name, [val])

    def iset(name, val):
        vsp.SetIntAnalysisInput(analysis, name, [val])

    # reference values (must match CAD)
    dset("Sref", 0.2275)
    dset("bref", 1.300)
    dset("cref", 0.176)      # 0.17619 rounded by some APIs; set 0.17619 if accepted
    # moment reference = CG (NP measured from here)
    dset("Xcg", 0.560)
    dset("Ycg", 0.0)
    dset("Zcg", 0.0)

    # AoA sweep at low Mach, representative Re
    dset("MachStart", 0.035)
    dset("MachEnd", 0.035)
    iset("MachNpts", 1)
    dset("AlphaStart", -4.0)
    dset("AlphaEnd", 8.0)
    iset("AlphaNpts", 7)
    # beta sweep for Cn_beta / Cl_beta
    dset("BetaStart", -8.0)
    dset("BetaEnd", 8.0)
    iset("BetaNpts", 5)
    dset("ReCref", 1.4e5)

    print("Running VSPAERO sweep ... (outputs .polar/.stab/.lod in the working dir)")
    try:
        vsp.ExecAnalysis(analysis)
    except Exception as exc:  # noqa
        raise SystemExit(
            "VSPAERO run failed (%s). API names may differ in your version.\n"
            "Use the GUI workflow in openvsp/README.md instead." % exc)

    print("Done. Now run:  python3 ../scripts/parse_vspaero.py <output>.polar 0.560")


if __name__ == "__main__":
    main()
