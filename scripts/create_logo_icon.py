"""One-off script: crop myway.png to icon-only and save as logo-icon.png."""
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Install Pillow: pip install Pillow")

def main():
    base = Path(__file__).resolve().parent.parent
    src = base / "assets" / "images" / "myway.png"
    dst = base / "assets" / "images" / "logo-icon.png"
    if not src.exists():
        raise SystemExit(f"Source not found: {src}")
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    # Keep only top ~52% so the Y-shaped icon is included and wordmark is excluded
    crop_h = int(h * 0.52)
    box = (0, 0, w, crop_h)
    cropped = img.crop(box)
    dst.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(dst, "PNG")
    print(f"Saved {dst}")

if __name__ == "__main__":
    main()
