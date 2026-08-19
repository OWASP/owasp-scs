#!/usr/bin/env python3
"""Verify printable-checklist page boundaries in staged handbook PDFs."""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
import unicodedata
from pathlib import Path

from pypdf import PdfReader


BOOKS = {
    "01-frontend-cdn-supply-chain": "CDN and Front-End Supply Chain Security",
    "02-dns-hosting-security": "DNS and Hosting Security",
    "03-employee-lifecycle-security": "Employee Lifecycle Security",
    "04-evm-forensics-defi-recovery": "EVM Forensics and DeFi Recovery",
    "05-hiring-remote-insider-dprk": "Hiring, Remote Work, and Insider Threat",
    "06-incident-response": "Incident Response",
    "07-infrastructure-security": "Infrastructure Security",
    "08-sdk-security-testing": "SDK Security Testing",
    "09-ux-security": "UX Security",
    "10-web3-attack-vectors-mapping": "Web3 Attack Vectors Mapping",
    "11-opsec-in-web3": "Web3 Operational Security",
}


def normalize(value: str) -> str:
    value = (
        unicodedata.normalize("NFKD", value)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def parse_heading(line: str):
    match = re.match(r"^(#{1,6})\s+(.*?)(?:\s+\{[^{}]*\})?\s*$", line)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def prepared_boundaries(repo_root: Path, slug: str, title: str):
    source = repo_root / "docs" / "handbooks" / slug
    files = [source / "index.md", *sorted(source.glob("part*.md")), source / "references.md"]
    raw = "\n\n".join(
        source_file.read_text(encoding="utf-8").replace("\r\n", "\n")
        for source_file in files
    )
    with tempfile.TemporaryDirectory(dir=repo_root / "tmp" / "pdfs") as work:
        work_path = Path(work)
        raw_path = work_path / "raw.md"
        prepared_path = work_path / "prepared.md"
        raw_path.write_text(raw, encoding="utf-8")
        subprocess.run(
            [
                "python3",
                str(repo_root / "scripts" / "handbooks" / "book_prep.py"),
                str(raw_path),
                str(prepared_path),
                str(work_path / "header.html"),
                str(work_path / "cover.html"),
                title,
                "#17a9d6",
                "#0e6f8e",
                "cover.png",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        prepared = prepared_path.read_text(encoding="utf-8").splitlines()

    starts = []
    ends = []
    for line in prepared:
        parsed = parse_heading(line)
        if not parsed:
            continue
        if ".printable-checklist-start" in line:
            starts.append(parsed)
        if ".after-printable-checklist" in line:
            ends.append(parsed)
    return starts, ends


def extract_page_data(reader: PdfReader):
    pages = []
    for page_number, page in enumerate(reader.pages, 1):
        heading_fragments = []
        body_fragments = []

        def visit(text, _cm, text_matrix, _font, font_size):
            value = normalize(text)
            y_position = float(text_matrix[5])
            # Running headers and page numbers are outside this body band.
            # Tracking body fragments catches pages that look blank even when
            # those repeated furniture elements still extract as text.
            if value and 90 < y_position < 1050:
                body_fragments.append(value)
            if font_size >= 15.5 and len(value) >= 4:
                heading_fragments.append(
                    (page_number, y_position, float(font_size), value)
                )

        text = page.extract_text(visitor_text=visit) or ""
        pages.append((text, heading_fragments, body_fragments))
    return pages


def heading_location(page_data, title: str):
    wanted = normalize(title)
    prefix = " ".join(wanted.split()[:4])
    hits = [
        fragment
        for _text, fragments, _body_fragments in page_data
        for fragment in fragments
        if fragment[3].startswith(prefix) or wanted.startswith(fragment[3])
    ]
    if not hits:
        return None
    return min(hits, key=lambda hit: (abs(len(hit[3]) - len(wanted)), hit[0]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_dir", type=Path)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    pdf_dir = args.pdf_dir.resolve()

    failures = []
    total_pages = 0
    total_starts = 0
    total_end_headings = 0

    for slug, title in BOOKS.items():
        starts, ends = prepared_boundaries(repo_root, slug, title)
        reader = PdfReader(pdf_dir / f"{slug}.pdf")
        page_data = extract_page_data(reader)
        total_pages += len(reader.pages)

        blank_pages = []
        for page_number, (_page_text, _fragments, body_fragments) in enumerate(
            page_data[1:], 2
        ):
            if not body_fragments:
                blank_pages.append(page_number)
        if blank_pages:
            failures.append(f"{slug}: blank pages {blank_pages}")

        a4 = all(
            any(
                abs(float(page.mediabox.width) - width) < 0.1
                and abs(float(page.mediabox.height) - height) < 0.1
                for width, height in (
                    (595.276, 841.89),
                    (841.89, 595.276),
                )
            )
            for page in reader.pages
        )
        if not a4:
            failures.append(f"{slug}: contains a non-A4 page")

        bad_starts = []
        for _level, name in starts:
            location = heading_location(page_data, name)
            if location is None or location[1] > 180:
                bad_starts.append((name, location))
        if bad_starts:
            failures.append(f"{slug}: bad checklist starts {bad_starts}")

        bad_ends = []
        for level, name in ends:
            if level == 1:
                continue
            location = heading_location(page_data, name)
            if location is None or location[1] > 180:
                bad_ends.append((name, location))
        if bad_ends:
            failures.append(f"{slug}: bad post-checklist starts {bad_ends}")

        total_starts += len(starts)
        total_end_headings += len(ends)
        print(
            f"{slug}: pages={len(reader.pages)} starts={len(starts)} "
            f"ends={len(ends)} start-top=PASS end-top=PASS "
            f"blank={len(blank_pages)} A4=PASS"
        )

    print(
        f"TOTAL pages={total_pages} checklist-starts={total_starts} "
        f"end-boundaries={total_end_headings}"
    )
    if failures:
        print("QA_RESULT FAIL")
        for failure in failures:
            print(failure)
        raise SystemExit(1)
    print("QA_RESULT PASS")


if __name__ == "__main__":
    main()
