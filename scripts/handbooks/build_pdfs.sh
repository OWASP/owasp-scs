#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HANDBOOK_ROOT="$REPO_ROOT/docs/handbooks"
FINAL_COVER_ROOT="$HANDBOOK_ROOT/covers-final"
HANDBOOK_SITE_BASE="${HANDBOOK_SITE_BASE:-https://scs.owasp.org/handbooks}"
CC_LICENSE_IMAGE="$REPO_ROOT/docs/assets/SCSVS/Images/CC-license.png"
PDF_TMP_ROOT="$REPO_ROOT/tmp/pdfs"
PDF_OUT_DIR="${PDF_OUT_DIR:-$PDF_TMP_ROOT/generated}"
PDF_LOG_DIR="$PDF_TMP_ROOT/logs"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [[ "$PYTHON_BIN" == "python3" && -x "$REPO_ROOT/venv/bin/python" ]]; then
  PYTHON_BIN="$REPO_ROOT/venv/bin/python"
fi

mkdir -p "$PDF_OUT_DIR" "$PDF_LOG_DIR"

find_mmdc() {
  if [[ -n "${MMDC_BIN:-}" && -x "${MMDC_BIN}" ]]; then
    printf '%s\n' "$MMDC_BIN"
    return
  fi
  if command -v mmdc >/dev/null 2>&1; then
    command -v mmdc
    return
  fi
  local candidate
  candidate="$(find "$HOME/.npm/_npx" \( -type f -o -type l \) -path '*/node_modules/.bin/mmdc' 2>/dev/null | head -n 1)"
  [[ -n "$candidate" ]] && printf '%s\n' "$candidate"
}

MMDC_BIN="$(find_mmdc)"
if [[ -z "$MMDC_BIN" ]]; then
  echo "Mermaid CLI (mmdc) was not found. Set MMDC_BIN to its executable path." >&2
  exit 2
fi

for dependency in pandoc weasyprint rsvg-convert pdfinfo; do
  if ! command -v "$dependency" >/dev/null 2>&1; then
    echo "Required build dependency is missing: $dependency" >&2
    exit 2
  fi
done

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Required Python interpreter is missing: $PYTHON_BIN" >&2
  exit 2
fi

if ! "$PYTHON_BIN" -c 'import pypdf' >/dev/null 2>&1; then
  echo "Required Python dependency is missing for $PYTHON_BIN: pypdf" >&2
  exit 2
fi

for build_input in "$SCRIPT_DIR/pdf_links.lua" "$SCRIPT_DIR/qa_pdf_links.py"; do
  if [[ ! -f "$build_input" ]]; then
    echo "Required handbook build input is missing: $build_input" >&2
    exit 2
  fi
done

BOOKS=(
  "01-frontend-cdn-supply-chain|CDN and Front-End Supply Chain Security|#17a9d6|#0e6f8e"
  "02-dns-hosting-security|DNS and Hosting Security|#12a594|#0b6b60"
  "03-employee-lifecycle-security|Employee Lifecycle Security|#d98a1f|#8a5410"
  "04-evm-forensics-defi-recovery|EVM Forensics and DeFi Recovery|#6e56e6|#43349a"
  "05-hiring-remote-insider-dprk|Hiring, Remote Work, and Insider Threat|#d6392f|#8e211b"
  "06-incident-response|Incident Response|#e2662a|#97401a"
  "07-infrastructure-security|Infrastructure Security|#3e63dd|#263f94"
  "08-sdk-security-testing|SDK Security Testing|#4fa31e|#2f6512"
  "09-ux-security|UX Security|#c79210|#855f0a"
  "10-web3-attack-vectors-mapping|Web3 Attack Vectors Mapping|#d62f86|#8e1b55"
  "11-opsec-in-web3|Web3 Operational Security|#b4892e|#6e5216"
)

pdf_cover_for_slug() {
  local slug="$1"
  printf '%s\n' "$FINAL_COVER_ROOT/$slug.png"
}

build_book() {
  local slug="$1" title="$2" accent="$3" accent_dark="$4"
  local source_dir="$HANDBOOK_ROOT/$slug"
  local cover
  cover="$(pdf_cover_for_slug "$slug")"
  local cover_name="cover.${cover##*.}"
  local output="$PDF_OUT_DIR/$slug.pdf"
  local log="$PDF_LOG_DIR/$slug.log"
  local work
  work="$(mktemp -d "$PDF_TMP_ROOT/${slug}.XXXXXX")"

  if [[ ! -f "$source_dir/index.md" || ! -f "$source_dir/references.md" || ! -f "$cover" || ! -f "$CC_LICENSE_IMAGE" ]]; then
    echo "[$slug] missing index, references, cover, or license artwork" | tee "$log" >&2
    rm -rf "$work"
    return 1
  fi

  cp -R "$source_dir/assets" "$work/assets"
  cp "$cover" "$work/$cover_name"
  cp "$CC_LICENSE_IMAGE" "$work/cc-by-sa.png"

  local files=("$source_dir/index.md")
  local part
  while IFS= read -r part; do files+=("$part"); done < <(find "$source_dir" -maxdepth 1 -type f -name 'part*.md' | sort -V)
  files+=("$source_dir/references.md")

  : > "$work/_combined_raw.md"
  local source
  for source in "${files[@]}"; do
    sed 's/\r$//' "$source" >> "$work/_combined_raw.md"
    printf '\n\n' >> "$work/_combined_raw.md"
  done

  (
    set -e
    echo "[$slug] preprocessing current website sources"
    if ! "$PYTHON_BIN" "$SCRIPT_DIR/book_prep.py" \
      "$work/_combined_raw.md" "$work/_combined.md" "$work/_header.html" "$work/_cover.html" \
      "$title" "$accent" "$accent_dark" "$cover_name"; then
      echo "[$slug] Markdown preprocessing failed" >&2
      exit 1
    fi
    echo "[$slug] rendering Mermaid and SVG figures"
    if ! "$PYTHON_BIN" "$SCRIPT_DIR/render_md.py" \
      "$work/_combined.md" "$work/_rendered.md" "$work/assets" \
      "$SCRIPT_DIR/pptr.json" "$MMDC_BIN"; then
      echo "[$slug] diagram rendering failed" >&2
      exit 1
    fi
    echo "[$slug] composing A4 PDF"
    if ! pandoc "$work/_rendered.md" \
      --from=markdown+fenced_divs-implicit_figures \
      --lua-filter="$SCRIPT_DIR/pdf_links.lua" \
      --metadata=handbook-slug:"$slug" \
      --metadata=handbook-site-base:"$HANDBOOK_SITE_BASE" \
      --pdf-engine=weasyprint \
      --standalone \
      --toc \
      --toc-depth=2 \
      -H "$work/_header.html" \
      -B "$work/_cover.html" \
      -c "$SCRIPT_DIR/pdf.css" \
      --resource-path="$work" \
      -o "$output" 2>&1 | tee "$work/_pandoc.log"; then
      echo "[$slug] Pandoc/WeasyPrint composition failed" >&2
      exit 1
    fi
    if grep -Eq 'No anchor .* for internal URI reference' "$work/_pandoc.log"; then
      echo "[$slug] unresolved internal PDF hyperlink; refusing to publish" >&2
      exit 1
    fi
    if ! "$PYTHON_BIN" "$SCRIPT_DIR/qa_pdf_links.py" "$output"; then
      echo "[$slug] PDF hyperlink QA failed" >&2
      exit 1
    fi
    if ! pdfinfo "$output" | awk -F: -v slug="$slug" '/^Pages:|^Page size:|^File size:/ {gsub(/^[[:space:]]+/, "", $2); print "[" slug "] " $1 ":" $2}'; then
      echo "[$slug] PDF metadata inspection failed" >&2
      exit 1
    fi
  ) > >(tee "$log") 2>&1
  local rc=$?

  rm -rf "$work"
  if [[ $rc -ne 0 || ! -s "$output" ]]; then
    echo "[$slug] FAILED (see $log)" >&2
    rm -f "$output"
    return 1
  fi
  echo "[$slug] BUILT $output"
}

requested=("$@")
failures=0
for entry in "${BOOKS[@]}"; do
  IFS='|' read -r slug title accent accent_dark <<< "$entry"
  if [[ ${#requested[@]} -gt 0 ]]; then
    include=0
    for requested_slug in "${requested[@]}"; do
      [[ "$requested_slug" == "$slug" ]] && include=1
    done
    [[ $include -eq 0 ]] && continue
  fi
  build_book "$slug" "$title" "$accent" "$accent_dark"
  build_rc=$?
  if [[ $build_rc -ne 0 ]]; then
    failures=$((failures + 1))
  fi
done

if [[ $failures -ne 0 ]]; then
  echo "$failures handbook PDF build(s) failed." >&2
  exit 1
fi

echo "All selected handbook PDFs built in $PDF_OUT_DIR"
