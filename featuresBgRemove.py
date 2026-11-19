from pathlib import Path

from PIL import Image, ImageOps
from rembg import new_session, remove

# input folder -> output folder
FOLDERS = {
    "Head": "headNoBg",
    "Sit": "sitNoBg",
    "stand": "standNoBg",
}

# "isnet-general-use" is a good default; "birefnet-general" is slower but more accurate.
MODEL = "isnet-general-use"

# Smooths soft edges (fabric, fringe) but can erode hard-edged objects.
ALPHA_MATTING = False

EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def process_folder(in_dir: Path, out_dir: Path, session) -> None:
    if not in_dir.is_dir():
        print(f"Skipping '{in_dir}': folder not found")
        return

    out_dir.mkdir(exist_ok=True)

    files = sorted(p for p in in_dir.iterdir() if p.suffix.lower() in EXTENSIONS)
    if not files:
        print(f"No images found in '{in_dir}'")
        return

    print(f"\n=== {in_dir} -> {out_dir} ({len(files)} images) ===")

    for i, path in enumerate(files, start=1):
        out_path = out_dir / f"{path.stem}.png"

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


def main() -> None:
    # Load the model once and reuse it for every folder
    session = new_session(MODEL)

    for in_name, out_name in FOLDERS.items():
        process_folder(Path(in_name), Path(out_name), session)

    print("\nDone.")


if __name__ == "__main__":
    main()
