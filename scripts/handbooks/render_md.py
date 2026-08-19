#!/usr/bin/env python3
"""Render Mermaid diagrams and browser-sensitive SVGs for reliable PDF output."""

import os
import re
import shutil
import subprocess
import sys


inp, out, assets_dir, pptr, mmdc = sys.argv[1:6]
text = open(inp, encoding="utf-8").read()
out_dir = os.path.dirname(os.path.abspath(out))
config = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mermaid.json")
environment = {
    **os.environ,
    "PUPPETEER_EXECUTABLE_PATH": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
}

pieces = []
last = 0
diagram_count = 0
diagram_failures = 0
for match in re.finditer(r"```mermaid[ \t]*\n(.*?)\n```", text, re.S):
    diagram_count += 1
    pieces.append(text[last : match.start()])
    code = match.group(1)
    caption = None
    caption_match = re.match(
        r"(?P<space>\n(?:[ \t]*\n)?)(?P<caption>\*(?:Figure|Diagram)\b[^\n]*\*)",
        text[match.end() :],
        re.I,
    )
    if caption_match:
        caption = caption_match.group("caption")
        last = match.end() + caption_match.end()
    else:
        last = match.end()

    source = os.path.join(assets_dir, f"_diagram_{diagram_count}.mmd")
    image = os.path.join(assets_dir, f"_diagram_{diagram_count}.png")
    with open(source, "w", encoding="utf-8") as handle:
        handle.write(code)

    ok = False
    result = None
    try:
        result = subprocess.run(
            [
                mmdc,
                "-i",
                source,
                "-o",
                image,
                "-p",
                pptr,
                "-c",
                config,
                "-e",
                "png",
                "-s",
                "2.5",
                "-b",
                "white",
            ],
            capture_output=True,
            timeout=150,
            env=environment,
        )
        ok = result.returncode == 0 and os.path.isfile(image) and os.path.getsize(image) > 500
    except Exception as exc:
        print(f"Mermaid diagram {diagram_count} raised {exc!r}", file=sys.stderr)
    finally:
        if os.path.exists(source):
            os.remove(source)

    if ok:
        relative = os.path.relpath(image, out_dir).replace(os.sep, "/")
        figure = [
            "",
            "::: {.figure-block .diagram-wrap}",
            f"![Technical diagram]({relative})",
        ]
        if caption:
            figure.extend(("", caption))
        figure.extend((":::", ""))
        pieces.append("\n".join(figure))
    else:
        detail = ""
        if result is not None:
            detail = (result.stderr or result.stdout or b"").decode(
                "utf-8", errors="replace"
            )[-4000:]
        print(f"Mermaid diagram {diagram_count} failed:\n{detail}", file=sys.stderr)
        diagram_failures += 1
        pieces.append("\n```text\n" + code + "\n```\n")
        if caption:
            pieces.append("\n" + caption + "\n")

pieces.append(text[last:])
rendered = "".join(pieces)

svg_count = 0
svg_failures = 0
svg_cache = {}
svg_pattern = re.compile(
    r"(?P<prefix>!\[[^\]]*\]\()"
    r"(?P<path>(?:assets/)?[^)\s]+\.svg)"
    r"(?P<suffix>(?:\s+[\"'][^)]*[\"'])?\))",
    re.I,
)
rsvg = shutil.which("rsvg-convert")
input_dir = os.path.dirname(os.path.abspath(inp))


def rasterize_svg(match):
    global svg_count, svg_failures
    source_ref = match.group("path")
    if source_ref in svg_cache:
        replacement = svg_cache[source_ref]
    else:
        svg_count += 1
        source = source_ref if os.path.isabs(source_ref) else os.path.join(input_dir, source_ref)
        png = os.path.join(assets_dir, f"_svg_{svg_count}.png")
        ok = False
        if rsvg and os.path.isfile(source):
            try:
                result = subprocess.run(
                    [
                        rsvg,
                        "-l",
                        "en-US,en",
                        "-w",
                        "2400",
                        "-a",
                        "-b",
                        "white",
                        "-o",
                        png,
                        source,
                    ],
                    capture_output=True,
                    timeout=90,
                )
                ok = result.returncode == 0 and os.path.isfile(png) and os.path.getsize(png) > 500
            except Exception:
                ok = False
        if ok:
            replacement = os.path.relpath(png, out_dir).replace(os.sep, "/")
        else:
            svg_failures += 1
            replacement = source_ref
        svg_cache[source_ref] = replacement
    return match.group("prefix") + replacement + match.group("suffix")


rendered = svg_pattern.sub(rasterize_svg, rendered)
open(out, "w", encoding="utf-8").write(rendered)
print(
    f"render_md: diagrams={diagram_count} failed={diagram_failures} "
    f"svgs={svg_count} svg_failed={svg_failures}"
)
if diagram_failures or svg_failures:
    sys.exit(1)
