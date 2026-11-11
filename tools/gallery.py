#!/usr/bin/env python3
"""Prepare gallery photos for the R2 bucket and print the <img> tags for them.

Usage:
    python3 tools/gallery.py SOURCE_DIR OUT_DIR [--layout grid|strips|masonry]

Needs Pillow (`pip install pillow`). For each JPEG/PNG in SOURCE_DIR it writes:
    OUT_DIR/gallery/750/<name>.webp    small copy for phones and grid thumbnails
    OUT_DIR/gallery/1500/<name>.webp   large copy for desktop and high-DPI screens
    OUT_DIR/gallery/full/<name>.jpg    2500px archive copy (not used by the pages)
Rotation from the camera is applied and all metadata (including GPS) is dropped.

Then upload (see CLAUDE.md):
    rclone copy OUT_DIR r2:countykidsofsteel-photos --s3-no-check-bucket \
      --header-upload "Cache-Control: public, max-age=31536000, immutable"
"""
import argparse
import os
import re
import sys

from PIL import Image, ImageOps

BASE = "https://photos.countykidsofsteel.ca/gallery"
WIDTHS = (750, 1500)
FULL = 2500
SIZES = {
    "grid": "(max-width: 767px) 50vw, 33vw",
    "strips": "(max-width: 767px) 50vw, 33vw",
    "masonry": "(max-width: 767px) 100vw, 50vw",
}


def key_for(filename):
    """URL-safe name: letters, digits, dash and underscore only."""
    stem = os.path.splitext(filename)[0]
    return re.sub(r"[^A-Za-z0-9_-]+", "-", stem).strip("-")


def fit(im, width):
    if im.width <= width:
        return im
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("out")
    ap.add_argument("--layout", choices=SIZES, default="grid")
    args = ap.parse_args()

    for d in [*map(str, WIDTHS), "full"]:
        os.makedirs(os.path.join(args.out, "gallery", d), exist_ok=True)

    files = sorted(f for f in os.listdir(args.source)
                   if f.lower().endswith((".jpg", ".jpeg", ".png")))
    seen = set()
    for f in files:
        key = key_for(f)
        if key in seen:
            sys.exit(f"Two files map to the same name '{key}'. Rename one and rerun.")
        seen.add(key)
        im = ImageOps.exif_transpose(Image.open(os.path.join(args.source, f))).convert("RGB")
        for w in WIDTHS:
            fit(im, w).save(os.path.join(args.out, "gallery", str(w), f"{key}.webp"),
                            "WEBP", quality=80, method=6)
        full = fit(im, FULL)
        full.save(os.path.join(args.out, "gallery", "full", f"{key}.jpg"),
                  "JPEG", quality=85, progressive=True)
        default = WIDTHS[-1] if args.layout == "masonry" else WIDTHS[0]
        srcset = ", ".join(f"{BASE}/{w}/{key}.webp {w}w" for w in WIDTHS)
        tag = (f'<img src="{BASE}/{default}/{key}.webp" srcset="{srcset}" '
               f'sizes="{SIZES[args.layout]}" alt="" width="{full.width}" '
               f'height="{full.height}" loading="lazy" decoding="async">')
        if args.layout == "strips":
            tag = f'<figure style="--ar:{full.width / full.height:.3f}">{tag}</figure>'
        else:
            tag = f"<figure>{tag}</figure>"
        print(tag)


if __name__ == "__main__":
    main()
