"""
clasp_c4_certified_gap.py — CLaSP's C4 random / swap / gap on the 738
census-certified swaps and their matched random controls, per checkpoint and
pooled over the three checkpoints.

WHY. census_c4_reanalysis.py re-scored only the SWAP side of the certified
items. Its random figure (random_condition_context.acc_on_valid_signals,
0.9695) is context only: every C4 random item on the 237 certified signals
(983 per seed), including the controls of swaps the census removed. It reports
no gap. The Table 4.2 row needs the paired comparison on the certified
population: each certified swap against the random control that shares its
pair_key (same signal, same correct caption), as already done for ChatTS
(regrade_chatts_c4_census.py) and TRACE N3 (n3_census_verdict.py followed by
analyze_probe1_stats.py). Removing a swap removes its matched control.

STATISTICS reuse analyze_probe1_stats.py unchanged: per_signal_counts and
bootstrap (unit = signal, items pooled, 10,000 resamples), and holm. Each cell
draws from its own fresh default_rng(0), so its interval does not depend on
which cells were computed before it. (analyze_probe1_stats.py shares one RNG
stream across all seed x component cells; run on a certified per-item file it
gives the same point values and interval endpoints within 0.003 of these.)
  per checkpoint   seeds 42 / 43 / 44, one cell each
  pooled           the three checkpoints' items for a signal pooled before
                   resampling; this is the "averaged over the three
                   checkpoints" figure, and its swap interval matches
                   census_c4_reanalysis.json
Holm: within each seed, the certified C4 p_gap replaces the all-990 C4 p_gap
in the five-component family taken from probe1_statistics.json.

GATES (hard stop on failure)
  G1  census sheet: 863 rows, clean y/n on q1-q3, exactly 738 valid
      (same validity rule as census_c4_reanalysis.py)
  G2  join: every valid census row's pair_key
      (C4_fluctuation_type|{sample_id}|{swap_to}) has exactly one swap and one
      random record in each of the three seeds, and the swap record's
      sample_id / swap_from / swap_to equal the census row's
  G3  reproduction: certified swap accuracy per seed and pooled equals
      c4_census_reanalysis.json (census_valid.per_seed / .acc) to 1e-12, with
      237 signals; the unmatched random context reproduces
      random_condition_context.acc_on_valid_signals to 1e-12

Run from repo root:
    python scripts/clasp_c4_certified_gap.py

Reads:  results/analysis/pinning_spotcheck_sequential.csv   (filled census)
        results/experiments/probe1_clasp_per_item.jsonl
        results/experiments/probe1_statistics.json           (Holm family)
        results/analysis/c4_census_reanalysis.json           (G3 reference)
Writes: results/analysis/clasp_c4_certified_gap.json
"""

from __future__ import annotations
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

from analyze_probe1_stats import bootstrap, holm, per_signal_counts

CENSUS = Path("results/analysis/pinning_spotcheck_sequential.csv")
PER_ITEM = Path("results/experiments/probe1_clasp_per_item.jsonl")
STATS = Path("results/experiments/probe1_statistics.json")
CENSUS_REANALYSIS = Path("results/analysis/c4_census_reanalysis.json")
OUT = Path("results/analysis/clasp_c4_certified_gap.json")

COMP = "C4_fluctuation_type"
SEEDS = ["42", "43", "44"]
EXPECT_VALID, EXPECT_TOTAL, EXPECT_SIGNALS = 738, 863, 237
N_BOOT, BOOT_SEED, MARGIN, ALPHA = 10000, 0, 0.05, 0.05
QCOLS = ["q1_grammatical", "q2_asserts_swap_to", "q3_not_still_true"]


def die(msg):
    print(f"\nGATE FAILED: {msg}")
    sys.exit(1)


def cell(recs):
    """analyze_probe1_stats statistics for one cell, with a fresh RNG."""
    counts = per_signal_counts(recs)
    st = bootstrap(counts, N_BOOT, np.random.default_rng(BOOT_SEED))
    st["n_items_per_condition"] = sum(r["condition"] == "swap" for r in recs)
    lo, hi = st["gap_ci90"]
    st["equivalence_margin"] = MARGIN
    st["equivalent_to_zero"] = bool(lo > -MARGIN and hi < MARGIN)
    diffs = np.array([cr / nr - cs / ns
                      for cs, ns, cr, nr in counts.values() if ns and nr])
    st["mean_signal_level_gap"] = float(diffs.mean())
    try:
        from scipy.stats import wilcoxon
        st["wilcoxon_p"] = float(wilcoxon(diffs).pvalue)
    except ImportError:
        st["wilcoxon_p"] = None
    return st


def main():
    # ------------------------------------------------------------------ G1
    with open(CENSUS, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) != EXPECT_TOTAL:
        die(f"G1: {len(rows)} census rows, expected {EXPECT_TOTAL}")
    norm = lambda v: str(v).strip().lower() if v is not None else ""
    if any(norm(r[c]) not in ("y", "n") for r in rows for c in QCOLS):
        die("G1: census rows without clean y/n on all three questions")
    valid = {f"{COMP}|{r['sample_id']}|{r['swap_to']}": r for r in rows
             if all(norm(r[c]) == "y" for c in QCOLS)}
    if len(valid) != EXPECT_VALID:
        die(f"G1: {len(valid)} valid pair keys, expected {EXPECT_VALID}")
    print(f"G1 pass — census {len(rows)} rows, {len(valid)} valid")

    # ------------------------------------------------------------------ G2
    recs = [json.loads(l) for l in open(PER_ITEM, encoding="utf-8")]
    c4 = [r for r in recs if r["component"] == COMP]
    cert = [r for r in c4 if r["pair_key"] in valid]
    seen = defaultdict(list)
    for r in cert:
        seen[(r["pair_key"], r["seed"], r["condition"])].append(r)
    for pk, row in valid.items():
        for s in SEEDS:
            for cond in ("swap", "random"):
                got = seen.get((pk, s, cond), [])
                if len(got) != 1:
                    die(f"G2: {pk} seed {s} {cond}: {len(got)} records")
            sw = seen[(pk, s, "swap")][0]
            if (sw["sample_id"], sw["swap_from"], sw["swap_to"]) != \
                    (row["sample_id"], row["swap_from"], row["swap_to"]):
                die(f"G2: swap record disagrees with census row for {pk}")
    print(f"G2 pass — {len(valid)} pair keys x {len(SEEDS)} seeds, one swap "
          f"and one matched random each ({len(cert)} records)")

    # ------------------------------------------------------------------ G3
    ref = json.load(open(CENSUS_REANALYSIS, encoding="utf-8"))
    ref_valid = ref["groups"]["census_valid"]
    for i, s in enumerate(SEEDS):
        a = np.mean([r["correct"] for r in cert
                     if r["seed"] == s and r["condition"] == "swap"])
        if abs(a - ref_valid["per_seed"][i]) > 1e-12:
            die(f"G3: seed {s} swap {a} != census_valid.per_seed[{i}] "
                f"{ref_valid['per_seed'][i]}")
    pooled_swap = np.mean([r["correct"] for r in cert
                           if r["condition"] == "swap"])
    if abs(pooled_swap - ref_valid["acc"]) > 1e-12:
        die(f"G3: pooled swap {pooled_swap} != census_valid.acc")
    sigs = {r["sample_id"] for r in cert}
    if len(sigs) != EXPECT_SIGNALS or ref_valid["n_signals"] != EXPECT_SIGNALS:
        die(f"G3: {len(sigs)} certified signals, expected {EXPECT_SIGNALS}")
    unmatched = float(np.mean([r["correct"] for r in c4
                               if r["condition"] == "random"
                               and r["sample_id"] in sigs]))
    n_unmatched = sum(r["condition"] == "random" and r["sample_id"] in sigs
                      for r in c4)
    ref_ctx = ref["random_condition_context"]["acc_on_valid_signals"]
    if abs(unmatched - ref_ctx) > 1e-12:
        die(f"G3: unmatched random context {unmatched} != {ref_ctx}")
    print("G3 pass — certified swap accuracy (per seed and pooled) and the "
          "unmatched random context reproduce c4_census_reanalysis.json")

    # --------------------------------------------------------------- cells
    per_seed = {f"seed{s}": cell([r for r in cert if r["seed"] == s])
                for s in SEEDS}
    pooled = cell(cert)
    pooled.pop("wilcoxon_p")   # significance is per seed (binding decision)
    pooled["n_records_per_condition"] = pooled["n_items_per_condition"]
    pooled["n_items_per_condition"] = EXPECT_VALID
    pooled["ci_vs_census_reanalysis_swap_ci95"] = {
        "census_c4_reanalysis": ref_valid["acc_ci95_signal_bootstrap"],
        "max_abs_dev": float(max(abs(a - b) for a, b in zip(
            pooled["acc_swap_ci95"], ref_valid["acc_ci95_signal_bootstrap"])))}

    # Holm within seed: certified C4 replaces all-990 C4 in the family
    fam = json.load(open(STATS, encoding="utf-8"))["per_seed_component"]
    for s in SEEDS:
        ps = {k.split("|", 1)[1]: v["p_gap"] for k, v in fam.items()
              if k.startswith(f"seed{s}|")}
        if len(ps) != 5 or COMP not in ps:
            die(f"Holm family for seed {s} incomplete: {sorted(ps)}")
        ps[COMP] = per_seed[f"seed{s}"]["p_gap"]
        adj = holm(ps)[COMP]
        per_seed[f"seed{s}"]["p_gap_holm"] = adj
        per_seed[f"seed{s}"]["significant"] = bool(adj < ALPHA)

    gaps = [per_seed[f"seed{s}"]["gap"] for s in SEEDS]

    # --------------------------------------------------------------- print
    print("\n" + "=" * 92)
    print("CLaSP C4 ON CERTIFIED SWAPS + MATCHED RANDOM CONTROLS "
          f"({EXPECT_VALID} items/condition, {EXPECT_SIGNALS} signals)")
    print("=" * 92)
    print(f"{'cell':<10}{'random':>8}{'swap':>8}{'95% CI':>18}"
          f"{'gap':>9}{'95% CI':>18}{'p(Holm)':>10}")
    for name, st in list(per_seed.items()) + [("pooled", pooled)]:
        cs = "[{:.3f}, {:.3f}]".format(*st["acc_swap_ci95"])
        cg = "[{:.3f}, {:.3f}]".format(*st["gap_ci95"])
        ph = f"{st['p_gap_holm']:.4f}" if "p_gap_holm" in st else "--"
        print(f"{name:<10}{st['acc_random']:>8.3f}{st['acc_swap']:>8.3f}"
              f"{cs:>18}{st['gap']:>+9.3f}{cg:>18}{ph:>10}")
    print(f"\ngap across checkpoints: mean {np.mean(gaps):+.3f}, "
          f"sd {np.std(gaps, ddof=1):.3f}")
    print(f"for contrast, unmatched random context on the same signals "
          f"(n={n_unmatched}): {unmatched:.4f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "script": "scripts/clasp_c4_certified_gap.py",
        "population": {
            "component": COMP,
            "n_items_per_condition": EXPECT_VALID,
            "n_signals": EXPECT_SIGNALS,
            "swap": "census-valid swaps (pinning_spotcheck_sequential.csv)",
            "random": "the random control sharing each certified swap's "
                      "pair_key; random distractors were never human-"
                      "validated"},
        "gates_passed": ["G1", "G2", "G3"],
        "bootstrap": {"n_boot": N_BOOT, "rng": f"fresh default_rng"
                      f"({BOOT_SEED}) per cell", "unit": "signal",
                      "functions": "analyze_probe1_stats.bootstrap"},
        "holm_family": "per seed: C1, C2, C3, C5 p_gap from "
                       "probe1_statistics.json + certified C4 p_gap",
        "per_checkpoint": per_seed,
        "pooled_three_checkpoints": pooled,
        "gap_across_checkpoints": {"mean": float(np.mean(gaps)),
                                   "sd": float(np.std(gaps, ddof=1))},
        "unmatched_random_context": {
            "acc": unmatched, "n_records": n_unmatched,
            "note": "all C4 random items on the certified signals, as in "
                    "c4_census_reanalysis.json; not the matched controls"},
    }, indent=2), encoding="utf-8")
    print(f"\nsaved -> {OUT}")


if __name__ == "__main__":
    main()
