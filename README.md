# 🇮🇳 India FD Rates

A GitHub project that automatically tracks the highest publicly advertised retail Fixed Deposit rates in India.

## 📊 Current Highest FD Rates

<!-- FD_TABLES_START -->

## 🏦 Top 5 Private Sector Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | HDFC Bank — Retail domestic FD; rate card and amount bands apply. | 6.50% | 7.10% | 3 Years 1 day to < 4 Years 7 Months | 03 Sep 2026 | [Official](https://www.hdfc.bank.in/fixed-deposit/fd-interest-rate) |

## 🏛️ Top 5 Public Sector Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| — | No VERIFIED retail rate available | — | — | — | — | — |

## 🏦 Top 5 Small Finance Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| — | No VERIFIED retail rate available | — | — | — | — | — |

### Last Updated

`03 Sep 2026 · source snapshot`

> ⚠️ FD rates change frequently. Always verify the rate, tenure, eligibility and conditions on the official bank website before investing.

<!-- FD_TABLES_END -->

## How It Works

- `data/fd-rates.json` is the published, reviewable snapshot.
- `scripts/update_rates.py` checks configured official bank rate pages once daily.
- The updater only replaces a value when it finds an explicit configured rate pattern. Failed or ambiguous checks are retained and reported instead of guessed.
- After a successful data update, `scripts/update_readme.py` regenerates only the marked table section above.
- `.github/workflows/update-fd-rates.yml` validates the data, commits changed data/history/README files, and deploys the Pages site.

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
