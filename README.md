# Simple Web Scraper for Threat Intelligence
Automated Indicator of Compromise (IOC) collector from public threat intelligence feeds (e.g. abuse.ch, URLhaus, Feodo Tracker, SSL Blacklist).

## Project Architecture
This lightweight modular python application executes an automated feed scraping pipeline:
1. **Fetch**: Uses `requests` with exponential backoff and localized `User-Agent` configs.
2. **Parse**: Applies regex patterns to extract IP Addresses, Domains, and SHA256 hashes from raw bodies.
3. **Validate**: Deduplicates listings and filters standard RFC1918 private IP addresses.
4. **Store**: Serializes validated threat intel list into standard `json`, `csv`, or `txt` files.

## Installation & Setup
1. Clone this repository or locate the downloadable files:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the scraping script:
   ```bash
   # Scrape the default URLhaus feed and save to output/iocs_urlhaus.json
   python main.py

   # Scrape Feodo Tracker and export as CSV
   python main.py --feed feodotracker --format csv

   # Run automated cycle scraping across ALL feeds
   python main.py --all
   ```

## Deploying on GitHub Actions / Pages
You can easily automate this tool to run daily and publish the output to GitHub Pages:
1. Store this repository under your GitHub account.
2. Setup a daily cron trigger under `.github/workflows/scrape.yml`:
```yaml
name: Global Threat Intel Scraping Cron

on:
  schedule:
    - cron: '0 0 * * *' # Every day at midnight
  workflow_dispatch: # Enable running manually in actions tab

jobs:
  scrape-and-publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Setup Python environment
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install active dependencies
        run: pip install -r requirements.txt

      - name: Execute Threat Scraping pipeline
        run: python main.py --all --format json --output output/

      - name: Deploy output feeds to gh-pages branch
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{"$"}}{{ secrets.GITHUB_TOKEN }}
          publish_dir: ./output
```
