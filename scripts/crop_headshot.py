from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


# Headshot crop controls.
# Coordinates are in pixels relative to assets/headshot-source.jpg.
# Increase CROP_TOP to move the crop window down; decrease it to move up.
# Decrease CROP_SIZE to zoom in; increase it to zoom out.
CROP_LEFT = 128
CROP_TOP = 280
CROP_SIZE = 674
OUTPUT_SIZES = (368, 552, 900)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "headshot-source.jpg"


def main() -> None:
    image = Image.open(SOURCE)
    image = ImageOps.exif_transpose(image).convert("RGB")

    crop_box = (
        CROP_LEFT,
        CROP_TOP,
        CROP_LEFT + CROP_SIZE,
        CROP_TOP + CROP_SIZE,
    )
    cropped = image.crop(crop_box)

    for size in OUTPUT_SIZES:
        resized = cropped.resize((size, size), Image.Resampling.LANCZOS)
        resized = resized.filter(ImageFilter.UnsharpMask(radius=0.8, percent=110, threshold=3))

        suffix = "" if size == max(OUTPUT_SIZES) else f"-{size}"
        jpeg_output = ROOT / "assets" / f"headshot{suffix}.jpg"
        webp_output = ROOT / "assets" / f"headshot{suffix}.webp"

        resized.save(jpeg_output, "JPEG", quality=95, optimize=True)
        resized.save(webp_output, "WEBP", quality=95, method=6)


if __name__ == "__main__":
    main()
