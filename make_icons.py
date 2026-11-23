# -*- coding: utf-8 -*-
"""Generate PWA icons for Mingli ClearLogic."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

BASE = Path(__file__).resolve().parent
OUT = BASE / "icons"
OUT.mkdir(parents=True, exist_ok=True)
S = 1024


def gradient(size, top=(10, 132, 255), bottom=(100, 210, 255)):
    img = Image.new("RGB", (size, size), top)
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / max(1, size - 1)
        # ease
        t = t * t * (3 - 2 * t)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (size, y)], fill=c)
    return img


def mark(size, scale=1.0, alpha=True):
    """Three descending white bars, centered."""
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w = int(460 * scale)
    h = int(92 * scale)
    x = (size - w) // 2
    gap = int(30 * scale)
    total = h * 3 + gap * 2
    y = (size - total) // 2
    widths = [w, int(w * 0.78), int(w * 0.56)]
    alphas = [255, 196, 138] if alpha else [255, 255, 255]
    for i, bw in enumerate(widths):
        bx = x + (w - bw) // 2
        d.rounded_rectangle([bx, y, bx + bw, y + h], radius=h // 2, fill=(255, 255, 255, alphas[i]))
        y += h + gap
    return layer


def rounded_icon(size, radius_ratio=0.22, transparent=True):
    img = gradient(S)
    mask = Image.new("L", (S, S), 0)
    md = ImageDraw.Draw(mask)
    r = int(S * radius_ratio)
    md.rounded_rectangle([0, 0, S - 1, S - 1], radius=r, fill=255)
    # subtle top-right gloss
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.ellipse([S * 0.55, -S * 0.35, S * 1.35, S * 0.55], fill=(255, 255, 255, 26))
    gloss = gloss.filter(ImageFilter.GaussianBlur(80))
    img = img.convert("RGBA")
    img.alpha_composite(gloss)
    img.alpha_composite(mark(S))
    img.putalpha(mask if transparent else Image.new("L", (S, S), 255))
    return img.resize((size, size), Image.LANCZOS)


def square_icon(size, radius_ratio=0.0, scale=0.78):
    img = gradient(S).convert("RGBA")
    gloss = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.ellipse([S * 0.55, -S * 0.35, S * 1.35, S * 0.55], fill=(255, 255, 255, 26))
    gloss = gloss.filter(ImageFilter.GaussianBlur(80))
    img.alpha_composite(gloss)
    img.alpha_composite(mark(S, scale=scale))
    if radius_ratio > 0:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius_ratio), fill=255)
        img.putalpha(mask)
    return img.resize((size, size), Image.LANCZOS)


# 192 / 512 standard
rounded_icon(192, 0.22).save(OUT / "icon-192.png", "PNG", optimize=True)
rounded_icon(512, 0.22).save(OUT / "icon-512.png", "PNG", optimize=True)
# maskable: full square, safe-zone mark
square_icon(512, 0.0, 0.72).save(OUT / "icon-maskable-512.png", "PNG", optimize=True)
# iOS home screen (iOS masks corners itself)
square_icon(180, 0.0, 0.76).save(OUT / "apple-touch-icon-180.png", "PNG", optimize=True)
# favicon
rounded_icon(32, 0.22).save(OUT / "favicon-32.png", "PNG", optimize=True)
rounded_icon(64, 0.22).save(OUT / "favicon-64.png", "PNG", optimize=True)

# also a 1024 master for stores / docs
rounded_icon(1024, 0.22).save(OUT / "icon-1024.png", "PNG", optimize=True)

for p in sorted(OUT.glob("*.png")):
    print(p.name, p.stat().st_size)
