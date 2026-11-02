import argparse
import re
import sys
from pathlib import Path

import yaml


FIELDS = {"fontname", "familyname", "fullname", "weight", "version", "copyright"}


def load_metadata(folder):
    path = folder / "font.yaml"
    try:
        with path.open(encoding="utf-8") as stream:
            metadata = yaml.safe_load(stream)
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(metadata, dict) or any(key not in FIELDS for key in metadata):
        raise ValueError("font.yaml must contain only supported metadata fields")
    if any(not isinstance(value, str) or not value.strip() for value in metadata.values()):
        raise ValueError("Metadata values must be nonempty strings (quote version numbers)")
    name = metadata.get("fontname")
    if not name or not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or len(name) > 63 or name in {".", ".."}:
        raise ValueError("fontname is required and must be a valid PostScript name (ASCII letters, digits, _, . or -, up to 63 characters)")
    metadata.setdefault("familyname", name)
    metadata.setdefault("fullname", name)
    return metadata


def discover_svgs(folder):
    mappings = {}
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() != ".svg":
            continue
        prefix, separator, description = path.stem.partition("_")
        if not separator or not description:
            raise ValueError(f"Invalid SVG filename: {path.name}")
        if len(prefix) == 1:
            codepoint = ord(prefix)
        elif re.fullmatch(r"[0-9]+", prefix):
            codepoint = int(prefix)
        elif re.fullmatch(r"U\+[0-9a-fA-F]+", prefix):
            codepoint = int(prefix[2:], 16)
        else:
            raise ValueError(f"Invalid character prefix in {path.name}")
        if codepoint > 0x10FFFF or 0xD800 <= codepoint <= 0xDFFF:
            raise ValueError(f"Invalid Unicode code point in {path.name}")
        if codepoint in mappings:
            raise ValueError(f"Duplicate character mapping: {mappings[codepoint].name} and {path.name}")
        mappings[codepoint] = path
    if not mappings:
        raise ValueError(f"No SVG files found in {folder}")
    return mappings


def create_font(folder, align_baseline=False):
    metadata = load_metadata(folder)
    mappings = discover_svgs(folder)
    import fontforge

    font = fontforge.font()
    try:
        for key, value in metadata.items():
            setattr(font, key, value)
        for codepoint, path in mappings.items():
            glyph = font.createChar(codepoint)
            glyph.importOutlines(str(path))
            if align_baseline:
                ymin = glyph.boundingBox()[1]
                glyph.transform([1, 0, 0, 1, 0, -ymin])
            glyph.left_side_bearing = 15
            glyph.right_side_bearing = 15
        for extension in ("ttf", "otf"):
            font.generate(str(folder / f"{metadata['fontname']}.{extension}"))
    finally:
        font.close()
    print(f"Font created: {folder / metadata['fontname']}.ttf/.otf")


def main():
    parser = argparse.ArgumentParser(description="Build a font from a folder of SVGs")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--align-baseline", action="store_true",
                        help="align the bottom of each outline to the baseline")
    args = parser.parse_args()
    try:
        create_font(args.folder, align_baseline=args.align_baseline)
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
