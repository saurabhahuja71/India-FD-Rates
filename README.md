# 🇮🇳 India FD Rates

A GitHub project that automatically tracks the highest publicly advertised retail Fixed Deposit rates in India.

## 📊 Current Highest FD Rates

<!-- FD_TABLES_START -->

## 🏦 Top 5 Private Sector Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | IDFC FIRST Bank — Resident retail FD; below the applicable deposit limit. | 7.25% | 7.75% | 400 days | 03 Sep 2026 | [Official](https://www.idfcfirstbank.com/personal-banking/deposits/fixed-deposit) |
| 2 | Yes Bank — Resident retail FD; confirm callable/product conditions. | 7.25% | 8.00% | 18 months | 03 Sep 2026 | [Official](https://www.yesbank.in/personal-banking/deposits/fixed-de-deposits) |
| 3 | Axis Bank — Resident retail deposit; check current amount slab. | 7.10% | 7.60% | 15 months to <18 months | 03 Sep 2026 | [Official](https://www.axisbank.com/interest-rate-on-deposits) |
| 4 | ICICI Bank — Domestic retail FD; senior rate for eligible resident citizens. | 7.10% | 7.60% | 15 months to 2 years | 03 Sep 2026 | [Official](https://www.icicibank.com/personal-banking/deposits/fixed-deposit/fd-interest-rates) |
| 5 | HDFC Bank — Retail domestic FD; rate card and amount bands apply. | 7.00% | 7.50% | 18 months to <21 months | 03 Sep 2026 | [Official](https://www.hdfcbank.com/personal/save/deposits/fixed-deposit-interest-rate) |

## 🏛️ Top 5 Public Sector Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | Bank of Baroda — Special 400-day scheme; verify its availability before booking. | 7.15% | 7.65% | 400 days | 03 Sep 2026 | [Official](https://www.bankofbaroda.in/personal-banking/accounts/term-deposit/fixed-deposit) |
| 2 | State Bank of India — Retail domestic term deposit under ₹3 crore. | 7.05% | 7.55% | 2 years to <3 years | 03 Sep 2026 | [Official](https://sbi.co.in/web/interest-rates/deposit-rates/retail-domestic-term-deposit-rates) |
| 3 | Canara Bank — Check whether the special-tenure offer remains open. | 7.00% | 7.50% | 444 days | 03 Sep 2026 | [Official](https://canarabank.com/pages/interest-rates) |
| 4 | Punjab National Bank — Retail domestic term deposit; special-tenure scheme may have an end date. | 7.00% | 7.50% | 400 days | 03 Sep 2026 | [Official](https://www.pnbindia.in/interest-rates-deposit.html) |
| 5 | Indian Bank — IND Green special scheme; minimum ₹1,000, maximum below ₹3 crore. | 6.80% | 7.30% | 555 days | 03 Sep 2026 | [Official](https://www.indianbank.in/departments/ind-green-555-days/) |

## 🏦 Top 5 Small Finance Banks

| Rank | Bank | Regular Citizen | Senior Citizen | Tenure | Last Verified | Source |
|------|------|-----------------|----------------|--------|---------------|--------|
| 1 | Utkarsh Small Finance Bank — Fixed Deposit Plus is non-callable and has deposit/withdrawal conditions; verify rate card. | 8.35% | 8.85% | 666 days | 03 Sep 2026 | [Official](https://www.utkarsh.bank/personal/term-deposits/fixed-deposits-plus) |
| 2 | Jana Small Finance Bank — Resident retail deposit; confirm current slab and callable status. | 8.00% | 8.50% | 365 days | 03 Sep 2026 | [Official](https://www.janabank.com/interest-rates/) |
| 3 | Suryoday Small Finance Bank — Check current retail rate card and product eligibility. | 8.00% | 8.60% | 5 years | 03 Sep 2026 | [Official](https://www.suryodaybank.com/interest-rates/) |
| 4 | Equitas Small Finance Bank — Limited/special 888-day rate; senior uplift is 0.60% for this tenure. | 7.80% | 8.40% | 888 days | 03 Sep 2026 | [Official](https://equitasbank.com/personal-banking/save/fixed-deposits/fixed-deposit/) |
| 5 | AU Small Finance Bank — Resident retail FD below ₹3 crore; senior rate requires eligible resident customer. | 7.40% | 7.90% | 30 months 1 day to 36 months | 03 Sep 2026 | [Official](https://www.au.bank.in/interest-rates/fixed-deposit-interest-rates) |

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
