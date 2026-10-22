"""Answer key for the Gemini consumer-finance eval.

Deterministic. Every number a correct answer should contain is computed here from the case
inputs and 2026 federal figures, so a model's answer can be checked against arithmetic, not tone.

2026 figures used (sources in README):
  Federal brackets and standard deduction: IRS Rev. Proc. 2025-32
  Medicare Part B/D IRMAA tiers: CMS 2026 notices
  401(k) deferral $24,500, IRA $7,500, HSA family $8,750: IRS 2026 limits

Run: python3 calc.py   (writes answer_key.json)
"""
import json
from datetime import date

BRACKETS = {
    "single": [(12_400, .10), (50_400, .12), (105_700, .22), (201_775, .24),
               (256_225, .32), (640_600, .35), (float("inf"), .37)],
    "mfj":    [(24_800, .10), (100_800, .12), (211_400, .22), (403_550, .24),
               (512_450, .32), (768_700, .35), (float("inf"), .37)],
}
STD_DED = {"single": 16_100, "mfj": 32_200}
IRMAA_TIER1_MFJ = 218_000          # MAGI at or above this triggers the first surcharge tier
LIMIT_401K = 24_500
LIMIT_IRA = 7_500
LIMIT_HSA_FAMILY = 8_750
FICA = 0.0765


def tax(taxable, status):
    owed, lower = 0.0, 0.0
    for upper, rate in BRACKETS[status]:
        if taxable > lower:
            owed += (min(taxable, upper) - lower) * rate
        lower = upper
    return round(owed, 2)


def marginal(taxable, status):
    lower = 0.0
    for upper, rate in BRACKETS[status]:
        if taxable <= upper:
            return rate
        lower = upper
    return BRACKETS[status][-1][1]


def top_of_bracket(taxable, status):
    for upper, _ in BRACKETS[status]:
        if taxable <= upper:
            return upper
    return float("inf")


def key():
    k = {}

    # c01: draw rates
    spend = 14_000 * 12
    k["c01_draw_rate_now_pct"] = {"value": round(spend / 3_600_000 * 100, 2), "tolerance": 0.3,
        "how": "168,000 / 3,600,000"}
    home = 1_350_000                      # midpoint of the stated $1.2-1.5M
    carrying = 4_500                      # owner's stated $4-5K/month to own
    spend_after = (14_000 - 7_500 + carrying) * 12
    k["c01_draw_rate_after_home_pct"] = {"value": round(spend_after / (3_600_000 - home) * 100, 2),
        "tolerance": 0.6, "how": "(14,000 - 7,500 rent + 4,500 carrying) x 12 / (3.6M - 1.35M home)"}

    # c02: surrender charge in contract year 2
    k["c02_year2_surrender_usd"] = {"value": 180_000 * 0.06, "tolerance": 100,
        "how": "6% x 180,000, before the market value adjustment"}

    # c03: Roth vs traditional
    taxable_now = 108_000 - 22_000 - STD_DED["single"]
    taxable_5050 = 108_000 - 12_250 - STD_DED["single"]
    k["c03_marginal_rate_pct"] = {"value": marginal(taxable_now, "single") * 100, "tolerance": 0,
        "how": f"taxable {taxable_now:,} single; 50/50 taxable {taxable_5050:,}, same bracket"}
    k["c03_extra_tax_5050_usd"] = {"value": round(tax(taxable_5050, "single") - tax(taxable_now, "single"), 2),
        "tolerance": 60, "how": "moving 9,750 from pre-tax to Roth at 22%"}

    # c04: rent vs sell
    move_out = date(2026, 12, 1)
    k["c04_sec121_deadline"] = {"value": "2029-12", "tolerance": "month",
        "how": "2-of-5-year use test: move out Dec 2026, sell by about Dec 2029"}
    k["c04_gain_usd"] = {"value": 640_000 - 455_000, "tolerance": 10_000,
        "how": "640,000 value - 455,000 purchase, before selling costs and improvements; under the 250,000 single exclusion"}
    maint = 640_000 * 0.01 / 12
    k["c04_net_low_usd"] = {"value": round(2_750 * 0.95 - 2_450 - maint), "tolerance": 150,
        "how": "rent 2,750 less 5% vacancy, less 2,450 costs, less 1%/yr maintenance; before tax. Pre-cost spread: 300"}
    k["c04_net_high_usd"] = {"value": round(2_900 * 0.95 - 2_450 - maint), "tolerance": 150,
        "how": "rent 2,900 less 5% vacancy, less 2,450 costs, less 1%/yr maintenance; before tax. Pre-cost spread: 450"}

    # c05: in-plan conversion
    base = 96_000 - 10_000 - STD_DED["single"]
    k["c05_conversion_tax_usd"] = {"value": round(tax(base + 38_000, "single") - tax(base, "single"), 2),
        "tolerance": 150, "how": f"taxable {base:,} -> {base + 38_000:,}; crosses 105,700"}
    k["c05_room_in_22_usd"] = {"value": top_of_bracket(base, "single") - base, "tolerance": 500,
        "how": f"105,700 - {base:,}"}

    # c06: conversions vs bracket and IRMAA
    agi = 64_000 + 70_000
    taxable = agi - STD_DED["mfj"]
    k["c06_room_to_top_of_22_usd"] = {"value": top_of_bracket(taxable, "mfj") - taxable, "tolerance": 1_000,
        "how": f"211,400 - taxable {taxable:,} (joint, spouse wages included)"}
    k["c06_room_under_irmaa_usd"] = {"value": IRMAA_TIER1_MFJ - agi, "tolerance": 1_000,
        "how": f"218,000 - MAGI {agi:,}; 2026 tier shown, thresholds adjust yearly"}
    k["c06_rmd_age"] = {"value": 75, "tolerance": 0, "how": "born 1963: SECURE 2.0 sets 75 for 1960 and later"}

    # c07: fee vs interest
    k["c07_annual_fee_usd"] = {"value": round(5.99 * 12, 2), "tolerance": 1, "how": "5.99 x 12"}
    k["c07_interest_on_600_usd"] = {"value": round(600 * 0.04, 2), "tolerance": 6,
        "how": "600 x ~4%, illustrative rate"}

    # c10: teen Roth
    k["c10_roth_max_usd"] = {"value": min(LIMIT_IRA, 9_000), "tolerance": 0, "how": "min(7,500, earned 9,000)"}
    k["c10_remaining_usd"] = {"value": 9_000 - min(LIMIT_IRA, 9_000), "tolerance": 0, "how": "9,000 - 7,500"}

    # c11: umbrella
    k["c11_increase_usd"] = {"value": 675 - 540, "tolerance": 0, "how": "675 - 540"}

    # c13: medical transactions (ground truth by merchant category)
    definite = [40.00, 285.00, 118.00, 195.00, 350.00, 180.00, 150.00]
    ambiguous = [63.48, 24.99, 600.00, 600.00]
    k["c13_definite_medical_usd"] = {"value": round(sum(definite), 2), "tolerance": 0.01,
        "how": "pediatrics, dental, lab, eyeglasses, hospital, PT, urgent care; excludes vet 412 and gym 260"}
    k["c13_ambiguous_usd"] = {"value": round(sum(ambiguous), 2), "tolerance": 0.01,
        "how": "drugstores 88.47 + Venmo therapy/session 1,200: confirm before counting"}

    # c16: HSA
    room = LIMIT_HSA_FAMILY - 1_200
    k["c16_hsa_room_usd"] = {"value": room, "tolerance": 0, "how": "8,750 family limit - 1,200 contributed"}
    k["c16_payroll_tax_saved_usd"] = {"value": round(room * FICA, 2), "tolerance": 10,
        "how": "7,550 x 7.65% if contributed through payroll"}
    return k


if __name__ == "__main__":
    answer_key = key()
    cases = json.load(open("cases.json"))["cases"]
    wanted = {n for c in cases for n in c["numbers"]}
    missing = wanted - set(answer_key)
    assert not missing, f"cases.json names numbers the key doesn't compute: {missing}"
    json.dump(answer_key, open("answer_key.json", "w"), indent=2)
    for name in sorted(answer_key):
        print(f"{name:32} {answer_key[name]['value']}")
