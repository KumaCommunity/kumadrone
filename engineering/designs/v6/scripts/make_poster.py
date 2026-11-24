#!/usr/bin/env python3
"""Compose a stylized 'concept poster' (V6) from the dark renders + text."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(__file__)
G = os.path.join(HERE, "..", "graphics")
F = "/System/Library/Fonts/Supplemental/"

BG = (16, 20, 25)
PANEL = (22, 27, 33)
BORDER = (46, 54, 64)
ACCENT = (242, 169, 0)
WHITE = (236, 239, 243)
STEEL = (198, 206, 214)
GREY = (146, 156, 168)


def font(name, size):
    return ImageFont.truetype(F + name, size)


FB = font("Arial Bold.ttf", 10); FR = font("Arial.ttf", 10)
FBLACK = font("Arial Black.ttf", 10)


def f(setname, size):
    return font(setname, size)


def img(name):
    return Image.open(os.path.join(G, name)).convert("RGBA")


def paste_fit(base, im, box):
    x, y, w, h = box
    r = min(w / im.width, h / im.height)
    nw, nh = max(1, int(im.width * r)), max(1, int(im.height * r))
    im2 = im.resize((nw, nh), Image.LANCZOS)
    base.alpha_composite(im2, (x + (w - nw) // 2, y + (h - nh) // 2))


def panel(d, box, title=None, tfont=None):
    x, y, w, h = box
    d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL, outline=BORDER, width=2)
    if title:
        d.rectangle([x, y, x + 6, y + 34], fill=ACCENT)
        d.text((x + 16, y + 6), title, font=tfont, fill=WHITE)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def bullets(d, x, y, items, fnt, fill=STEEL, lh=30, maxw=600, dot=ACCENT):
    for it in items:
        d.ellipse([x, y + 10, x + 8, y + 18], fill=dot)
        for ln in wrap(d, it, fnt, maxw - 24):
            d.text((x + 20, y), ln, font=fnt, fill=fill)
            y += lh
        y += 6
    return y



FTITLE = font("Arial Black.ttf", 96)
FSUB40 = font("Arial.ttf", 40)
FSUB28 = font("Arial.ttf", 28)
FSUB24 = font("Arial.ttf", 24)
FBIG = font("Arial Bold.ttf", 30)
FSUB = font("Arial.ttf", 22)
FPT = font("Arial Bold.ttf", 28)
FSCAP = font("Arial.ttf", 24)
FTBL = font("Arial Bold.ttf", 26)
FCELL = font("Arial.ttf", 25)
FBUL = font("Arial.ttf", 25)


def draw_feature(d, x, y, kind, label, sub):
    s = 58
    box = [x, y, x + s, y + s]
    d.rounded_rectangle(box, radius=8, outline=STEEL, width=2)
    cx, cy = x + s / 2, y + s / 2
    if kind == "cam":
        d.rounded_rectangle([x + 9, y + 16, x + s - 9, y + s - 16], radius=4, outline=STEEL, width=2)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=STEEL, width=2)
    elif kind == "wing":
        d.line([x + 8, y + s - 16, x + s - 8, y + s - 16], fill=STEEL, width=2)
        d.polygon([(x + 8, y + s - 16), (cx, y + 16), (x + s - 8, y + s - 16)], outline=STEEL, width=2)
    elif kind == "v":
        d.line([x + 14, y + 16, cx, y + s - 14], fill=STEEL, width=3)
        d.line([x + s - 14, y + 16, cx, y + s - 14], fill=STEEL, width=3)
    elif kind == "mod":
        for i in range(3):
            d.rectangle([x + 12 + i * 11, y + 18, x + 22 + i * 11, y + s - 18], outline=STEEL, width=2)
    else:
        for i in range(3):
            yy = y + 18 + i * 9
            d.line([x + 10, yy, x + s - 10, yy], fill=STEEL, width=2)
    d.text((x + s + 18, y - 2), label, font=FBIG, fill=WHITE)
    d.text((x + s + 18, y + 30), sub, font=FSUB, fill=GREY)


def main():
    W, H = 3400, 2000
    canvas = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(canvas)

    d.rectangle([48, 44, 62, 196], fill=ACCENT)
    d.text((80, 22), "KUMA FPV V6", font=FTITLE, fill=WHITE)
    d.text((84, 138), "Modular Fixed-Wing RC Aircraft", font=FSUB40, fill=STEEL)
    d.text((86, 190), "Configuration B   \u2022   3D-Printed Hobby Aircraft Concept", font=FSUB28, fill=GREY)

    paste_fit(canvas, img("v6d_hero.png"), (1110, 40, 2260, 830))

    bx, by, bw, bh = 2740, 70, 620, 104
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=12, fill=(20, 24, 29), outline=ACCENT, width=3)
    d.text((bx + 24, by + 12), "CONCEPT", font=FSUB40, fill=ACCENT)
    d.text((bx + 24, by + 62), "NOT FLIGHT VALIDATED", font=FSUB24, fill=STEEL)

    feats = [
        ("cam", "Nose FPV Camera", "Forward-facing nano FPV camera in nose cone"),
        ("wing", "High-Mounted Fixed Wing", "No ailerons; 7 deg dihedral"),
        ("v", "Upright V-Tail", "Two ruddervators (pitch & yaw)"),
        ("mod", "Modular & Secured", "Bolt-together sections, hatches, secure tray"),
        ("lay", "3D-Printed", "LW-PLA shell, PETG hardpoints, M3/M4"),
    ]
    y = 300
    for k, lab, sub in feats:
        draw_feature(d, 52, y, k, lab, sub)
        y += 122

    labels = [
        ("v6d_side.png", "Side View", "Fuselage: 970 mm"),
        ("v6d_front.png", "Front View", "Span: 1,300 mm  \u2022  dihedral 7 deg"),
        ("v6d_top.png", "Top View", "Wing 200->150 mm  \u2022  V-tail 270 mm @45"),
        ("v6d_rear.png", "Rear View", "Pusher prop  \u2022  dia 150 mm"),
    ]
    vw, vh, gap, vy = 790, 360, 22, 895
    x = 52
    for fn, title, cap in labels:
        panel(d, (x, vy, vw, vh), title, FPT)
        paste_fit(canvas, img(fn), (x + 12, vy + 40, vw - 24, vh - 78))
        d.text((x + 16, vy + vh - 32), cap, font=FSCAP, fill=STEEL)
        x += vw + gap
    draw_bottom(d, canvas)
    canvas.save(os.path.join(G, "v6_poster.png"))


def draw_internal(d, box):
    x, y, w, h = box
    yb = y + int(h * 0.46)
    ph = 96
    x0, x1 = x + 16, x + w - 16
    d.rounded_rectangle([x0, yb - ph // 2, x1, yb + ph // 2], radius=34, outline=STEEL, width=2)
    for fr in (0.18, 0.36, 0.54, 0.72, 0.88):
        xx = x0 + fr * (x1 - x0)
        d.line([xx, yb - ph // 2, xx, yb + ph // 2], fill=BORDER, width=2)
    blocks = [
        (0.05, 0.13, (60, 70, 84), "Camera"),
        (0.19, 0.37, (46, 120, 90), "Equipment Bay"),
        (0.42, 0.58, (200, 150, 40), "Battery"),
        (0.61, 0.70, (52, 96, 150), "RX"),
        (0.80, 0.87, (40, 70, 120), "Motor"),
    ]
    bh = ph - 20
    for i, (f0, f1, col, lab) in enumerate(blocks):
        bx0 = x0 + f0 * (x1 - x0); bx1 = x0 + f1 * (x1 - x0)
        d.rounded_rectangle([bx0, yb - bh // 2, bx1, yb + bh // 2], radius=6, fill=col, outline=STEEL, width=1)
        lx = (bx0 + bx1) / 2
        ly = yb - ph // 2 - 36 - (30 if i % 2 else 0)
        d.line([lx, yb - ph // 2 - 4, lx, ly + 26], fill=ACCENT, width=2)
        tw = d.textlength(lab, font=FSUB24)
        d.text((lx - tw / 2, ly), lab, font=FSUB24, fill=STEEL)
    d.text((x0, yb + ph // 2 + 40),
           "Schematic only \u2014 stations approximate (see mass/CG data)",
           font=FSUB24, fill=GREY)


def draw_bottom(d, canvas):
    y0, h = 1290, 680
    boxes = [(40, 720), (778, 720), (1516, 600), (2134, 560), (2712, 600)]
    titles = ["Internal Layout (Concept)", "Exploded Assembly (Modular)",
              "Configuration B / Construction", "Preliminary Geometry", "Engineer Review"]
    for (x, w), t in zip(boxes, titles):
        panel(d, (x, y0, w, h), t, FPT)

    # internal layout schematic
    draw_internal(d, (56, y0 + 60, 688, 540))

    # exploded image
    paste_fit(canvas, img("v6d_exploded.png"), (778 + 14, y0 + 48, 720 - 28, h - 70))

    # config + construction bullets
    x = 1516 + 20
    yy = y0 + 50
    d.text((x, yy), "Configuration B", font=FTBL, fill=ACCENT); yy += 40
    yy = bullets(d, x, yy, ["Fixed, high-mounted wing", "No ailerons (ruddervator-only)",
                            "Upright V-tail (2 ruddervators)", "Rear pusher propeller",
                            "Modular, 3D-printed airframe"],
                 FBUL, maxw=560, lh=32)
    yy += 6
    d.text((x, yy), "Construction", font=FTBL, fill=ACCENT); yy += 40
    bullets(d, x, yy, ["LW-PLA printed shell", "PETG hardpoints, hatches, trays",
                       "M3/M4 heat-set inserts", "Removable wing & V-tail",
                       "Secured battery / equipment tray"], FBUL, maxw=560, lh=32)

    # geometry table
    x = 2134 + 18; yy = y0 + 52
    rows = [("Wingspan", "1,300 mm"), ("Fuselage", "970 mm"), ("Wing area", "0.2275 m\u00b2"),
            ("Aspect ratio", "7.43"), ("Wing airfoil", "NACA 2412"), ("Tail airfoil", "NACA 0010"),
            ("Wing dihedral", "7\u00b0 / side"), ("V-tail", "270 mm @ 45\u00b0"),
            ("Empty mass", "~1.35 kg"), ("Static margin", "+2.7 % (panel)*")]
    for lab, val in rows:
        d.text((x, yy), lab, font=FCELL, fill=GREY)
        tw = d.textlength(val, font=FCELL)
        d.text((x + 560 - 30 - tw, yy), val, font=FCELL, fill=WHITE)
        d.line([x, yy + 30, x + 560 - 24, yy + 30], fill=BORDER, width=1)
        yy += 40

    # review / notes
    x = 2712 + 20; yy = y0 + 50
    d.text((x, yy), "Key notes", font=FTBL, fill=ACCENT); yy += 40
    bullets(d, x, yy, ["Mass ~1.35 kg empty; +500 g \u2248 1.85 kg",
                       "VSPAERO panel (incl. fuselage): pitch margin thin \u2014 move CG forward",
                       "Rudder-only lateral control \u2014 flight test required",
                       "Concept only: not flight validated"],
            FBUL, maxw=560, lh=32)
    yy = y0 + h - 120
    d.text((x, yy), "* static margin provisional (VLM/panel);", font=FSUB24, fill=GREY)
    d.text((x, yy + 28), "  fuselage makes it marginal at current CG.", font=FSUB24, fill=GREY)


if __name__ == "__main__":
    main()

    print("poster saved ->", os.path.join(G, "v6_poster.png"))
