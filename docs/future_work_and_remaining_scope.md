# Future work & remaining scope — decision record (2026-08-17)

**Status of this document:** decision by Ranyi, 2026-08-17, following Claude's
recommendation in the ChatTS close-out chat. One item below is
**PENDING SUPERVISOR AGREEMENT** and is marked as such. Everything else is
settled. Future writing-stage chats should follow this file when drafting the
future-work / limitations sections and should NOT re-open these scope
decisions without saying so explicitly.

**Context:** as of 2026-08-16 the execution program is COMPLETE — all four
models (CLaSP, TRACE, ChatTS, text-embedding-3-large floor) × all three
probes, scored and recorded (state doc rev. 18 §2; handoff header xv). The
items below are everything that was ever on the optional/remaining list.

---

## Decision: not executed — written up as future work

**FW-1. Probe 1 on the TRUCE substrate (free-form captions).**
Was always the secondary Probe-1 target (proposal + state doc §4: parser over
free-form captions, parse-coverage reported, ~100 parses manually validated,
selection bias stated). NOT executed. Write-up treatment:
- One "future work" paragraph: extending the component-swap probe to
  free-form natural-language captions, with the parser + parse-coverage +
  human-validation protocol as designed.
- One limitations sentence: the Probe-1 cross-model matrix rests on
  structured/label-derived caption substrates (SUSHI grammar; TRACE narrative
  grammar); generalisation to free-form captions is designed but untested.
- ⚠ **PENDING SUPERVISOR AGREEMENT** — say one line in the next supervisor
  conversation ("I plan to leave the TRUCE Probe-1 substrate as future
  work"). If the supervisor wants it executed, that re-opens scope; record
  the outcome here.

**FW-2. TRACE N5 location mechanism (climate-inference vs station-memorisation).**
The designed negative control detected location at 0.92 overall and 0.900 on
the 40 place-name-only swaps (frame and length confounds ruled out) — so
location IS signal-inferable to TRACE; the mechanism is open. NOT chased.
Write-up treatment:
- This is NOT only future work: the finding itself is measured and goes in
  the TRACE results/discussion as the reframed-control story (state doc §2).
- One discussion paragraph on the open mechanism question + one future-work
  sentence (a discriminating experiment, e.g. climate-plausible synthetic
  series vs memorised-station probes).
- Never describe N5 as a negative control anywhere in the thesis.

**FW-3. TRACE restricted option-(a) "garnish" (downsampled-SUSHI Probe 1 on
surviving components).** NOT executed; deliberately decorative. Write-up
treatment: at most one future-work sentence; may be dropped entirely. The
two-walled C4 finding (substrate loss at 186 points + N4 unbuildable-clean)
stands on its own in the TRACE chapter and does not need this run.

**FW-4. One-page CLaSP baseline report.** Dissolved into the methods chapter
— not future work, not a separate task, nothing to mention.

---

## Decision: MUST happen during writing (not optional)

**W-1. Literature verification queue** (handoff §5). The unverified cited
facts — including MMTS-Bench's ">0.95 Align ceiling" and "240 QA pairs", and
the TS-Haystack venue — must be source-verified (alphaXiv) before they appear
in thesis prose, or dropped/marked unverified. This is the same discipline
the thesis preaches; budget an hour or two. The verified-facts table (state
doc §6.1) lists what is already pinned and what carries ⚠ marks.

---

## Standing write-up reminders that intersect with future work

These are NOT new decisions — they are pointers to already-pinned caveats
that the future-work/limitations sections must not contradict:

- ChatTS claims are conditional on its capability level (SUSHI 0.726; TRUCE
  WEAK-VIABLE 0.622, borderline argued): "no Probe-3 shortcut" is always
  "no shortcut detected at its capability level". C3 (periodic waveform) is
  VOID for ChatTS — no read, so nothing to future-work about it beyond the
  viability statement.
- The SUSHI width-limited Probe-3 contrasts (rung2↔gaussian, fivenum↔rung2
  at n=140) are quoted as inconclusive-by-width, never as equivalence; a
  larger-n replication is a legitimate future-work sentence.
- Thin cells always quoted with their n (TRUCE invariant 18; SUSHI invariant
  4, ambiguous 5, degenerate 1).
- Pooled numbers are never load-bearing; strata always (TRACE pooled profile
  is a documented mixture artifact).
- Dataset-defect notes for limitations: SUSHI "Large part," truncation;
  TRUCE '{}' caption ×7 + junk; TRUCE-synth duplicate signals (~2% R@1
  coin-flip for any model).

---

*Repo note: the clone is canonical for governing docs. This file should also
be committed to `docs/` in `RaneeLuo/Thesis-probes` so the two copies cannot
drift; if the supervisor decision on FW-1 changes anything, update both.*
