import os
import re
import time
from urllib.parse import quote as urlquote

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

HEADERS = {
    "User-Agent": "TP01-Scraper/1.0 (Univ Eloued student project; rim-chiba@univ-eloued.dz)"
}
BASE = "https://en.wikiquote.org/wiki/"
CACHE_DIR = os.path.join("data", "raw_pages")
os.makedirs(CACHE_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)
retry = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

AUTHORS = [
    "Albert Einstein", "Mark Twain", "Oscar Wilde", "Winston Churchill",
    "Mahatma Gandhi", "Aristotle", "Friedrich Nietzsche", "Voltaire",
    "Confucius", "Benjamin Franklin", "Abraham Lincoln",
    "Martin Luther King, Jr.", "Stephen Hawking", "Richard Feynman",
    "Carl Sagan",
]

SKIP = {"see also", "external links", "references", "further reading",
        "notes", "misattributed", "disputed", "sources", "bibliography",
        "footnotes"}


def get_html(title):
    """نجيبو الصفحة (من الكاش إذا موجودة)."""
    path = os.path.join(CACHE_DIR, re.sub(r"[^\w]+", "_", title) + ".html")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    url = BASE + urlquote(title.replace(" ", "_"))
    r = session.get(url, timeout=(30, 60))
    r.raise_for_status()
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)
    time.sleep(1)
    return r.text


def parse_quotes(html, author):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("div.mw-parser-output")
    rows = []
    for top in content.find_all("section", recursive=False):
        h2 = top.find("h2")
        top_name = h2.get_text(strip=True) if h2 else ""
        low = top_name.lower()
        if low.startswith("quotes about") or low in SKIP:
            continue

        good_uls = [ul for ul in top.find_all("ul") if ul.parent.name == "section"]
        for ul in good_uls:
            head = ul.parent.find(["h2", "h3", "h4"])
            sub_name = head.get_text(strip=True) if head else top_name
            for li in ul.find_all("li", recursive=False):
                for sub in li.find_all("ul"):   
                    sub.decompose()
                text = " ".join(li.get_text(" ", strip=True).split())
                if len(text) > 20:
                    rows.append({"author": author, "section": sub_name, "quote": text})
    return rows


all_rows = []
for author in AUTHORS:
    try:
        html = get_html(author)
        rows = parse_quotes(html, author)
        print(f"{len(rows):5d}  {author}")
        all_rows.extend(rows)
    except Exception as e:
        print(f"  ERR  {author}: {e}")

df = pd.DataFrame(all_rows)
before = len(df)
df = df.drop_duplicates(subset="quote").reset_index(drop=True)

df.to_csv(os.path.join("data", "quotes.csv"), index=False, encoding="utf-8-sig")
print(f"\nTotal: {before} | after dedup: {len(df)}")
print("OK >= 1000 ✅" if len(df) >= 1000 else "Less than 1000 ❌ (زيدو مؤلفين)")