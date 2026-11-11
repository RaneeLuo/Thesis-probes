#!/usr/bin/env python3
"""Pre-upload checks for the FMTS camera-ready.

Usage:
    python3 check_camera_ready.py [main.tex] [main.pdf] [--limit 4]

Either argument may be omitted (pass the .tex, the .pdf, or both).
Checks:
  * .tex  - placeholders / TODOs, leftover anonymous author block, missing 'final'
            style option, \\cite keys missing from the .bib files it loads.
  * .log  - undefined references/citations, overfull boxes (if main.log exists).
  * .pdf  - total pages and the page on which the references start, so the
            main-text page count can be compared with the limit.
Exit code 1 if any HARD problem is found. Needs `pdftotext` (poppler) for PDFs.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDERS = re.compile(
    r"TODO|FIXME|XXX|PLACEHOLDER|CITATION NEEDED|\?\?\?|verify this|lorem ipsum",
    re.IGNORECASE,
)
ANON = re.compile(r"Anonymous|Anonymi[sz]ed|anonymous\.4open", re.IGNORECASE)
# Submission PDFs carry line numbers, e.g. "142   References".
REF_HEADINGS = re.compile(r"^\s*(?:\d+\s+)?(References|Bibliography)\s*$", re.MULTILINE)


def strip_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in text.splitlines())


def check_tex(tex: Path, hard: list, soft: list) -> None:
    raw = tex.read_text(encoding="utf-8", errors="replace")
    body = strip_comments(raw)

    for i, line in enumerate(raw.splitlines(), 1):
        if PLACEHOLDERS.search(line):
            soft.append(f"{tex.name}:{i}: placeholder/TODO: {line.strip()[:100]}")

    author = re.search(r"\\author\{(.*?)\n\}", body, re.S) or re.search(r"\\author\{(.*)", body)
    if author is None:
        hard.append("no \\author{...} block found")
    elif ANON.search(author.group(1)):
        hard.append("author block still looks anonymous")
    for i, line in enumerate(body.splitlines(), 1):
        if ANON.search(line) and "\\author" not in line:
            soft.append(f"{tex.name}:{i}: 'anonymous' wording outside author block: {line.strip()[:100]}")

    style = re.search(r"\\usepackage(\[[^\]]*\])?\{(neurips_\d{4})\}", body)
    if style is None:
        soft.append("no \\usepackage{neurips_YYYY} line found - check the template")
    else:
        opts = style.group(1) or ""
        if style.group(2) != "neurips_2026":
            hard.append(f"style is {style.group(2)}, expected neurips_2026")
        if "final" not in opts:
            hard.append(f"style options {opts or '(none)'} lack 'final' - still the anonymous submission layout")
        if "preprint" in opts:
            soft.append("'preprint' option set - camera-ready normally uses 'final'")

    keys = set()
    for m in re.finditer(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}", body):
        keys.update(k.strip() for k in m.group(1).split(",") if k.strip())
    bibs = []
    for m in re.finditer(r"\\(?:bibliography|addbibresource)\{([^}]*)\}", body):
        for name in m.group(1).split(","):
            p = tex.parent / (name.strip() if name.strip().endswith(".bib") else name.strip() + ".bib")
            bibs.append(p)
    bib_keys = set()
    for p in bibs:
        if p.exists():
            bib_keys.update(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", p.read_text(encoding="utf-8", errors="replace")))
        else:
            soft.append(f"bibliography file not found: {p}")
    if bibs and bib_keys:
        missing = sorted(keys - bib_keys)
        if missing:
            hard.append(f"cite keys not in .bib: {', '.join(missing)}")
        unused = sorted(bib_keys - keys)
        if unused:
            soft.append(f"{len(unused)} .bib entries never cited (fine if \\nocite is intended)")
    print(f"[tex] {len(keys)} distinct citation keys, {len(bib_keys)} .bib entries")

    log = tex.with_suffix(".log")
    if log.exists():
        text = log.read_text(encoding="utf-8", errors="replace")
        undefined = set(re.findall(r"(?:Reference|Citation) `([^']+)' .*undefined", text))
        if undefined:
            hard.append(f"undefined references/citations in log: {', '.join(sorted(undefined))}")
        overfull = re.findall(r"Overfull \\hbox \((\d+\.?\d*)pt too wide\)", text)
        big = [float(x) for x in overfull if float(x) > 5]
        if big:
            soft.append(f"{len(big)} overfull boxes wider than 5pt (max {max(big):.1f}pt) - text sticks into the margin")
    else:
        soft.append(f"no {log.name}; compile first to check undefined references")


def check_pdf(pdf: Path, limit: float, hard: list, soft: list) -> None:
    try:
        out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        soft.append("pdftotext not installed; skipped PDF checks")
        return
    pages = out.split("\f")
    if pages and not pages[-1].strip():
        pages = pages[:-1]
    ref_page = next((i + 1 for i, p in enumerate(pages) if REF_HEADINGS.search(p)), None)
    print(f"[pdf] {len(pages)} pages total")
    if ref_page is None:
        soft.append("could not find a 'References' heading; count main-text pages by eye")
        return
    # References usually start mid-page, so main text ends on (or just before) ref_page.
    print(f"[pdf] references start on page {ref_page}")
    if ref_page > limit + 1:
        hard.append(f"main text exceeds {limit:g} pages: references start on page {ref_page}")
    elif ref_page == limit + 1:
        soft.append(
            f"references start on page {ref_page}: OK only if page {ref_page} begins with the References "
            f"heading (no main text on it) - look at the page"
        )
    else:
        print(f"[pdf] main text fits within {limit:g} pages")
    first = pages[0]
    if ANON.search(first):
        hard.append("page 1 of the PDF still contains 'Anonymous'")
    if re.search(r"Submitted to|Do not distribute", first, re.IGNORECASE):
        hard.append("page 1 footer still says 'Submitted to ... / Do not distribute' - style not in final mode")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="main .tex and/or compiled .pdf")
    ap.add_argument("--limit", type=float, default=4, help="main-text page limit (default 4)")
    args = ap.parse_args()

    hard, soft = [], []
    for f in map(Path, args.files):
        if not f.exists():
            hard.append(f"file not found: {f}")
        elif f.suffix == ".tex":
            check_tex(f, hard, soft)
        elif f.suffix == ".pdf":
            check_pdf(f, args.limit, hard, soft)
        else:
            soft.append(f"ignored {f} (not .tex or .pdf)")

    for label, items in (("HARD", hard), ("CHECK", soft)):
        for item in items:
            print(f"{label}: {item}")
    print("RESULT:", "problems found" if hard else "no hard problems (still review the CHECK lines)")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
