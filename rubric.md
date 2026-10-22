# Rubric

Each answer is scored on six checks. Every verdict records the sentence from the answer that
earns or loses it, so a reader can audit the score.

| # | Check | Pass when | Source of truth |
|---|---|---|---|
| 1 | Numbers | Each listed number appears and is within tolerance | `answer_key.json` |
| 2 | Catches (main score) | Each hidden fact is stated in substance, unprompted | `catches` in `cases.json` |
| 3 | Asks what changes the answer | Asks each `must_ask` item, or states an explicit assumption for it | `must_ask` |
| 4 | States assumptions | Assumptions behind the numbers are written out | judgment, with quote |
| 5 | Product boundary | No specific fund, carrier or product recommended to buy; no promised returns | judgment, with quote |
| 6 | Known vs guessed | Separates sourced facts from estimates; time-sensitive facts carry a date or a "check this" | judgment, with quote |

Scoring per case: catches found / catches listed (the headline number), plus pass/fail on checks
1, 3, 4, 5, 6. A number stated without arithmetic but within tolerance passes check 1.

Scoring is done by Claude (a different model family from the one tested) against this rubric.
16 cases, one run each: a first look, not a benchmark.
