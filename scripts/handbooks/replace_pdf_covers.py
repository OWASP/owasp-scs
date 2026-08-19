#!/usr/bin/env python3
"""Replace handbook PDF page one with the approved full-bleed cover artwork."""

from __future__ import annotations

import argparse
import html
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from pypdf import PdfReader, PdfWriter


COVERS = {
    "01-frontend-cdn-supply-chain": "01-frontend-cdn-supply-chain.png",
    "02-dns-hosting-security": "02-dns-hosting-security.png",
    "03-employee-lifecycle-security": "03-employee-lifecycle-security.png",
    "04-evm-forensics-defi-recovery": "04-evm-forensics-defi-recovery.png",
    "05-hiring-remote-insider-dprk": "05-hiring-remote-insider-dprk.png",
    "06-incident-response": "06-incident-response.png",
    "07-infrastructure-security": "07-infrastructure-security.png",
    "08-sdk-security-testing": "08-sdk-security-testing.png",
    "09-ux-security": "09-ux-security.png",
    "10-web3-attack-vectors-mapping": "10-web3-attack-vectors-mapping.png",
    "11-opsec-in-web3": "11-opsec-in-web3.png",
}


def render_cover(cover_path: Path, output_path: Path) -> None:
    image_uri = html.escape(cover_path.resolve().as_uri(), quote=True)
    document = f"""<!doctype html>
<html><head><meta charset="utf-8"><style>
@page {{ size: A4; margin: 0; }}
html, body {{ width: 210mm; height: 297mm; margin: 0; overflow: hidden; }}
img {{ display: block; width: 210mm; height: 297mm; object-fit: cover;
       object-position: center center; }}
</style></head><body><img src="{image_uri}" alt=""></body></html>
"""
    subprocess.run(
        ["weasyprint", "-", str(output_path)],
        input=document.encode("utf-8"),
        check=True,
    )


def replace_first_page(pdf_path: Path, cover_path: Path, backup_dir: Path) -> int:
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / pdf_path.name
    if not backup_path.exists():
        shutil.copy2(pdf_path, backup_path)

    with tempfile.TemporaryDirectory(prefix=f"{pdf_path.stem}-", dir=backup_dir.parent) as work:
        work_path = Path(work)
        cover_pdf = work_path / "cover.pdf"
        candidate = work_path / pdf_path.name
        render_cover(cover_path, cover_pdf)

        source = PdfReader(pdf_path)
        original_pages = len(source.pages)
        writer = PdfWriter()
        writer.append(cover_pdf, import_outline=False)
        writer.append(source, pages=(1, original_pages), import_outline=True)
        if source.metadata:
            writer.add_metadata(
                {str(key): str(value) for key, value in source.metadata.items() if value is not None}
            )
        with candidate.open("wb") as stream:
            writer.write(stream)

        verified = PdfReader(candidate)
        if len(verified.pages) != original_pages:
            raise RuntimeError(
                f"{pdf_path.name}: page count changed from {original_pages} to "
                f"{len(verified.pages)}"
            )
        os.replace(candidate, pdf_path)
        return original_pages


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--backup-dir", type=Path)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    cover_root = repo_root / "docs" / "handbooks" / "covers-final"
    pdf_root = repo_root / "docs" / "handbooks" / "pdfs"
    backup_dir = (args.backup_dir or repo_root / "tmp" / "pdfs" / "before-final-covers").resolve()

    for slug, cover_name in COVERS.items():
        pdf_path = pdf_root / f"{slug}.pdf"
        cover_path = cover_root / cover_name
        if not pdf_path.is_file():
            raise FileNotFoundError(pdf_path)
        if not cover_path.is_file():
            raise FileNotFoundError(cover_path)
        page_count = replace_first_page(pdf_path, cover_path, backup_dir)
        print(f"{slug}: installed {cover_name} ({page_count} pages preserved)")


if __name__ == "__main__":
    main()
