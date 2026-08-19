#!/usr/bin/env python3
"""Fail when handbook PDFs contain unsafe or machine-local hyperlinks."""

from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path
from urllib.parse import urlsplit

from pypdf import PdfReader


ALLOWED_URI_SCHEMES = {"http", "https", "mailto"}
UNSAFE_ACTIONS = {"/Launch", "/GoToR"}


def pdf_inputs(arguments: list[Path]) -> list[Path]:
    result: list[Path] = []
    for argument in arguments:
        if argument.is_dir():
            result.extend(sorted(argument.glob("*.pdf")))
        elif argument.suffix.lower() == ".pdf":
            result.append(argument)
        else:
            raise ValueError(f"Not a PDF or directory: {argument}")
    unique = list(dict.fromkeys(path.resolve() for path in result))
    if not unique:
        raise ValueError("No PDFs found")
    return unique


def is_local_hostname(hostname: str | None) -> bool:
    if hostname is None:
        return False
    normalized = hostname.lower().rstrip(".")
    if normalized == "localhost" or normalized.endswith(".localhost"):
        return True
    try:
        return ipaddress.ip_address(normalized).is_loopback
    except ValueError:
        return False


def inspect_pdf(pdf_path: Path) -> tuple[list[str], dict[str, int]]:
    reader = PdfReader(pdf_path)
    failures: list[str] = []
    counts = {
        "pages": len(reader.pages),
        "annotations": 0,
        "internal": 0,
        "external": 0,
    }

    for page_number, page in enumerate(reader.pages, 1):
        for reference in page.get("/Annots") or []:
            annotation = reference.get_object()
            counts["annotations"] += 1

            if annotation.get("/Dest") is not None:
                counts["internal"] += 1

            action_reference = annotation.get("/A")
            if action_reference is None:
                continue

            action = action_reference.get_object()
            action_kind = str(action.get("/S") or "")
            if action_kind in UNSAFE_ACTIONS:
                failures.append(
                    f"{pdf_path.name}: page {page_number}: unsafe {action_kind} action"
                )
                continue

            if action_kind == "/GoTo":
                counts["internal"] += 1
                continue

            uri_value = action.get("/URI")
            if uri_value is None:
                continue

            uri = str(uri_value).strip()
            parsed_uri = urlsplit(uri)
            scheme = parsed_uri.scheme.lower()

            if scheme not in ALLOWED_URI_SCHEMES:
                failures.append(
                    f"{pdf_path.name}: page {page_number}: disallowed URI {uri!r}"
                )
                continue

            if scheme in {"http", "https"} and parsed_uri.hostname is None:
                failures.append(
                    f"{pdf_path.name}: page {page_number}: URI has no hostname {uri!r}"
                )
                continue

            if is_local_hostname(parsed_uri.hostname):
                failures.append(
                    f"{pdf_path.name}: page {page_number}: loopback URI {uri!r}"
                )
                continue

            counts["external"] += 1

    return failures, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    aggregate = {
        "pdfs": 0,
        "pages": 0,
        "annotations": 0,
        "internal": 0,
        "external": 0,
    }

    for pdf_path in pdf_inputs(args.inputs):
        pdf_failures, counts = inspect_pdf(pdf_path)
        failures.extend(pdf_failures)
        aggregate["pdfs"] += 1
        for key in ("pages", "annotations", "internal", "external"):
            aggregate[key] += counts[key]
        print(
            f"{pdf_path.name}: pages={counts['pages']} "
            f"annotations={counts['annotations']} internal={counts['internal']} "
            f"external={counts['external']}"
        )

    if failures:
        raise SystemExit("Unsafe PDF links found:\n" + "\n".join(failures))

    print(
        "PDF link QA passed: "
        f"pdfs={aggregate['pdfs']} pages={aggregate['pages']} "
        f"annotations={aggregate['annotations']} "
        f"internal={aggregate['internal']} external={aggregate['external']}; "
        "no file://, loopback, /Launch, or /GoToR targets"
    )


if __name__ == "__main__":
    main()
