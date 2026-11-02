# svg2font-docker

Convert a folder of SVG glyphs/icons into TTF and OTF fonts.

## User guide

### Get started

You need Docker installed and running. To build a font from your own folder:

```bash
docker run --rm -v "/path/to/my-font:/data" ghcr.io/rabidgremlin/svg2font-docker:latest .
```

Docker automatically pulls the image if it is not already available locally.
The generated `.ttf` and `.otf` files appear alongside your inputs. Existing
files with the same names are overwritten.

The repository contains [example inputs](example/) and a [generated TTF font](example/SVG2FontExampleFont-Regular.ttf).
To try the example, download a local copy of the example folder, then run:

```bash
docker run --rm -v "/path/to/example:/data" ghcr.io/rabidgremlin/svg2font-docker:latest .
```

### Create your own font

Create a folder containing a `font.yaml` file and your SVG glyphs/icons. For example:

```yaml
fontname: MyIconFont-Regular
familyname: My Icon Font
fullname: My Icon Font Regular
weight: Regular
version: "1.0"
copyright: Copyright 2026 Your Name
```

Only `fontname` is required. The other fields are optional strings; quote version
numbers in YAML. Missing `familyname` and `fullname` default to `fontname`. The
font name must contain only ASCII letters, digits, underscores, periods, or
hyphens, and be at most 63 characters long.

Name each SVG `X_description.svg`, where `X` identifies the character:

- A single character, such as `a_icon.svg` or `A_icon.svg`. Case matters, so these map to different characters. A single digit maps to that digit character.
- A decimal code point of two or more digits, such as `65_icon.svg` for `A`.
- A Unicode code point, such as `U+0041_icon.svg` for `A`.

Each character can appear only once: `65_icon.svg` and `U+0041_icon.svg` cannot
be used together. SVG extensions are case-insensitive.

Mount your font folder at `/data` and pass `.` to use it:

```bash
docker run --rm -v "/path/to/my-font:/data" ghcr.io/rabidgremlin/svg2font-docker:latest .
```

Alternatively, mount a parent folder and pass a subfolder name:

```bash
docker run --rm -v "/path/to/fonts:/data" ghcr.io/rabidgremlin/svg2font-docker:latest my-font
```

The mounted folder must be writable. The generated fonts are saved alongside the
inputs using `fontname` as the filename. On Linux, add
`--user "$(id -u):$(id -g)"` to the `docker run` command if you want output files
owned by your current user.

## Developer guide

Open the repository in a development container using the included `.devcontainer`
configuration. Its setup installs FontForge's Python bindings and prepares a `uv`
environment with access to system packages.

Run the script inside the development container:

```bash
uv run python main.py example
```

Replace `example` with the path to another font input folder.
