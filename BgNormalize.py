"""
Batch background removal for museum artifact photos.

Reads every image in ./images and writes a transparent-background PNG
with the same name to ./imagesNoBg.

Install:
    pip install "rembg[cpu]" pillow          # or "rembg[gpu]" for NVIDIA GPUs
"""

from pathlib import Path

from PIL import Image, ImageOps
from rembg import new_session, remove

INPUT_DIR = Path("images")
OUTPUT_DIR = Path("imagesNoBg")

# Good general-purpose models for objects/artifacts:
#   "isnet-general-use"  - fast, clean edges (good default)
#   "birefnet-general"   - best quality, slower and heavier
#   "u2net"              - older default, still decent
MODEL = "isnet-general-use"

# Alpha matting smooths soft edges (fringes, fabric, feathers) but can
# eat into hard-edged objects like pottery or metal. Try it if edges look rough.
ALPHA_MATTING = False

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def main() -> None:
    if not INPUT_DIR.is_dir():
        raise SystemExit(f"Input folder not found: {INPUT_DIR.resolve()}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    # Load the model once and reuse it for every image
    session = new_session(MODEL)

    files = sorted(p for p in INPUT_DIR.iterdir() if p.suffix.lower() in EXTENSIONS)
    if not files:
        raise SystemExit(f"No images found in {INPUT_DIR.resolve()}")

    for i, path in enumerate(files, start=1):
        out_path = OUTPUT_DIR / f"{path.stem}.png"

        if out_path.exists():
            print(f"[{i}/{len(files)}] skipping {path.name} (already done)")
            continue

        try:
            with Image.open(path) as img:
                img = ImageOps.exif_transpose(img)  # respect camera rotation
                result = remove(img, session=session, alpha_matting=ALPHA_MATTING)
            result.save(out_path)
            print(f"[{i}/{len(files)}] {path.name} -> {out_path.name}")
        except Exception as e:
            print(f"[{i}/{len(files)}] FAILED {path.name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
