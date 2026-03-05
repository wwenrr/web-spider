#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from PIL import Image


def main() -> None:
    args = parse_args()
    image = Image.open(args.input).convert("RGBA")
    width, height = image.size
    pixels = image.load()

    bg = estimate_background(image)
    row_foreground = []
    min_row_pixels = max(1, int(width * args.min_row_fraction))

    for y in range(height):
        count = 0
        for x in range(width):
            if is_foreground(pixels[x, y], bg, args.tolerance):
                count += 1
        row_foreground.append(count)

    bands = find_bands(row_foreground, min_row_pixels)
    if not bands:
        image.save(args.output)
        return

    # Choose the main icon band: prefer larger area and earlier (higher) position.
    best = max(bands, key=lambda b: (b[1] - b[0]) - (b[0] * 0.15))
    top, bottom = best

    left, right = find_column_bounds(pixels, width, top, bottom, bg, args.tolerance)
    if left >= right:
        image.save(args.output)
        return

    pad_x = int((right - left) * args.pad)
    pad_y = int((bottom - top) * args.pad)
    left = max(0, left - pad_x)
    right = min(width - 1, right + pad_x)
    top = max(0, top - pad_y)
    bottom = min(height - 1, bottom + pad_y)

    cropped = image.crop((left, top, right + 1, bottom + 1))
    squared = to_square(cropped)
    squared.save(args.output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove text under a logo by keeping the primary upper foreground band."
    )
    parser.add_argument("input", type=Path, help="Input image path")
    parser.add_argument("output", type=Path, help="Output image path")
    parser.add_argument("--tolerance", type=int, default=40, help="Foreground color tolerance")
    parser.add_argument("--min-row-fraction", type=float, default=0.01, help="Minimum foreground ratio per row")
    parser.add_argument("--pad", type=float, default=0.08, help="Extra padding around detected icon")
    return parser.parse_args()


def estimate_background(image: Image.Image) -> tuple[int, int, int]:
    width, height = image.size
    pixels = image.load()
    samples: list[tuple[int, int, int]] = []

    border = max(1, min(width, height) // 50)
    for x in range(width):
        for y in range(border):
            samples.append(pixels[x, y][:3])
            samples.append(pixels[x, height - 1 - y][:3])
    for y in range(height):
        for x in range(border):
            samples.append(pixels[x, y][:3])
            samples.append(pixels[width - 1 - x, y][:3])

    # Most common border color is usually the page/background.
    return Counter(samples).most_common(1)[0][0]


def is_foreground(px: tuple[int, int, int, int], bg: tuple[int, int, int], tolerance: int) -> bool:
    if px[3] < 10:
        return False
    return (
        abs(px[0] - bg[0]) + abs(px[1] - bg[1]) + abs(px[2] - bg[2])
    ) > tolerance


def find_bands(row_counts: list[int], threshold: int) -> list[tuple[int, int]]:
    bands: list[tuple[int, int]] = []
    start: int | None = None
    for i, count in enumerate(row_counts):
        if count >= threshold and start is None:
            start = i
        elif count < threshold and start is not None:
            bands.append((start, i - 1))
            start = None
    if start is not None:
        bands.append((start, len(row_counts) - 1))
    return bands


def find_column_bounds(
    pixels,
    width: int,
    top: int,
    bottom: int,
    bg: tuple[int, int, int],
    tolerance: int,
) -> tuple[int, int]:
    left = width - 1
    right = 0
    for y in range(top, bottom + 1):
        for x in range(width):
            if is_foreground(pixels[x, y], bg, tolerance):
                left = min(left, x)
                right = max(right, x)
    return left, right


def to_square(image: Image.Image) -> Image.Image:
    w, h = image.size
    side = max(w, h)
    canvas = Image.new("RGBA", (side, side), (255, 255, 255, 0))
    offset_x = (side - w) // 2
    offset_y = (side - h) // 2
    canvas.paste(image, (offset_x, offset_y), image)
    return canvas


if __name__ == "__main__":
    main()
