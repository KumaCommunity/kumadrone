#!/usr/bin/env python3
"""Split multi-body STLs and report each sub-body volume + bbox to determine
whether internal stiffeners are fused to the skin or floating/disconnected."""
import os
import trimesh

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PARTS = ["wing_L1", "wing_R1", "wing_L2", "wing_center", "tail_L",
         "ruddervator_L"]


def main():
    for name in PARTS:
        path = os.path.join(ROOT, "STL", name + ".stl")
        m = trimesh.load(path, force="mesh")
        parts = m.split(only_watertight=False)
        parts = sorted(parts, key=lambda p: -abs(p.volume))
        print(f"\n=== {name}: {len(parts)} bodies, total |V|="
              f"{abs(m.volume)/1000:.3f} cm3 ===")
        for i, p in enumerate(parts):
            b = p.bounds
            dims = b[1] - b[0]
            print(f"  body {i}: vol={abs(p.volume)/1000:8.3f} cm3  "
                  f"dims={dims[0]:6.1f}x{dims[1]:6.1f}x{dims[2]:5.1f} mm  "
                  f"centroid=({p.centroid[0]:.0f},{p.centroid[1]:.0f},{p.centroid[2]:.0f})")


if __name__ == "__main__":
    main()
