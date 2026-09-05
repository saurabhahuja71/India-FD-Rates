# 🇮🇳 India FD Rates

A GitHub project that automatically tracks the highest publicly advertised retail Fixed Deposit rates in India.

## 📊 Current Highest FD Rates

The rankings use the highest eligible callable resident-domestic-retail FD rate, including callable special-tenure schemes. Non-callable, bulk, NRI-only and institutional products are excluded; product details remain in the evidence sections and inventory.

[View the all-bank inventory and every configured bank status](all-banks.html) · [Inspect the verification report](verification_report.md) · [Inspect the machine-readable ranking audit](data/ranking_audit.json)

<!-- FD_TABLES_START -->

## 🏦 Highest Callable Retail FD Rates — Private Sector

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Verification | Last Verified | Source |
|------|------|-----------------|----------------|--------|--------------|---------------|--------|
| 1 | Bandhan Bank | 7.45% | 7.95% | 2 years to less than 3 years | LIVE | 05 Sep 2026 | [Official](https://www.bandhan.bank.in/fixed-deposit) |
| 2 | RBL Bank | 7.20% | 7.70% | 18 months to 36 months | LIVE | 05 Sep 2026 | [Official](https://www.rbl.bank.in/interest-rates) |
| 3 | IDFC FIRST Bank | 7.10% | 7.35% | 500 days – 3 years | LIVE | 05 Sep 2026 | [Official](https://www.idfcfirst.bank.in/personal-banking/deposits/fixed-deposit/fd-interest-rates) |
| 4 | Yes Bank | 7.00% | 7.75% | Regular: 18 months 1 day < 24 months<br>Senior: 36 months < 60 months | LIVE | 05 Sep 2026 | [Official](https://www.yes.bank.in/sites/web/content/published/api/v1.1/assets/CONTE74C9031F1EA4D3B98EC33112F600AC5/native/yb_interest_rates_on_savings_account_n_term_deposit_1jan2026.pdf?download=false) |
| 5 | Federal Bank | 6.85% | 7.35% | 48 months | LIVE | 05 Sep 2026 | [Official](https://www.federal.bank.in/deposit-rate) |

## 🏛️ Highest Callable Retail FD Rates — Public Sector

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Verification | Last Verified | Source |
|------|------|-----------------|----------------|--------|--------------|---------------|--------|
| 1 | Bank of Baroda | 6.75% | 7.25% | bob Golden Goal deposit Scheme (555 Days) | LIVE | 05 Sep 2026 | [Official](https://bankofbaroda.bank.in/interest-rate-and-service-charges/deposits-interest-rates/fixed-deposits-callable-and-non-callable-upto-ten-crores) |
| 2 | Canara Bank | 6.60% | 7.10% | 555 Days* | LIVE | 05 Sep 2026 | [Official](https://www.canarabank.bank.in/term-deposits-rate-of-interest-p.a.) |
| 3 | Indian Overseas Bank | 6.60% | 7.10% | 444 Days | LIVE | 05 Sep 2026 | [Official](https://www.iob.bank.in/en/domestic-nro-nre-retail-term-deposit-rates) |
| 4 | Punjab National Bank | 6.60% | 7.10% | 444 Days | LIVE | 05 Sep 2026 | [Official](https://www.pnbindia.in/interest-rates-deposit.html) |
| 5 | Union Bank of India | 6.55% | 7.05% | 555 Days | LIVE | 05 Sep 2026 | [Official](https://www.unionbankofindia.bank.in/en/details/rate-of-interest) |

## 🏦 Highest Callable Retail FD Rates — Small Finance

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Verification | Last Verified | Source |
|------|------|-----------------|----------------|--------|--------------|---------------|--------|
| 1 | Utkarsh Small Finance Bank | 8.10% | 8.25% | 666 Days | LIVE | 05 Sep 2026 | [Official](https://www.utkarsh.bank.in/personal/digital-products/digital-fixed-deposit) |
| 2 | Jana Small Finance Bank | 8.00% | 8.30% | >2 Years - 3 Years (1095 Days) | LIVE | 05 Sep 2026 | [Official](https://www.janabank.com/interest-rates/) |
| 3 | Shivalik Small Finance Bank | 8.00% | 8.25% | 23 months 1 day to 27 months | LIVE | 05 Sep 2026 | [Official](https://shivalik.bank.in/interest-rate) |
| 4 | Ujjivan Small Finance Bank | 7.80% | 8.30% | 3 Year 1 Day – 3 year 6 months | LIVE | 05 Sep 2026 | [Official](https://www.ujjivansfb.bank.in/interest-rates) |
| 5 | AU Small Finance Bank | 7.40% | 7.90% | 30 Months 1 Day to 36 Months | LIVE | 05 Sep 2026 | [Official](https://www.au.bank.in/interest-rates/fixed-deposit-interest-rates) |

## Data Coverage

- **Private Sector:** ✅ 7 / 9 banks verified
- **Public Sector:** ✅ 5 / 12 banks verified
- **Small Finance:** ✅ 5 / 9 banks verified

### Last Collection Run

`05 Sep 2026 · source snapshot`

> ⚠️ FD rates change frequently. Always verify the rate, tenure, eligibility and conditions on the official bank website before investing.

<!-- FD_TABLES_END -->

## How It Works

- `data/fd-rates.json` is the published, reviewable snapshot.
- `scripts/update_rates.py` checks configured official bank rate pages once daily.
- The updater only promotes a value when an adapter finds explicit tenure-linked retail rates. Failed or ambiguous checks are retained as non-current and reported instead of guessed.
- After a successful data update, `scripts/update_readme.py` regenerates only the marked table section above.
- `.github/workflows/update-fd-rates.yml` validates the data, commits changed data/history/README files, and deploys the Pages site.
- `config/banks.yaml` is the bank registry. Each enabled bank loads an independent adapter from `scripts/banks/`; adapters can select HTML tables, structured HTML, official PDFs, or official endpoints without sharing a brittle site-wide regex.
- A failed adapter affects only that bank. It is written as `FAILED`, excluded from the current ranking, and included in the next collection report for repair.
- `data/fetch_failures.json` records attempted official URLs, HTTP metadata, parser stage, and the exact failure reason for the latest collection run.

## Data Accuracy

The figures are indicative annual rates for eligible resident retail deposits, not investment advice. Always confirm the rate, eligibility, amount limit, callable status, special-scheme end date, and booking date on the linked official bank page before investing. No referral or promotional links are used.

## Local Development

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>.

To check sources and regenerate the tables locally:

```bash
python3 scripts/update_rates.py
```

To validate the published JSON without fetching sources:

```bash
python3 scripts/validate_data.py
```
