"""Run body-inclusive VSPAERO pitch and sideslip screens with and without the dorsal fin."""
import argparse
import csv
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TEMPLATE = (HERE / "panel_template.vspscript").read_text()
FIN = """ string fin=AddGeom("WING","");
 SetGeomName(fin,"dorsal_fin");
 SetParmVal(fin,"Sym_Planar_Flag","Sym",0);
 SetParmVal(fin,"X_Rel_Location","XForm",0.788);
 SetParmVal(fin,"Z_Rel_Location","XForm",0.033);
 SetParmVal(fin,"X_Rel_Rotation","XForm",90.0);
 SetDriverGroup(fin,1,SPAN_WSECT_DRIVER,ROOTC_WSECT_DRIVER,TIPC_WSECT_DRIVER);
 SetParmVal(fin,"Root_Chord","XSec_1",0.125);
 SetParmVal(fin,"Tip_Chord","XSec_1",0.065);
 SetParmVal(fin,"Span","XSec_1",0.074);
 SetParmVal(fin,"Sweep","XSec_1",24.68);
 SetParmVal(fin,"Dihedral","XSec_1",0.0);
"""


def run_case(executable, out, name, fin, sweep):
    directory = out / name
    directory.mkdir(parents=True, exist_ok=False)
    values = dict(zip(("ALPHA_START", "ALPHA_END", "ALPHA_N", "BETA_START", "BETA_END", "BETA_N"), sweep))
    script = TEMPLATE.replace("@@FIN@@", FIN if fin else "")
    for key, val in values.items():
        script = script.replace(f"@@{key}@@", str(val))
    script_path = directory / "case.vspscript"
    script_path.write_text(script)
    with (directory / "solver.log").open("w") as log:
        subprocess.run([executable, "-script", str(script_path)], cwd=directory, stdout=log,
                       stderr=subprocess.STDOUT, check=True)
    key = (directory / "V6_run.vkey").read_text()
    if ("dorsal_fin_S" in key) != fin:
        raise RuntimeError(f"{name} did not match requested solver geometry")
    lines = (directory / "V6_run.polar").read_text().splitlines()
    header_idx = next(i for i, line in enumerate(lines) if line.split()[:3] == ["Beta", "Mach", "AoA"])
    labels = lines[header_idx].split()
    rows = np.array([[float(x) for x in line.split()] for line in lines[header_idx+1:] if line.strip()])
    if len(rows) != max(sweep[2], sweep[5]) or not np.isfinite(rows).all():
        raise RuntimeError(f"{name} sweep incomplete")
    result = {"configuration": name, "samples": len(rows), "x_np_mm": "", "cmz_beta_per_rad": ""}
    if sweep[2] > 1:
        alpha = rows[:, labels.index("AoA")]
        cl_slope = np.polyfit(alpha, rows[:, labels.index("CLtot")], 1)[0]
        cm_slope = np.polyfit(alpha, rows[:, labels.index("CMytot")], 1)[0]
        inputs = (directory / "V6_run.vspaero").read_text()
        chord = float(re.search(r"^Cref\s*=\s*([.0-9e+-]+)", inputs, re.M)[1])
        result["x_np_mm"] = round(560 - 1000 * chord * cm_slope / cl_slope, 2)
    else:
        beta = np.radians(rows[:, labels.index("Beta")])
        result["cmz_beta_per_rad"] = round(np.polyfit(beta, rows[:, labels.index("CMztot")], 1)[0], 5)
    print(result, flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vspscript", default="/Applications/OpenVSP.app/Contents/Resources/vspscript")
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    results_path = args.out.resolve()
    results_path.mkdir(parents=True, exist_ok=True)
    cases = [(f"{config}_alpha", fin, (-4, 8, 7, 0, 0, 1))
             for config, fin in (("base", False), ("fin", True))]
    cases += [(f"{config}_beta{alpha}", fin, (alpha, alpha, 1, -6, 6, 5))
              for config, fin in (("base", False), ("fin", True)) for alpha in (2, 6)]
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(lambda case: run_case(args.vspscript, results_path, *case), cases))
    with (results_path / "results.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=results[0])
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
