# finance_eval

A small first test of whether Gemini catches the fact a person didn't know to ask about when they bring it a personal-finance decision.

Companion to the write-up *Financial OS: where am I?* by Inna Raykhman (October 2026). Built with Claude from Inna's thesis, questions, and definition of a good answer; run against Gemini through the Gemini API.

All cases and documents are synthetic, modeled on question patterns in public personal-finance groups, with every personal detail and number changed. Nothing here is financial advice.

## What's here

| Path | What it is |
|---|---|
| `cases.json` | 16 cases: the question, attached files, the hidden facts a good answer must catch (50 in all), the questions it should ask, and the numbers to check |
| `files/` | Generated documents for 9 of the cases (statements, a pay stub, an annuity illustration, a CPA invoice, card exports) |
| `calc.py` → `answer_key.json` | Answer key in code: 20 numbers computed from 2026 federal tax brackets, the standard deduction, and Medicare income tiers |
| `prompts/principle.txt` | The rule set added in run 2 (as a system instruction) |
| `rubric.md` | How answers were graded |
| `run.py` | Harness. Python 3.8+, standard library only |
| `results/` | Raw Gemini answers, one JSON line per case per run |
| `scores_pro.md` | Grades for every case, with the sentence each grade rests on |

## Runs

- **Run 1:** the question as written.
- **Run 2:** the same question with `prompts/principle.txt` as the system instruction.
- Gemini 3.1 Pro (preview) with Google Search grounding, October 21, 2026. Graded by Claude against `rubric.md`; numbers checked against `answer_key.json`.

## Reproduce

```
export GEMINI_API_KEY=your-key        # from aistudio.google.com
python3 run.py --probe                # which models and search your key can use
python3 run.py --model gemini-3.1-pro-preview
```

Options: `--cases c01,c06`, `--arm baseline|principle|both`, `--no-search`, `--dry-run`, `--make-manual` (prompts for pasting into the Gemini app).

## 2026 figures used

- Federal brackets and standard deduction: IRS Rev. Proc. 2025-32
- Medicare Part B/D income-related tiers: CMS 2026
- 401(k) $24,500; IRA $7,500; HSA family $8,750: IRS 2026 limits
