# 🇮🇳 India FD Rates

A GitHub project that automatically tracks the highest publicly advertised retail Fixed Deposit rates in India.

## 📊 Current Highest FD Rates

<!-- FD_TABLES_START -->

## 🏦 Top 5 Private Sector Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | Axis Bank | 6.50% | 7.00% | 18 Months < 2 Years | 03 Sep 2026 | [Official](https://www.axisbank.com/interest-rate-on-deposits) |
| 2 | HDFC Bank | 6.50% | 7.10% | 3 Years 1 day to < 4 Years 7 Months | 03 Sep 2026 | [Official](https://www.hdfc.bank.in/fixed-deposit/fd-interest-rate) |

> ⚠️ Only 2 bank(s) could be verified in the latest collection run.

## 🏛️ Top 5 Public Sector Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | Bank of Baroda | 6.75% | 7.25% | bob Golden Goal deposit Scheme (555 Days) | 03 Sep 2026 | [Official](https://bankofbaroda.bank.in/interest-rate-and-service-charges/deposits-interest-rates/fixed-deposits-callable-and-non-callable-upto-ten-crores) |
| 2 | Canara Bank | 6.60% | 7.10% | 555 Days* | 03 Sep 2026 | [Official](https://www.canarabank.bank.in/term-deposits-rate-of-interest-p.a.) |
| 3 | Punjab National Bank | 6.60% | 7.10% | 444 Days | 03 Sep 2026 | [Official](https://www.pnbindia.in/interest-rates-deposit.html) |
| 4 | Union Bank of India | 6.55% | 7.05% | 555 Days | 03 Sep 2026 | [Official](https://www.unionbankofindia.bank.in/en/details/rate-of-interest) |
| 5 | State Bank of India | 6.45% | 7.05% | Regular: 2 years to less than 3 years<br>Senior: 5 years and up to 10 years | 03 Sep 2026 | [Official](https://sbi.co.in/web/interest-rates/deposit-rates/retail-domestic-term-deposits) |

## 🏦 Top 5 Small Finance Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | Jana Small Finance Bank | 8.00% | 8.30% | >2 Years - 3 Years (1095 Days) | 03 Sep 2026 | [Official](https://www.janabank.com/interest-rates/) |
| 2 | AU Small Finance Bank | 7.40% | 7.90% | 30 Months 1 Day to 36 Months | 03 Sep 2026 | [Official](https://www.au.bank.in/interest-rates/fixed-deposit-interest-rates) |

> ⚠️ Only 2 bank(s) could be verified in the latest collection run.

## Data Coverage

- **Private Sector:** ✅ 2 / 7 banks verified
- **Public Sector:** ✅ 5 / 7 banks verified
- **Small Finance:** ✅ 2 / 7 banks verified

### Last Collection Run

`03 Sep 2026 · source snapshot`

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
