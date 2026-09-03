# India FD Rates

India FD Rates is a GitHub Pages site that compares the highest publicly advertised retail fixed-deposit rates across private-sector, public-sector, and small-finance banks.

## How it works

- `data/fd-rates.json` is the published, reviewable snapshot.
- `scripts/update_rates.py` checks each configured official bank rate page once daily.
- The updater only replaces a value when it can find an explicit, configured rate pattern. Failed or ambiguous checks are retained and reported instead of guessed.
- `.github/workflows/update-fd-rates.yml` updates the snapshot and deploys the Pages artifact.

The figures are indicative annual rates for eligible resident retail deposits, not investment advice. Always confirm the rate, eligibility, amount limit, callable status, and booking date on the linked official bank page before investing.

## Local development

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>.

To check the updater without changing data:

```bash
python3 scripts/update_rates.py --check-only
```
