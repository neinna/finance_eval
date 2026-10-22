# Scores: gemini-3.6-flash, Google Search grounding on, run 2026-10-22 18:42 UTC
Same 16 cases, same two arms, same rubric and answer key as scores_pro.md.
Run 1 = case prompt only. Run 2 = same prompt with prompts/principle.txt as the system instruction.
Scored 2026-10-22 by Claude against rubric.md. ✓ = 1, ◐ = 0.5, ✗ = 0.
One run per case per arm; run-to-run variance not measured.

## Headline

| | Run 1 | Run 2 |
|---|---|---|
| Hidden facts caught | 31.5 / 50 (63%) | 41.5 / 50 (83%) |
| Cases where it asked the user anything | 0 / 16 | 16 / 16 |
| Answer-key numbers matched (scorable) | 10 / 20 | 15 / 20 |

## Catches by case

| Case | Run 1 | Run 2 | What changed |
|---|---|---|---|
| c01 cash, retire at 50 | 2/4 | 3/4 | Both say there is no safe 7-8% and work from a 3-3.5% withdrawal on projected assets, not the 4.7% draw on today's. Both assume $300-350K/yr of new savings. Run 2 adds education costs and the 40.8% tax drag on the cash; neither adds health insurance. |
| c02 annuity "no fees" | 2.5/3 | 2.5/3 | Run 1 repeats the advisor: commission "does not reduce your initial $180,000." Run 2: "no fees" is "MISLEADING," cost is in the spread and commission. Run 1 names insurer ratings and guaranty limits; run 2 drops them. |
| c03 Roth split | 3/3 | 3/3 | Same, both on correct 2026 figures ($16,100 deduction, 22% bracket). Run 2 commits: "Keep most of your contributions Traditional." |
| c04 rent or sell condo | 2.5/3 | 2.5/3 | Both catch the window to late 2029 and that the cash flow nets to about zero. Neither mentions depreciation recapture. Run 2: "Sell the Condo." |
| c05 in-plan conversion | 2/2 | 2/2 | Both on correct 2026 brackets ($105,700 top of 22%). Run 2 states the $35,800 room; run 1 only the $2,200 spill. |
| c06 conversions vs Medicare | 2.5/4 | 3.5/4 | Run 2 adds the two-year Medicare lookback and the $84,000 limit under $218,000. Both recommend waiting for the 12% years after the wife retires. |
| c07 HYSA + teen account | 1.5/3 | 3/3 | Run 2: $71.88 fee vs $21 of interest, dated rates ("Oct 2026"). Run 1: fee as "12% of the money," rates "4%-5%" and "often around 5.00% APY," undated. |
| c08 Mint replacement | 1/2 | 2/2 | Run 1 calls building her own "surprisingly easy." Run 2 prices aggregator access and maintenance and says avoid building live bank pipelines. Run 1 cites "Claude 3.5 Sonnet." |
| c09 one-time advice | 1/2 | 2/2 | Run 2 offers to model the offer now and asks for the details; adds the shared $24,500 401(k) limit across employers. |
| c10 teen's income | 2/4 | 4/4 | Run 2 adds UTMA aid treatment (20% vs 5.64%) and 529-to-Roth rollovers. Only arm of the four to catch all four. |
| c11 umbrella +25% | 2/3 | 3/3 | Run 1 says the earlier AI explanation "is accurate" with no sources. Run 2 confirms with sources and bundle math. |
| c12 $30K windfall | 1.5/3 | 1/3 | Run 2 asks three questions, then ranks Roth conversion first and the ADU last ("Lifestyle Choice") on a default 24% bracket. Its Roth math credits the conversion with "+$116,090," which is the taxable-account growth of the $30K, not the gain from converting. Run 1 lists the questions for her to ask herself and suggests a 15/15 split. Neither mentions state 529 deduction caps. |
| c13 health spending total | 1/4 | 2.5/4 | Both total $2,606.47, counting drugstore purchases and Venmo "session" payments as medical. Run 2 asks what the total is for and states the drugstore assumption; it does not flag the Venmo payments. |
| c14 CPA bill | 1.5/3 | 2/3 | Both catch "an extension to file is not an extension to pay." Run 2 computes penalty ($204) and interest (~$249) and asks about the engagement letter. Both call the fee too high; neither mentions the 110% safe harbor. |
| c15 solo 401(k) | 3/4 | 3/4 | Run 1 mentions Form 5500-EZ; run 2 drops it but asks about a W-2 401(k) (shared $24,500 limit). Ascensus fees differ again: "$20 per participant + $20 per fund" vs "$100 setup and $365/year." |
| c16 401(k) vs HSA | 2.5/3 | 2.5/3 | Both put the HSA first and do the $7,550 math. Both treat the $6,200 of receipts as reimbursable "at any time," not as cash for the crunch now. Run 2 computes $577.58 of payroll tax saved; it also gives $176,100 as the "2025/2026" Social Security wage cap, which is 2025's. |

## Numbers vs answer key

| Number | Key | Run 1 | Run 2 |
|---|---|---|---|
| c01 draw rate on today's assets | 4.67% | ✗ not stated | ✗ not stated |
| c02 year-2 surrender | $10,800 | ✗ not stated | ✗ (gives year 1, $13,242.60) |
| c03 marginal rate | 22% | ✓ | ✓ |
| c03 extra tax at 50/50 | $2,145 | ✓ | ✓ |
| c04 gain | $185,000 | ✓ | ✓ ($146,600-$185,000, low end net of selling costs) |
| c04 exclusion window | ~3 years after move-out | ✓ | ✓ |
| c05 conversion tax | $8,404 | ✓ ~$8,400 | ✓ $8,404 |
| c05 room left in 22% | $35,800 | ✗ not stated (gives the $2,200 spill) | ✓ |
| c06 room to top of 22% | $109,600 | ✗ | ✗ |
| c06 room under Medicare tier | $84,000 | ✗ (gives $85,000 on a different base) | ✓ |
| c06 RMD age | 75 | ✓ | ✓ |
| c07 annual fee | $71.88 | ✗ (as "12% of the money") | ✓ |
| c07 interest on $600 | ~$24 | ✗ | ✓ $21 at 3.5% |
| c10 Roth max | $7,500 | ✓ | ✓ |
| c10 left after Roth | $1,500 | ✓ | ✓ |
| c11 increase | $135 | ✓ | ✓ |
| c13 definite medical | $1,318.00 | ✗ $2,606.47 | ✗ $2,606.47 |
| c13 ambiguous to confirm | $1,288.47 | ✗ | ✗ |
| c16 HSA room | $7,550 | ✓ | ✓ |
| c16 payroll tax saved | $577.58 | ✗ | ✓ |

## Full grid (hidden facts caught, of 50)

| | Run 1 | Run 2 | Rules added |
|---|---|---|---|
| Pro | 34.5 (69%) | 44.5 (89%) | +20 pts |
| Flash | 31.5 (63%) | 41.5 (83%) | +20 pts |
| Model added | +6 pts | +6 pts | |

## Patterns (Flash, and what differs from Pro)

1. **Rules moved the score more than the model did.** Same +20 points on both models; Pro over Flash, +6 in both runs. Flash with rules (83%) beats Pro without (69%).
2. **Flash got the 2026 brackets right where Pro didn't** (c03, c05, c06 all on $16,100 / $105,700 / $32,200 / $100,800), but used the 2025 Social Security wage cap as 2026 (c16). Stale figures move around; they don't go away.
3. **Product facts keep drifting.** Lunch Money is now "$60/year" (c13 run 2), a third price across answers. Ascensus fees differ in all four answers.
4. **Same blind spot on the spending total.** All four answers say $2,606.47.
5. **Rules can lower a score.** c12 went from 1.5 to 1: run 2 ranked firmly on a default bracket and its conversion math is wrong.
6. Only 4 of 16 Flash cases scored the same in both runs (Pro: 8), because Flash's run 1 was weaker.
