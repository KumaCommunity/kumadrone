#!/usr/bin/env python3
"""Render V6 views as clean silver-on-transparent PNGs for the poster.
Views: hero (iso), front, side, top, rear, exploded. Fast 2-D projection."""
import os, glob, io
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import trimesh
from PIL import Image

HERE = os.path.dirname(__file__)
STL = os.path.join(HERE, "..", "STL")
GDIR = os.path.join(HERE, "..", "graphics")
CACHE = "/tmp/v6_tris.npz"
EXCLUDE = {"forward_equipment_tray", "insert_fit_coupon", "camera_plate", "dorsal_fairing"}
PETG_PARTS = {"coupler_0","coupler_1","coupler_2","coupler_3","coupler_4","wing_key",
  "tail_saddle","tail_shoe_R","tail_shoe_L","saddle_plate","camera_cradle","secured_tray",
  "motor_bulkhead","centre_spar_joiner","wing_center_spar_sleeve","control_horn_R",
  "control_horn_L","ruddervator_hinge_R","ruddervator_hinge_L"}
SILVER = np.array([0.86, 0.88, 0.90])
PETG   = np.array([0.55, 0.62, 0.70])


def basis(e):
    e = e / np.linalg.norm(e)
    up = np.array([0, 0, 1.0])
    if abs(e @ up) > 0.98:
        up = np.array([0, 1.0, 0])
    u = np.cross(up, e); u /= np.linalg.norm(u)
    v = np.cross(e, u); v /= np.linalg.norm(v)
    return e, u, v


def render(T, M, e, path, px=1500, pad=0.05):
    e, u, v = basis(e)
    n = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    nl = np.linalg.norm(n, axis=1); nl[nl == 0] = 1; n /= nl[:, None]
    f = n @ e
    keep = f > 0.02
    T, M, f = T[keep], M[keep], f[keep]
    P = np.einsum("nij,j->ni", T, u); Q = np.einsum("nij,j->ni", T, v)
    verts = np.stack([P, Q], 2)
    depth = (T.mean(1) @ e)
    o = np.argsort(depth); verts, M, f = verts[o], M[o], f[o]
    shade = 0.35 + 0.65 * np.clip(f, 0, 1)
    base = np.where(M[:, None] == 1, PETG[None, :], SILVER[None, :])
    cols = np.clip(base * shade[:, None], 0, 1)
    xmin, xmax = P.min(), P.max(); ymin, ymax = Q.min(), Q.max()
    mx = pad * max(xmax - xmin, ymax - ymin)
    fig, ax = plt.subplots(figsize=(px / 150, px / 150 * (ymax - ymin + 2 * mx) / (xmax - xmin + 2 * mx) + 1e-6))
    ax.add_collection(PolyCollection(verts, facecolors=cols, edgecolors="none"))
    ax.set_xlim(xmin - mx, xmax + mx); ax.set_ylim(ymin - mx, ymax + mx)
    ax.set_aspect("equal"); ax.axis("off")
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)
    fig.savefig(path, transparent=True, dpi=170, bbox_inches="tight", pad_inches=0.01)
    plt.close(fig)
    print("rendered", os.path.basename(path))


def load_cache():
    if os.path.exists(CACHE):
        d = np.load(CACHE); return d["tris"].astype(float), d["mats"]
    T, M = [], []
    for fn in sorted(glob.glob(os.path.join(STL, "*.stl"))):
        nm = os.path.splitext(os.path.basename(fn))[0]
        if nm in EXCLUDE: continue
        t = np.asarray(trimesh.load(fn, force="mesh").triangles, float)
        T.append(t); M.append(np.full(len(t), 1 if nm in PETG_PARTS else 0))
    T = np.concatenate(T); M = np.concatenate(M)
    np.savez_compressed(CACHE, tris=T.astype(np.float32), mats=M.astype(np.int8))
    return T, M


def load_exploded(k=1.6):
    T, M = [], []
    allv = []
    parts = []
    for fn in sorted(glob.glob(os.path.join(STL, "*.stl"))):
        nm = os.path.splitext(os.path.basename(fn))[0]
        if nm in EXCLUDE: continue
        m = trimesh.load(fn, force="mesh")
        t = np.asarray(m.triangles, float)
        if len(t) == 0: continue
        c = t.reshape(-1, 3).mean(0)
        parts.append((t, c, 1 if nm in PETG_PARTS else 0)); allv.append(t.reshape(-1, 3))
    g = np.concatenate(allv).mean(0)
    for t, c, mat in parts:
        off = k * (c - g)
        T.append(t + off); M.append(np.full(len(t), mat))
    return np.concatenate(T), np.concatenate(M)


def main():
    os.makedirs(GDIR, exist_ok=True)
    T, M = load_cache()
    render(T, M, np.array([-1.0, -1.05, 0.62]), os.path.join(GDIR, "v6d_hero.png"), px=1700)
    render(T, M, np.array([0, 0, 1.0]), os.path.join(GDIR, "v6d_top.png"))
    render(T, M, np.array([-1.0, 0, 0]), os.path.join(GDIR, "v6d_front.png"))
    render(T, M, np.array([0, 1.0, 0]), os.path.join(GDIR, "v6d_side.png"))
    render(T, M, np.array([1.0, 0, 0]), os.path.join(GDIR, "v6d_rear.png"))
    Te, Me = load_exploded()
    render(Te, Me, np.array([-1.0, -1.05, 0.62]), os.path.join(GDIR, "v6d_exploded.png"), px=1700)


if __name__ == "__main__":
    main()
