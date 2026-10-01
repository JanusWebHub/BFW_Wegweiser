"""Combine the ground-floor Flucht- und Rettungsplan photos into one image.

Usage (works from any working directory):
    python claude/tools/compose_eg.py                 # combined_eg.png
    python claude/tools/compose_eg.py --overlay       # combined_eg_overlay.png
    python claude/tools/compose_eg.py --src DIR [out.png] [--overlay]

Where the inputs come from:
    The script finds its inputs itself, so it can live anywhere in the repo.
    The repo root is derived from this file's location (claude/tools/ goes up
    two levels). Photos and the 2018 PDF are read from
        <repo root>/docs/ignore/archive/other/eg
    Use --src DIR to read them from another folder instead. Needed there:
        - the 7 photos named in WINGS below (IMG-20260911-WA00xx.jpg)
        - Grafik_Etage_BFW_rotated180 1.pdf (only with --overlay)
    If any are missing, the script stops before doing any work and lists them,
    with a reminder to use --src. Photo file names, crop boxes and anchors are
    hardcoded in WINGS, so a different photo set needs new entries.

Output:
    out.png as the first positional argument, else combined_eg.png or
    combined_eg_overlay.png inside the source folder. Plain output is trimmed
    to its content; --overlay keeps the full 2018 sheet.

--overlay:
    Draws the photos on top of the 2018 layout as faint red linework, which
    makes placement errors easy to see. This puts the 2018 labels and names in
    the picture. The default output contains nothing from the 2018 PDF.

How the placement works:
    The 10 photos show 7 distinct wings; one photo per wing is used (the rest
    are the same wings at other rotations). Each WINGS entry holds the photo,
    a crop box (drawing only, no title, legend or behaviour boxes), two anchor
    points in the photo and the matching two points on the canvas. A
    similarity transform (scale, rotation, translation, no flip) is derived
    from the anchors. Canvas anchors were read off the 2018 layout (rotated
    upright, 2000 x 1414 layout units) only to decide where each wing sits;
    nothing else from that PDF is used. NUDGE holds small manual shifts read
    off a marked-up overlay. Each photo is also lighting-flattened, and its
    Standort marker is removed (colour test, plus BLANKS polygons for grey
    ones). Overlapping wings are merged by keeping the darker pixel.

Limits:
    A photo collage, not a survey. The 2018 layout is not metrically exact
    against the 2026 plans, and the photos have perspective skew, so seams
    can be off by a few tens of layout units. Text keeps each photo's own
    rotation. Per-wing scale differs slightly (about 0.59 to 0.68).

Needs: numpy, Pillow.
"""
import argparse
import io
import math
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[2]          # claude/tools/ -> repo root
ap = argparse.ArgumentParser()
ap.add_argument("out", nargs="?")
ap.add_argument("--overlay", action="store_true")
ap.add_argument("--src", default=str(REPO / "docs/ignore/archive/other/eg"))
args = ap.parse_args()

SRC = Path(args.src).resolve()
OVERLAY = args.overlay
OUT = Path(args.out) if args.out else SRC / (
    "combined_eg_overlay.png" if OVERLAY else "combined_eg.png")
PDF = SRC / "Grafik_Etage_BFW_rotated180 1.pdf"

S = 2.0                  # canvas pixels per layout unit
CW, CH = 2000, 1414      # layout units

WINGS = [
    # plan, file, crop box, photo anchors, canvas anchors
    ("052", "IMG-20260911-WA0005.jpg", (590, 360, 1650, 740),
     ((1505, 635), (548, 520)), ((359, 140), (622, 737))),
    ("053", "IMG-20260911-WA0004.jpg", (170, 650, 930, 1400),
     ((415, 860), (828, 1318)), ((622, 737), (522, 1090))),
    ("054", "IMG-20260911-WA0002.jpg", (295, 490, 840, 1270),
     ((565, 990), (665, 990)), ((279, 700), (279 - 100 * 0.63, 700))),
    ("055", "IMG-20260911-WA0006.jpg", (290, 600, 690, 1405),
     ((617, 1200), (500, 718)), ((918, 787), (1251, 733))),
    ("056", "IMG-20260911-WA0001.jpg", (440, 540, 830, 1425),
     ((503, 1195), (610, 797)), ((1042, 1008), (1307, 1072))),
    ("058", "IMG-20260911-WA0009.jpg", (140, 295, 1450, 870),
     ((848, 520), (350, 830)), ((1688, 641), (1412, 850))),
    ("060", "IMG-20260911-WA0000.jpg", (195, 415, 1600, 745),
     ((258, 595), (1480, 590)), ((1651, 311), (841, 315))),
]

NUDGE = {  # manual shifts (layout units) read off the marked-up overlay
    "055": (50, 15),
    "056": (20, 20),
    "058": (28, 16),
    "060": (-30, 0),
}

BLANKS = {  # grey Standort markers the colour test misses (photo coords)
    "IMG-20260911-WA0009.jpg": [[(385, 378), (600, 378), (600, 428), (470, 428),
                                (335, 612), (312, 606), (425, 428), (385, 428)]],
}


def similarity(p, c):
    """Return (a, b, tx, ty) with canvas = [[a,-b],[b,a]] @ photo + t."""
    (p1, p2), (c1, c2) = p, c
    pv = complex(p2[0] - p1[0], p2[1] - p1[1])
    cv = complex(c2[0] - c1[0], c2[1] - c1[1])
    z = cv / pv
    a, b = z.real, z.imag
    tx = c1[0] - (a * p1[0] - b * p1[1])
    ty = c1[1] - (b * p1[0] + a * p1[1])
    return a, b, tx, ty


def clean(im, box, blanks=()):
    """Crop to the drawing, flatten the lighting, drop the Standort marker."""
    a = np.asarray(im).astype(np.float32)
    small = im.resize((im.width // 8, im.height // 8), Image.BILINEAR)
    bg = small.filter(ImageFilter.MaxFilter(11)).filter(ImageFilter.GaussianBlur(6))
    bg = np.asarray(bg.resize(im.size, Image.BILINEAR)).astype(np.float32)
    v = np.clip(a / np.maximum(bg, 1) / 0.93, 0, 1)
    r, g, bl = a[..., 0], a[..., 1], a[..., 2]
    navy = (((bl - r >= 12) & (bl - g >= 6) & (bl < 110))
            | ((bl - r >= 40) & (bl - g >= 15)))
    navy = Image.fromarray((navy * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7))
    v[np.asarray(navy) > 0] = 1
    if blanks:
        m = Image.new("L", im.size, 0)
        for poly in blanks:
            ImageDraw.Draw(m).polygon(poly, fill=255)
        v[np.asarray(m) > 0] = 1
    keep = np.zeros(a.shape[:2], bool)
    x0, y0, x1, y1 = box
    keep[y0:y1, x0:x1] = True
    v[~keep] = 1
    return Image.fromarray((v * 255).astype(np.uint8))


needed = [SRC / w[1] for w in WINGS] + ([PDF] if OVERLAY else [])
missing = [p.name for p in needed if not p.exists()]
if missing:
    sys.exit("missing in %s: %s\nUse --src DIR to point at the folder." % (SRC, ", ".join(missing)))

canvas = Image.new("RGB", (int(CW * S), int(CH * S)), "white")
if OVERLAY:
    # backdrop: the 2018 layout (embedded JPEG of the PDF), rotated upright,
    # as faint red linework so the photos on top stay readable
    pdf = PDF.read_bytes()
    jpg = pdf[pdf.find(b"\xff\xd8\xff"):pdf.rfind(b"\xff\xd9") + 2]
    ref = Image.open(io.BytesIO(jpg)).convert("L").rotate(180).resize(canvas.size)
    ink = np.clip((200 - np.asarray(ref).astype(np.float32)) / 200, 0, 1)[..., None]
    canvas = Image.fromarray((255 - ink * np.array([0, 200, 200], np.float32)).astype(np.uint8))

for name, fname, box, pa, ca in WINGS:
    a, b, tx, ty = similarity(pa, ca)
    dx, dy = NUDGE.get(name, (0, 0))
    tx, ty = tx + dx, ty + dy
    a, b, tx, ty = a * S, b * S, tx * S, ty * S
    det = a * a + b * b
    # PIL wants the inverse map: photo = M^-1 (canvas - t)
    ia, ib = a / det, -b / det
    coeffs = (ia, -ib, -(ia * tx - ib * ty),
              ib, ia, -(ib * tx + ia * ty))
    cropped = clean(Image.open(SRC / fname).convert("RGB"), box, BLANKS.get(fname, ()))
    warped = cropped.transform(canvas.size, Image.AFFINE, coeffs,
                               resample=Image.BICUBIC, fillcolor="white")
    canvas = ImageChops.darker(canvas, warped)
    print(name, "scale %.3f rot %.1f deg" % (math.hypot(a, b) / S,
                                              math.degrees(math.atan2(b, a))))

bbox = ImageChops.invert(canvas.convert("L")).point(lambda v: 255 if v > 40 else 0).getbbox()
m = 60
bbox = (max(bbox[0] - m, 0), max(bbox[1] - m, 0),
        min(bbox[2] + m, canvas.width), min(bbox[3] + m, canvas.height))
(canvas if OVERLAY else canvas.crop(bbox)).save(OUT)
print("wrote", OUT)
