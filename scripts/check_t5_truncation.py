#!/usr/bin/env python3
"""
check_t5_truncation.py — does CLaSP's 64-token text limit cut any caption?

models/clasp/model.py encodes captions with truncation=True, max_length=64.
A SUSHI caption is "shape sentence(s) + fluctuation sentence", so if a
caption runs past 64 T5 tokens the part that is cut is the fluctuation
sentence — exactly the clause a C4 swap replaces. This script counts, with
the same tokenizer the model uses, how many captions exceed the limit:

  (1) every caption in data/processed/pairs.jsonl, per dataset and split;
  (2) every caption_correct / caption_distractor in
      data/processed/probe1_items.jsonl, per component and condition.

A token count includes the EOS token the tokenizer appends, so a caption
is truncated iff its untruncated length is > 64.

Run from the repository root (needs data/ and transformers):
    python scripts/check_t5_truncation.py
Writes: results/analysis/t5_truncation_check.json
"""

import json
from collections import defaultdict
from pathlib import Path

from transformers import AutoTokenizer

TEXT_MODEL = "google-t5/t5-small"   # = ClaspConfig.text_model
MAX_LEN = 64                        # = max_length in ClaspModel.encode_text
PAIRS = Path("data/processed/pairs.jsonl")
ITEMS = Path("data/processed/probe1_items.jsonl")
OUT = Path("results/analysis/t5_truncation_check.json")


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def summarise(lengths):
    over = [n for n in lengths if n > MAX_LEN]
    return {"n": len(lengths), "n_over_limit": len(over),
            "max_tokens": max(lengths) if lengths else None}


def main():
    tok = AutoTokenizer.from_pretrained(TEXT_MODEL)
    n_tokens = lambda text: len(tok(text).input_ids)
    report = {"tokenizer": TEXT_MODEL, "max_length": MAX_LEN}

    by_split = defaultdict(list)
    for r in read_jsonl(PAIRS):
        by_split[f"{r['dataset']}|{r['split']}"].append(n_tokens(r["caption"]))
    report["pairs"] = {k: summarise(v) for k, v in sorted(by_split.items())}

    by_cell = defaultdict(list)
    for it in read_jsonl(ITEMS):
        for field in ("caption_correct", "caption_distractor"):
            key = f"{it['component']}|{it['condition']}|{field}"
            by_cell[key].append(n_tokens(it[field]))
    report["probe1_items"] = {k: summarise(v) for k, v in sorted(by_cell.items())}

    print(f"tokenizer {TEXT_MODEL}, limit {MAX_LEN} tokens (incl. EOS)\n")
    for section in ("pairs", "probe1_items"):
        print(f"[{section}]")
        for k, s in report[section].items():
            flag = "  <-- TRUNCATED" if s["n_over_limit"] else ""
            print(f"  {k:<55} n={s['n']:>6}  over={s['n_over_limit']:>5}  "
                  f"max={s['max_tokens']}{flag}")
        print()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
