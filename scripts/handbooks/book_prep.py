#!/usr/bin/env python3
"""Turn the current handbook web Markdown into print-ready book Markdown."""

import html
import re
import sys


def unwrap_fenced_checklists(source_lines):
    """Render copy-ready Markdown task-list templates as real PDF checklists."""
    result = []
    unwrapped = 0
    i = 0
    while i < len(source_lines):
        if re.match(r"^```markdown\s*$", source_lines[i], re.I):
            j = i + 1
            while j < len(source_lines) and not re.match(r"^```\s*$", source_lines[j]):
                j += 1
            if j < len(source_lines):
                block = source_lines[i + 1 : j]
                task_items = sum(
                    bool(re.match(r"^\s*-\s+\[[ xX]\]\s+\S", line)) for line in block
                )
                if task_items >= 2:
                    for line in block:
                        heading = re.match(r"^#{1,6}\s+(.*\S)\s*$", line)
                        if heading:
                            if result and result[-1] != "":
                                result.append("")
                            result.extend((f"**{heading.group(1)}**", ""))
                            continue
                        result.append(
                            line.replace("<script>", "&lt;script&gt;").replace(
                                "<link>", "&lt;link&gt;"
                            )
                        )
                    unwrapped += 1
                    i = j + 1
                    continue
        result.append(source_lines[i])
        i += 1
    return result, unwrapped


def strip_web_bookbar(lines):
    result = []
    i = 0
    removed = 0
    while i < len(lines):
        if re.search(r'<div\s+class="handbook-bookbar"', lines[i]):
            depth = 0
            while i < len(lines):
                depth += len(re.findall(r"<div\b", lines[i]))
                depth -= len(re.findall(r"</div>", lines[i]))
                i += 1
                if depth <= 0:
                    break
            removed += 1
            continue
        result.append(lines[i])
        i += 1
    return result, removed


def is_web_navigation_line(line):
    """Return whether a line is handbook navigation that is omitted in print."""
    return bool(
        re.match(r"^\[Back to (?:Handbook.* )?contents\]", line, re.I)
        or re.match(r"^\[Back to Handbook \d+ contents\]", line, re.I)
        or line.lstrip().startswith("[Next:")
        or "](../_SERIES_INDEX.md)" in line
        or "](../_CONVENTIONS.md)" in line
    )


def is_web_navigation_separator(lines, index):
    """Detect a thematic break used only to separate web-only navigation."""
    if not re.match(r"^\s*---\s*$", lines[index]):
        return False
    next_index = index + 1
    while next_index < len(lines) and not lines[next_index].strip():
        next_index += 1
    return next_index < len(lines) and is_web_navigation_line(lines[next_index])


def wrap_static_figures(lines):
    result = []
    wrapped = 0
    i = 0
    while i < len(lines):
        if re.match(r"^!\[[^\]]*\]\([^\n]+\)\s*$", lines[i]) and i + 1 < len(lines):
            caption = lines[i + 1]
            if re.match(r"^[*_](?:Figure|Diagram)\b.*[*_]\s*$", caption, re.I):
                result.extend(("::: {.figure-block}", lines[i], "", caption, ":::", ""))
                wrapped += 1
                i += 2
                continue
        result.append(lines[i])
        i += 1
    return result, wrapped


def wrap_marked_pdf_tables(lines):
    """Convert invisible source markers into PDF-only table containers."""
    result = []
    wrapped = {"fit": 0, "landscape": 0}
    i = 0
    while i < len(lines):
        marker = re.match(
            r"^\s*<!--\s*pdf-table:\s*(fit|landscape)\s*-->\s*$",
            lines[i],
            re.I,
        )
        if not marker:
            result.append(lines[i])
            i += 1
            continue

        treatment = marker.group(1).lower()
        if i + 2 >= len(lines) or not lines[i + 1].lstrip().startswith("|"):
            raise ValueError(
                f"pdf-table marker at source line {i + 1} is not followed by a table"
            )

        table_lines = []
        i += 1
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            table_lines.append(lines[i])
            i += 1

        result.append(f"::: {{.pdf-table-{treatment}}}")
        result.extend(table_lines)
        result.extend((":::", ""))
        wrapped[treatment] += 1

    return result, wrapped


def parse_heading(line):
    """Return a Markdown ATX heading's level and visible title."""
    match = re.match(
        r"^(#{1,6})\s+(.*?)(?:\s+\{[^{}]*\})?\s*$",
        line,
    )
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def add_heading_class(line, class_name):
    """Add a Pandoc heading class without disturbing existing attributes."""
    if f".{class_name}" in line:
        return line
    attributes = re.search(r"\s+\{([^{}]*)\}\s*$", line)
    if attributes:
        existing = attributes.group(1).strip()
        replacement = f" {{{existing} .{class_name}}}"
        return line[: attributes.start()] + replacement
    return f"{line} {{.{class_name}}}"


def mark_printable_checklists(lines):
    """Give every printable checklist clean page boundaries.

    A checklist is either explicitly named in its heading or is a section
    containing at least three Markdown task-list items. Every qualifying
    heading receives its own boundary even when it is nested inside a larger
    checklist appendix, because each child checklist must remain independently
    printable.
    """
    headings = []
    current_heading = None
    task_counts = {}

    for index, line in enumerate(lines):
        parsed = parse_heading(line)
        if parsed:
            level, title = parsed
            headings.append({"index": index, "level": level, "title": title})
            current_heading = len(headings) - 1
            continue
        if current_heading is not None and re.match(r"^\s*-\s+\[[ xX]\]\s+\S", line):
            task_counts[current_heading] = task_counts.get(current_heading, 0) + 1

    parent_start_marker = re.compile(
        r"^\s*<!--\s*pdf-checklist-start-at-parent\s*-->\s*$", re.I
    )
    candidates = []
    for heading_number, heading in enumerate(headings):
        if heading["level"] == 1:
            continue
        named_checklist = bool(re.search(r"\bchecklists?\b", heading["title"], re.I))
        task_checklist = task_counts.get(heading_number, 0) >= 3
        if named_checklist or task_checklist:
            heading["start_index"] = heading["index"]
            marker_index = heading["index"] - 1
            while marker_index >= 0 and not lines[marker_index].strip():
                marker_index -= 1
            if marker_index >= 0 and parent_start_marker.match(lines[marker_index]):
                parent = next(
                    (
                        prior
                        for prior in reversed(headings[:heading_number])
                        if prior["level"] < heading["level"]
                    ),
                    None,
                )
                if parent is None:
                    raise ValueError(
                        "pdf-checklist-start-at-parent marker has no parent heading"
                    )
                heading["start_index"] = parent["index"]
                separator_index = parent["index"] - 1
                while separator_index >= 0 and not lines[separator_index].strip():
                    separator_index -= 1
                if separator_index >= 0 and re.match(
                    r"^\s*---\s*$", lines[separator_index]
                ):
                    heading["parent_separator_index"] = separator_index
            candidates.append(heading)

    for candidate in candidates:
        candidate["scope_end"] = len(lines)
        for heading in headings:
            if (
                heading["index"] > candidate["index"]
                and heading["level"] <= candidate["level"]
            ):
                candidate["scope_end"] = heading["index"]
                break

    selected = candidates

    start_indexes = {heading["start_index"] for heading in selected}
    parent_separator_indexes = {
        heading["parent_separator_index"]
        for heading in selected
        if "parent_separator_index" in heading
    }
    end_indexes = set()
    for checklist in selected:
        if checklist["scope_end"] < len(lines):
            end_indexes.add(checklist["scope_end"])

    result = []
    for index, line in enumerate(lines):
        if parent_start_marker.match(line) or index in parent_separator_indexes:
            continue
        if index in start_indexes:
            line = add_heading_class(line, "printable-checklist-start")
        if index in end_indexes:
            line = add_heading_class(line, "after-printable-checklist")
        result.append(line)

    return result, [heading["title"] for heading in selected]


inp, out, header_out, cover_out, title, accent, accent_dark, cover_name = sys.argv[1:9]
source_lines = open(inp, encoding="utf-8").read().splitlines()
source_lines, removed_bookbars = strip_web_bookbar(source_lines)
lines, unwrapped_checklists = unwrap_fenced_checklists(source_lines)

out_lines = []
i = 0
while i < len(lines):
    line = lines[i]

    # Do not let a divider that belongs only to stripped web navigation flow
    # onto an otherwise empty PDF page before the next forced part opener.
    if is_web_navigation_separator(lines, i):
        i += 1
        continue

    # A few appendix closers keep the web navigation after a useful sentence.
    # Preserve the sentence while removing only the website-only link suffix.
    line = re.sub(
        r"\s*\[Back to (?:Handbook )?contents\]\(index\.md\)\s*\|\s*"
        r"\[Series index\]\(\.\./index\.md\)\s*$",
        "",
        line,
        flags=re.I,
    )

    if "page-break-after: always" in line:
        i += 1
        continue
    if is_web_navigation_line(line):
        i += 1
        continue
    if line.startswith("Part of the [OWASP SCS Handbook Series]"):
        i += 1
        continue
    if re.match(r"^#\s+OWASP SCS .*Handbook\s*$", line):
        i += 1
        continue
    if re.match(r"^##\s+Contents\s*$", line):
        i += 1
        while i < len(lines) and not re.match(r"^#{1,2}\s+\S", lines[i]):
            i += 1
        continue

    part = re.match(r"^#\s+Part\s+([IVXLCM0-9]+):\s*(.*\S)\s*$", line)
    if part:
        roman = {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
            5: "V",
            6: "VI",
            7: "VII",
            8: "VIII",
            9: "IX",
            10: "X",
        }
        number, label = part.groups()
        if number.isdigit():
            number = roman.get(int(number), number)
        out_lines.append(f"# Part {number}: {label} {{.part-opener}}")
        i += 1
        continue

    out_lines.append(line)
    i += 1

out_lines, wrapped_figures = wrap_static_figures(out_lines)
out_lines, wrapped_pdf_tables = wrap_marked_pdf_tables(out_lines)
out_lines, printable_checklists = mark_printable_checklists(out_lines)
body = "\n".join(out_lines).lstrip("\n")
escaped_title = html.escape(title, quote=True)

front = (
    "---\n"
    f'pagetitle: "{title.replace(chr(34), chr(92) + chr(34))}"\n'
    "lang: en\n"
    "---\n\n"
)
frontmatter = (
    "# Frontispiece {.frontispiece-title}\n\n"
    '<div class="frontmatter-kicker">OWASP SMART CONTRACT SECURITY PROJECT</div>\n\n'
    f'<div class="frontmatter-book-title">{escaped_title}</div>\n\n'
    "## About This Handbook {.frontmatter-section-title}\n\n"
    f"**{title}** is part of the OWASP Smart Contract Security Handbook Series. "
    "The series extends smart contract security beyond contract code into the people, "
    "process, application, infrastructure, and operational layers surrounding Web3 systems.\n\n"
    "Each handbook is designed as a defensive field reference for architects, engineers, "
    "security practitioners, incident responders, auditors, and organizational leaders. "
    "It complements the OWASP Smart Contract Security Verification Standard (SCSVS), "
    "Smart Contract Security Testing Guide (SCSTG), Smart Contract Weakness Enumeration "
    "(SCWE), Smart Contract Top 10, and SCS Checklist without replacing those resources.\n\n"
    '<div class="frontmatter-edition">\n'
    '<span class="frontmatter-edition__label">SERIES EDITION</span>\n'
    '<span class="frontmatter-edition__value">2026</span>\n'
    '</div>\n\n'
    "## Copyright and License {.frontmatter-section-title .frontmatter-new-page}\n\n"
    "Copyright &#169; 2026 The OWASP Foundation and contributors.\n\n"
    '<img class="cc-license-mark" src="cc-by-sa.png" '
    'alt="Creative Commons Attribution-ShareAlike 4.0 International" />\n\n'
    "This document is released under the "
    "[Creative Commons Attribution-ShareAlike 4.0 International License]"
    "(https://creativecommons.org/licenses/by-sa/4.0/). You may share and adapt the "
    "material with appropriate attribution and under the same license. For reuse or "
    "distribution, make the license terms clear and identify material changes.\n\n"
    "OWASP publications are community-developed educational resources. References to "
    "organizations, products, or services do not constitute endorsement, and the material "
    "is provided without warranty.\n\n"
    "## Author and Creative Credits {.frontmatter-section-title}\n\n"
    '::: {.frontmatter-credit-grid}\n'
    '::: {.frontmatter-credit-row}\n'
    '::: {.frontmatter-credit-card}\n'
    '<div class="frontmatter-credit-role">Project Lead</div>\n\n'
    '<div class="frontmatter-credit-name"><a href="https://www.linkedin.com/in/shashank-in/">Shashank | CredShields</a></div>\n\n'
    '<div class="frontmatter-credit-title">CEO and Co-Founder</div>\n'
    ':::\n\n'
    '::: {.frontmatter-credit-card}\n'
    '<div class="frontmatter-credit-role">Author | Project Maintainer</div>\n\n'
    '<div class="frontmatter-credit-name"><a href="https://www.linkedin.com/in/pratik-lagaskar/">Pratik Lagaskar</a></div>\n\n'
    '<div class="frontmatter-credit-title">Security Researcher</div>\n'
    ':::\n\n'
    ':::\n\n'
    '::: {.frontmatter-credit-row .frontmatter-credit-row--centered}\n'
    '::: {.frontmatter-credit-card}\n'
    '<div class="frontmatter-credit-role">Cover Page Designs</div>\n\n'
    '<div class="frontmatter-credit-name"><a href="https://www.linkedin.com/in/siddharth-neekher-340519117/">Siddharth Neekher</a></div>\n\n'
    '<div class="frontmatter-credit-title">Lead UI Designer @ CredShields</div>\n'
    ':::\n'
    ':::\n'
    ':::\n\n'
    '::: {.frontmatter-end}\n'
    ':::\n\n'
)
cover = (
    '<div class="cover-page">\n'
    f'<img src="{html.escape(cover_name, quote=True)}" alt="Cover of {escaped_title}" />\n'
    "</div>\n"
)
open(out, "w", encoding="utf-8").write(front + frontmatter + body + "\n")
open(cover_out, "w", encoding="utf-8").write(cover)

header = (
    "<style>\n"
    f":root {{ --accent: {accent}; --accent-dark: {accent_dark}; }}\n"
    f'@page {{ @top-left {{ content: "OWASP SCS  |  {escaped_title}"; }} }}\n'
    "</style>\n"
)
open(header_out, "w", encoding="utf-8").write(header)

print(
    "book_prep: "
    f"{len(source_lines)} source lines; {removed_bookbars} web bookbar removed; "
    f"{unwrapped_checklists} fenced checklists unwrapped; "
    f"{wrapped_figures} static figures grouped; "
    f"{wrapped_pdf_tables['fit']} fit tables and "
    f"{wrapped_pdf_tables['landscape']} landscape tables isolated; "
    f"{len(printable_checklists)} printable checklist sections isolated"
)
for checklist in printable_checklists:
    print(f"book_prep: printable checklist: {checklist}")
