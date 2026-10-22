# Scores: gemini-3.1-pro-preview, Google Search grounding on, run 2026-10-21 18:43 UTC
Baseline = case prompt only. Principle = same prompt with prompts/principle.txt as the system instruction.
Scored 2026-10-21 by Claude (a different model family) against rubric.md. ✓ = 1, ◐ = 0.5, ✗ = 0.
One run per case per arm; run-to-run variance not measured.

## Headline

| | Baseline | Principle |
|---|---|---|
| Hidden facts caught | 34.5 / 50 (69%) | 44.5 / 50 (89%) |
| Cases where it asked the user anything | 0 / 16 | 16 / 16 |
| Answer-key numbers matched (scorable) | 13 / 20 | 15 / 20 |

Flash comparison (gemini-3.6-flash, no search, baseline, the 9 cases that ran): 21 / 27 catches (78%). Pro baseline on the same 9 cases: 21.5 / 27 (80%).

## Catches by case

| Case | Baseline | Principle | What changed |
|---|---|---|---|
| c01 cash, retire at 50 | 2/4 | 4/4 | Principle adds health insurance ("+$24,000 out-of-pocket health insurance") and shows the draw rate (3.54%). Baseline: "You have likely already won the game," budget with no health insurance, assumes $300-400K/yr of new savings. Principle bonus: 40.8% tax drag on the money-market interest. |
| c02 annuity "no fees" | 3/3 | 3/3 | Both catch surrender + MVA, spread/commission, Treasury comparison, and the 59½ penalty. Principle flips the call: "I strongly rank keeping your money out of this annuity." |
| c03 Roth split | 3/3 | 3/3 | Same. Both state the 22% bracket as "$48,475 to $103,350" for 2026; those are 2025 thresholds (2026: $50,400 to $105,700). Harmless here. |
| c04 rent or sell condo | 3/3 | 3/3 | Both catch the 3-year exclusion window and recapture. Principle asks "Does your HOA allow renting?" and "Do you plan to move back?" |
| c05 in-plan conversion | 2/2 | 2/2 | Both catch no-withholding and the 24% spill. Principle uses the 2025 bracket top ($103,350) as 2026 and recommends converting "only up to $33,450"; correct 2026 room is $35,800, which the baseline got. |
| c06 conversions vs Medicare | 4/4 | 4/4 | Baseline: correct 2026 figures ($32,200 deduction, $218,000 threshold, $84,000 buffer), recommends waiting for the 12% years after the wife retires. Principle: names the Medicare threshold as "your primary speed limit" ($84,000 vs $109,600 of 22% room) and says "cap it at $84,000 this year," but drops the cheaper-later option. |
| c07 HYSA + teen account | 1.5/3 | 3/3 | Principle dates and sources rates ("As of October 2026... Wealthfront 3.55% base APY") and notes partner-bank FDIC. Baseline: "often... over 4.5% APY," undated; no FDIC mention. |
| c08 Mint replacement | 2/2 | 2/2 | Both read her rules and name aggregation as the hard part. Both flag that aggregators drop MCC codes. Baseline cites "Claude 3.5 Sonnet" as current. |
| c09 one-time advice | 1/2 | 2/2 | Principle: "I can also do this for you right now, for free," asks for the offer details, flags ISO/AMT and offer deadlines. Baseline: directories only. |
| c10 teen's income | 2/4 | 2/4 | Both catch UTMA control at majority and the $7,500 limit. Neither mentions UTMA's financial-aid treatment or 529-to-Roth rollovers. Principle adds FICA on his wages ($688.50). |
| c11 umbrella +25% | 1.5/3 | 3/3 | Baseline confirms the earlier AI's explanation ("spot-on") with no sources. Principle confirms with 7 sources, adds the $135/yr size and the underlying-limits question. |
| c12 $30K windfall | 1.5/3 | 2.5/3 | Baseline picks the ADU without asking. Principle asks the three deciding questions, flags state 529 deduction caps, then ranks on defaults. Its Roth-conversion math compares $245,894 of converted money against $59,014 of new money: not like for like. |
| c13 health spending total | 1.5/4 | 3/4 | Both total $2,606.47, counting drugstore purchases ($88.47) and Venmo "session" payments ($1,200) as medical; definite medical is $1,318.00. Both exclude the vet and gym. Principle asks what the total is for and flags HSA receipt rules and the 7.5% AGI floor. |
| c14 CPA bill | 2/3 | 2/3 | Both catch "an extension to file is not an extension to pay." Principle computes penalty ($204) and interest (~$205). Both judge the fee ("egregious fee padding") from no cited source; neither mentions the safe harbor. |
| c15 solo 401(k) | 2/4 | 3/4 | Principle asks whether there's a W-2 401(k) (shared $24,500 limit). Neither mentions Form 5500-EZ. Ascensus fees differ between runs ("$20 per participant + $20 per fund" vs "$250 per participant"). |
| c16 401(k) vs HSA | 2.5/3 | 3/3 | Principle: reimburse the $6,200 of saved receipts now, turning $9,000 into "$15,200 of tax-advantaged savings." Baseline treats the receipts as a future safety net and says to live on cash while payroll is redirected. |

## Numbers vs answer key

| Number | Key | Baseline | Principle |
|---|---|---|---|
| c01 draw rate on today's assets | 4.67% | ✗ not stated | ✗ not stated (gives 3.54% on projected assets) |
| c02 year-2 surrender | $10,800 | ✗ (gives year 1, $12,600) | ✗ (gives year 1, $13,242.60 on account value) |
| c03 marginal rate | 22% | ✓ | ✓ |
| c03 extra tax at 50/50 | $2,145 | ✓ | ✓ |
| c04 gain | $185,000 | ✓ | ✓ |
| c04 exclusion window | ~3 years after move-out | ✓ | ✓ |
| c05 conversion tax | $8,404 | ✓ $8,404 | ✓ $8,451 (within tolerance) |
| c05 room left in 22% | $35,800 | ✓ | ✗ $33,450 (2025 bracket) |
| c06 room to top of 22% | $109,600 | ✗ not computed | ✓ |
| c06 room under Medicare tier | $84,000 | ✓ | ✓ |
| c06 RMD age | 75 | ✓ | ✓ |
| c07 annual fee | $71.88 | ✓ | ✓ |
| c07 interest on $600 | ~$24 | ✓ $25-30 | ✓ $18 at 3% (edge) |
| c10 Roth max | $7,500 | ✓ | ✓ |
| c10 left after Roth | $1,500 | ✓ | ✓ $811.50 after FICA (more precise than the key) |
| c11 increase | $135 | ✗ not stated | ✓ |
| c13 definite medical | $1,318.00 | ✗ $2,606.47 | ✗ $2,606.47 |
| c13 ambiguous to confirm | $1,288.47 | ✗ | ✗ (listed as assumptions, asked to confirm, still totaled) |
| c16 HSA room | $7,550 | ✓ | ✓ |
| c16 payroll tax saved | $577.58 | ✗ not computed | ✓ $577 |

Not scored (case-design gaps, answer key depended on assumptions not in the prompt): c01 draw rate after home; c04 net monthly cash flow (principle's -$300 happens to fall inside the key's range).

## Patterns

1. **The instruction moved the result more than the model did.** Catch rate 69% to 89%; questions to the user 0 to 16 cases. Flash and Pro caught about the same share of hidden facts on the 9 shared cases.
2. **Search fixed some figures, not all.** Flash without search called the 2024 Medicare threshold the 2026 one ($206,000). Pro with search got $218,000 in both arms, but labeled the 2025 bracket thresholds as 2026 in three answers (c03 x2, c05 principle), and in c05 that changed the recommendation.
3. **Facts about products are unstable.** Lunch Money "~$120/yr" (c08 baseline) vs "about $40 to $50 a year" (c13 principle); Ascensus fees differ between runs. Neither is sourced in the answer.
4. **More useful also means more directive.** Principle answers say "cap it at $84,000 this year," "Do not shop around," "Sell the condo," "firing this firm." That is the line between information and advice.
5. **Strongest when the trap is in the document:** surrender table (c02), purchase date (c04), no-withholding note (c05), spouse wages (c06), saved receipts (c16).
