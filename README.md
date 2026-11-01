# svg2font-docker
Containerised tool for converting a folder of .svg files into a .ttf font

## Dev container

The `.devcontainer` folder provides a minimal environment based on Debian trixie with GitHub CLI, Node.js, Python, uv, Docker-in-Docker (moby disabled) and the [Codex CLI](https://github.com/openai/codex).

## Build a font

Run `uv run python main.py example` (replace `example` with your font folder).
The folder must contain `font.yaml` with a `fontname`; optional string fields are
`familyname`, `fullname`, `weight`, `version`, and `copyright`. Quote version
numbers in YAML. Missing family and full names default to `fontname`. The font
name must contain only ASCII letters, digits, underscores, periods, or hyphens,
and be at most 63 characters long.

Name each SVG `X_description.svg`, where `X` is a single case-sensitive
character, a decimal code point (two or more digits), or a Unicode code point
such as `U+0041`. For example, `a_icon.svg` and `A_icon.svg` map to different
characters; `65_icon.svg` and `U+0041_icon.svg` both map to `A` and cannot be
used together. A single digit maps to that digit character. SVG extensions are
case-insensitive. The generated TTF and OTF files are written into the folder,
using `fontname` as the filename, and existing files may be overwritten.
