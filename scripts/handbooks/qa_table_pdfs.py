#!/usr/bin/env python3
"""Verify the handbook tables that require targeted PDF layout treatment."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class TableCheck:
    slug: str
    name: str
    orientation: str
    anchors: tuple[str, ...]
    samples: tuple[str, ...]


CHECKS = (
    TableCheck(
        "01-frontend-cdn-supply-chain",
        "threat-model worksheet",
        "portrait",
        ("STRIDE Category", "Residual Risk (H/M/L)"),
        ("Wallet-connect script (CDN)", "Security review"),
    ),
    TableCheck(
        "01-frontend-cdn-supply-chain",
        "SBOM inventory",
        "portrait",
        ("Package / Action", "Pinned Version + Hash"),
        ("Ecosystem", "SBOM Component ID"),
    ),
    TableCheck(
        "01-frontend-cdn-supply-chain",
        "third-party script inventory",
        "portrait",
        ("Script / Widget", "Removal Candidate?"),
        ("Analytics vendor", "Data Accessible"),
    ),
    TableCheck(
        "02-dns-hosting-security",
        "DNS/ENS/IPFS asset register",
        "portrait",
        ("Controlling Party or Key", "Monitoring in Place"),
        ("Registrar account, hardware MFA", "Infra lead"),
    ),
    TableCheck(
        "03-employee-lifecycle-security",
        "equipment and account planning",
        "portrait",
        ("Standard hire", "Treasury, deploy-key, or admin hire"),
        ("Hardware security key", "Initial device geofence"),
    ),
    TableCheck(
        "03-employee-lifecycle-security",
        "role access template",
        "portrait",
        ("Role Infrastructure Code Communications Treasury",),
        ("Smart contract deployer", "Support or community manager"),
    ),
    TableCheck(
        "03-employee-lifecycle-security",
        "communications access template",
        "portrait",
        ("Default group at hire", "Approver for elevation"),
        ("Company email", "Domain registrar and DNS panel"),
    ),
    TableCheck(
        "05-hiring-remote-insider-dprk",
        "investigation RACI",
        "portrait",
        ("Task", "IT/Identity Admin", "Initial triage and evidence capture"),
        ("Executive Sponsor", "Legal hold and preservation scope"),
    ),
    TableCheck(
        "06-incident-response",
        "incident contact list",
        "portrait",
        ("Primary channel", "Escalation SLA", "Last verified"),
        ("Incident commander (on-call)", "Primary exchange security contact"),
    ),
    TableCheck(
        "08-sdk-security-testing",
        "offensive code-path analysis",
        "portrait",
        ("Entry point", "Example in an SDK", "Offensive check"),
        ("Transaction builder", "Native code execution"),
    ),
    TableCheck(
        "08-sdk-security-testing",
        "coordinated-disclosure timeline",
        "portrait",
        (
            "Phase Standard CVD target Active-exploitation target",
            "Registry takedown of malicious version",
        ),
        ("Confirm and triage", "Downstream notification"),
    ),
    TableCheck(
        "10-web3-attack-vectors-mapping",
        "TTP quick-reference matrix",
        "portrait",
        ("Technique (summary)", "Detection Signal", "Primary Mitigation"),
        ("User and Social", "compromised OSS package"),
    ),
    TableCheck(
        "10-web3-attack-vectors-mapping",
        "Web3 Attack Vectors Top 15 summary",
        "portrait",
        ("Primary Layer", "Handbook Chapter", "Representative Incident"),
        ("Multisig Hijacking", "Wrench Attacks and Physical Coercion"),
    ),
)


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def orientation(page) -> str:
    return "landscape" if float(page.mediabox.width) > float(page.mediabox.height) else "portrait"


def longest_single_letter_run(text: str) -> int:
    longest = current = 0
    for line in text.splitlines():
        token = line.strip()
        if re.fullmatch(r"[A-Za-z]", token):
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def outline_titles(items) -> list[str]:
    titles: list[str] = []
    for item in items:
        if isinstance(item, list):
            titles.extend(outline_titles(item))
        elif getattr(item, "title", None):
            titles.append(str(item.title))
    return titles


def link_data(reader: PdfReader) -> tuple[set[str], set[str], list[str]]:
    named = set(reader.named_destinations)
    external: set[str] = set()
    broken_internal: list[str] = []
    for page_number, page in enumerate(reader.pages, 1):
        for reference in page.get("/Annots", ()):
            annotation = reference.get_object()
            if annotation.get("/Subtype") != "/Link":
                continue
            destination = annotation.get("/Dest")
            action = annotation.get("/A")
            if action and action.get("/S") == "/URI":
                external.add(str(action.get("/URI")))
            elif action and action.get("/S") == "/GoTo":
                destination = action.get("/D")
            if isinstance(destination, str) and destination not in named:
                broken_internal.append(f"page {page_number}: {destination}")
    return named, external, broken_internal


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf_dir", type=Path)
    parser.add_argument("--baseline-dir", type=Path)
    args = parser.parse_args()

    failures: list[str] = []
    readers: dict[str, PdfReader] = {}
    page_text: dict[str, list[str]] = {}

    for check in CHECKS:
        if check.slug not in readers:
            reader = PdfReader(args.pdf_dir / f"{check.slug}.pdf")
            readers[check.slug] = reader
            page_text[check.slug] = [page.extract_text() or "" for page in reader.pages]

        reader = readers[check.slug]
        texts = page_text[check.slug]
        candidates = [
            index
            for index, text in enumerate(texts)
            if all(anchor.casefold() in clean(text).casefold() for anchor in check.anchors)
        ]
        if not candidates:
            failures.append(f"{check.slug}: {check.name}: header words are split or missing")
            continue

        candidate_text = clean("\n".join(texts[index] for index in candidates)).casefold()
        missing = [sample for sample in check.samples if sample.casefold() not in candidate_text]
        if missing:
            failures.append(
                f"{check.slug}: {check.name}: split or missing sample text {missing}"
            )

        bad_orientation = [
            index + 1
            for index in candidates
            if orientation(reader.pages[index]) != check.orientation
        ]
        if bad_orientation:
            failures.append(
                f"{check.slug}: {check.name}: wrong orientation on pages {bad_orientation}"
            )

        bad_runs = [
            (index + 1, longest_single_letter_run(texts[index]))
            for index in candidates
            if longest_single_letter_run(texts[index]) >= 4
        ]
        if bad_runs:
            failures.append(
                f"{check.slug}: {check.name}: character-by-character wrapping {bad_runs}"
            )

        print(
            f"{check.slug}: {check.name}: pages="
            f"{','.join(str(index + 1) for index in candidates)} "
            f"orientation={check.orientation} text=PASS wrap=PASS"
        )

    for slug, reader in readers.items():
        named, external, broken_internal = link_data(reader)
        outline = outline_titles(reader.outline)
        if not outline:
            failures.append(f"{slug}: document outline is missing")
        if broken_internal:
            failures.append(f"{slug}: broken internal links {broken_internal}")

        if args.baseline_dir:
            baseline = PdfReader(args.baseline_dir / f"{slug}.pdf")
            baseline_named, baseline_external, _ = link_data(baseline)
            baseline_outline = outline_titles(baseline.outline)
            if named != baseline_named:
                failures.append(f"{slug}: named destinations changed")
            if external != baseline_external:
                failures.append(f"{slug}: external link targets changed")
            if outline != baseline_outline:
                failures.append(f"{slug}: document outline changed")

        print(
            f"{slug}: structure: outline={len(outline)} destinations={len(named)} "
            f"external-links={len(external)} internal-targets=PASS"
        )

    if failures:
        print("QA_RESULT FAIL")
        for failure in failures:
            print(failure)
        raise SystemExit(1)
    print(f"QA_RESULT PASS tables={len(CHECKS)} pdfs={len(readers)}")


if __name__ == "__main__":
    main()
