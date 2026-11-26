#!/usr/bin/env python3
"""Render assets/og-image.png (1200x630) from the official wordmark.

Usage (from the repo root):  python3 scripts/make_og.py
Requires Pillow. Rasterizes the path in assets/logo-white.svg directly
(it uses only absolute M/L/C/Z commands, even-odd fill), so the wordmark
is the official artwork, not a redraw. Text uses a local sans font if found.
"""
import re
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
W, H, SS = 1200, 630, 4
BG, FG, MUTED, LIME, TEAL, BORDER = (11, 13, 11), (241, 245, 236), (163, 173, 159), (195, 245, 60), (62, 230, 180), (35, 42, 35)


def subpaths(d):
    toks = re.findall(r"[MLCZmlcz]|-?\d*\.?\d+(?:e-?\d+)?", d)
    i, cur, out, pts, cmd = 0, (0.0, 0.0), [], [], None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                if pts:
                    out.append(pts)
                pts = []
            continue
        if cmd == "M":
            cur = (float(toks[i]), float(toks[i + 1])); i += 2
            if pts:
                out.append(pts)
            pts = [cur]; cmd = "L"
        elif cmd == "L":
            cur = (float(toks[i]), float(toks[i + 1])); i += 2
            pts.append(cur)
        elif cmd == "C":
            x1, y1, x2, y2, x, y = map(float, toks[i:i + 6]); i += 6
            x0, y0 = cur
            for k in range(1, 17):
                s = k / 16; m = 1 - s
                pts.append((m**3 * x0 + 3 * m * m * s * x1 + 3 * m * s * s * x2 + s**3 * x,
                            m**3 * y0 + 3 * m * m * s * y1 + 3 * m * s * s * y2 + s**3 * y))
            cur = (x, y)
        else:
            raise ValueError("unsupported path command " + str(cmd))
    if pts:
        out.append(pts)
    return out


def wordmark_mask(width_px):
    svg = (ROOT / "assets/logo-white.svg").read_text()
    d = re.search(r'\sd="([^"]+)"', svg).group(1)
    scale = width_px * SS / 1485
    w, h = int(1485 * scale), int(235 * scale)
    mask = Image.new("1", (w, h), 0)
    for sp in subpaths(d):
        layer = Image.new("1", (w, h), 0)
        ImageDraw.Draw(layer).polygon([(x * scale, y * scale) for x, y in sp], fill=1)
        mask = ImageChops.logical_xor(mask, layer)  # even-odd fill
    return mask.convert("L").resize((w // SS, h // SS), Image.LANCZOS)


def font(size, weight):
    for path in ["/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if Path(path).exists():
            f = ImageFont.truetype(path, size)
            try:
                f.set_variation_by_axes([size if size < 32 else 32, weight])
            except Exception:
                pass
            return f
    return ImageFont.load_default()


def main():
    img = Image.new("RGB", (W, H), BG)
    # soft lime glow, top center
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((W / 2 - 520, -420, W / 2 + 520, 260), fill=60)
    from PIL import ImageFilter
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.composite(Image.new("RGB", (W, H), (150, 220, 40)), img, glow)
    dr = ImageDraw.Draw(img)
    # faint grid
    for x in range(0, W, 56):
        dr.line([(x, 0), (x, H)], fill=(19, 22, 19))
    for y in range(0, H, 56):
        dr.line([(0, y), (W, y)], fill=(19, 22, 19))

    left = 96
    m = wordmark_mask(640)
    img.paste(Image.new("RGB", m.size, (255, 255, 255)), (left, 190), m)
    dr = ImageDraw.Draw(img)
    f_big = font(64, 700)
    dr.text((left, 190 + m.size[1] + 34), "Business Broker", font=f_big, fill=MUTED)
    # lime accent bar + line
    dr.rounded_rectangle((left, 120, left + 10, 130), radius=5, fill=LIME)
    dr.text((left + 24, 112), "VALUE-ADDED BUSINESS BROKER", font=font(22, 600), fill=MUTED)
    by = H - 110
    dr.line([(left, by - 30), (W - left, by - 30)], fill=BORDER, width=2)
    f_sm = font(30, 600)
    t1 = "Raise value before a sale. "
    dr.text((left, by), t1, font=f_sm, fill=FG)
    x2 = left + dr.textlength(t1, font=f_sm)
    dr.text((x2, by), "Grow it after you buy.", font=f_sm, fill=LIME)
    dr.text((W - left, by), "swyftbb.com", font=font(26, 500), fill=TEAL, anchor="ra")
    out = ROOT / "assets/og-image.png"
    img.save(out, optimize=True)
    print("Wrote", out)


if __name__ == "__main__":
    main()
