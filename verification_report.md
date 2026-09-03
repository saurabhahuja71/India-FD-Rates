# FD Verification Report

Generated: `2026-09-03T09:36:51Z`

## Ranking policy

The published ranking is **highest callable resident-domestic-retail FD rate**, including callable special-tenure schemes (for example, 444/555-day products). Non-callable, bulk, NRI-only, and institutional products are excluded from the main ranking. Special products are retained separately in bank evidence.

## Public-sector audit

| Rank | Bank | Rate | Verification |
|---:|---|---:|---|
| 1 | Bank of Baroda | 6.75% | LIVE_VERIFIED |
| 2 | Canara Bank | 6.60% | LIVE_VERIFIED |
| 3 | Indian Overseas Bank | 6.60% | LIVE_VERIFIED |
| 4 | Punjab National Bank | 6.60% | LIVE_VERIFIED |
| 5 | Union Bank of India | 6.55% | LIVE_VERIFIED |
| 6 | State Bank of India | 6.45% | LIVE_VERIFIED |

### Bank of India

- Status: **FAILED**
- Evidence source: `https://bankofindia.bank.in/interest-rate/rupee-term-deposit-rate`
- Rate: **not available**
- Rank: **not ranked** because no acceptable current official evidence was fetched.
- Reason: official BOI pages and the official policy-document candidate returned HTTP 403 to this automation runner; no current downloadable rate schedule was verified.

### State Bank of India

- Status: **LIVE_VERIFIED**
- Rank: **#6**
- SBI is excluded from the Top 5 because its verified callable retail rate ranks #6, below the five highest verified public-sector rates.

## Changes since previous snapshot

| Bank | Old rate | Corrected rate | Old rank | New rank | Root cause |
|---|---:|---:|---:|---:|---|
| Axis Bank | 7.0% | 6.5% | 1 | 5 | adapter/source-column correction |
| Yes Bank | 7.25% | 7.0% | — | 4 | adapter/source-column correction |
| Bank of Baroda | 5.0% | 6.75% | — | 1 | adapter/source-column correction |
| State Bank of India | 7.05% | 6.45% | — | 6 | adapter/source-column correction |
| Canara Bank | 7.0% | 6.6% | — | 2 | adapter/source-column correction |
| Punjab National Bank | 5.0% | 6.6% | — | 4 | adapter/source-column correction |
| Utkarsh Small Finance Bank | 8.0% | 8.1% | — | 1 | adapter/source-column correction |
| AU Small Finance Bank | 7.5% | 7.4% | 2 | 5 | adapter/source-column correction |
| Jana Small Finance Bank | 5.0% | 8.0% | — | 2 | adapter/source-column correction |
| RBL Bank | 8.15% | 7.2% | 1 | 2 | RBL adapter previously selected non-callable/Super Senior columns; corrected to callable General/Senior columns |
| Indian Overseas Bank | 7.0% | 6.6% | 1 | 3 | adapter/source-column correction |

## Evidence blocks for ranked banks

### private_sector
- **Bandhan Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `2 years to less than 3 years`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **7.45%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.95%**; source: https://www.bandhan.bank.in/fixed-deposit
- **RBL Bank** — table: `Fixed Deposits – Less than INR 3 crores – Premature Withdrawal Allowed`; tenure: `18 months to 36 months`; regular column: `General Citizen — Interest Rates (per annum)` = **7.20%**; senior column: `Senior Citizen — Senior Citizen Interest Rates (per annum)` = **7.70%**; source: https://www.rbl.bank.in/interest-rates
- **IndusInd Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `2 Years to 3 Years`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **7.00%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.75%**; source: https://www.indusind.bank.in/in/en/personal/rates.html
- **Yes Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `18 months 1 day < 24 months`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **7.00%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.75%**; source: https://www.yes.bank.in/sites/web/content/published/api/v1.1/assets/CONTE74C9031F1EA4D3B98EC33112F600AC5/native/yb_interest_rates_on_savings_account_n_term_deposit_1jan2026.pdf?download=false
- **Axis Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `18 Months < 2 Years`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **6.50%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.00%**; source: https://www.axisbank.com/interest-rate-on-deposits
### public_sector
- **Bank of Baroda** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `bob Golden Goal deposit Scheme (555 Days)`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **6.75%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.25%**; source: https://bankofbaroda.bank.in/interest-rate-and-service-charges/deposits-interest-rates/fixed-deposits-callable-and-non-callable-upto-ten-crores
- **Canara Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `555 Days*`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **6.60%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.10%**; source: https://www.canarabank.bank.in/term-deposits-rate-of-interest-p.a.
- **Indian Overseas Bank** — table: `Revised retail deposits below Rs. 3 Crore; callable counterpart to separately listed non-callable deposits`; tenure: `444 Days`; regular column: `Revised Rates for Deposits below Rs. 3 Crore W.E.F 15.05.2026 (in %)` = **6.60%**; senior column: `Senior Citizen additional interest: +0.50% over applicable retail rate` = **7.10%**; source: https://www.iob.bank.in/en/domestic-nro-nre-retail-term-deposit-rates
- **Punjab National Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `444 Days`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **6.60%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.10%**; source: https://www.pnbindia.in/interest-rates-deposit.html
- **Union Bank of India** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `555 Days`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **6.55%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.05%**; source: https://www.unionbankofindia.bank.in/en/details/rate-of-interest
### small_finance
- **Utkarsh Small Finance Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `666 Days`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **8.10%**; senior column: `Senior Citizen Interest Rates (per annum)` = **8.25%**; source: https://www.utkarsh.bank.in/personal/digital-products/digital-fixed-deposit
- **Jana Small Finance Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `>2 Years - 3 Years (1095 Days)`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **8.00%**; senior column: `Senior Citizen Interest Rates (per annum)` = **8.30%**; source: https://www.janabank.com/interest-rates/
- **Shivalik Small Finance Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `23 months 1 day to 27 months`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **8.00%**; senior column: `Senior Citizen Interest Rates (per annum)` = **8.25%**; source: https://shivalik.bank.in/interest-rate
- **Ujjivan Small Finance Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `3 Year 1 Day – 3 year 6 months`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **7.80%**; senior column: `Senior Citizen Interest Rates (per annum)` = **8.30%**; source: https://www.ujjivansfb.bank.in/interest-rates
- **AU Small Finance Bank** — table: `Callable domestic resident retail FD table (adapter-selected)`; tenure: `30 Months 1 Day to 36 Months`; regular column: `General/Regular Citizen Interest Rates (per annum)` = **7.40%**; senior column: `Senior Citizen Interest Rates (per annum)` = **7.90%**; source: https://www.au.bank.in/interest-rates/fixed-deposit-interest-rates
