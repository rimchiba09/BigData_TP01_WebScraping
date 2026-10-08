# TP01: Python Web Scraping

Module: Big Data Analytics, M2 IA & Data Science, University of El Oued (2026/2027)

## Goal
Scrape quotes from Wikiquote and save them to CSV (at least 1000 rows).

## How to run
pip install -r requirements.txt
python src/fetch_page.py         # Q1: fetch a page and print its HTML
python src/scrape_quotes.py      # Q2-Q4: scrape 15 authors, write data/quotes.csv
python src/validate_dataset.py   # check shape, nulls, lengths

## Result
data/quotes.csv: 3870 unique quotes, columns: author, section, quote.

## Source and license
Data comes from Wikiquote (https://en.wikiquote.org), licensed under CC BY-SA.
Pages are fetched politely (descriptive User-Agent, 1 second delay, local cache).
