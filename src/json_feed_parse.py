# Full TradingView-style JSON News Feed Pipeline

import json
import csv
from datetime import datetime

# === CONFIG ===
INPUT_JSON = "tests/news_feed.json"
OUTPUT_CSV = "tests/parsed_news.csv"

# === STEP 1: Load JSON File ===
try:
    with open(INPUT_JSON, "r") as f:
        data = json.load(f)
    print("✅ JSON loaded successfully")
except Exception as e:
    print("❌ Failed to load JSON:", e)
    exit(1)

# === STEP 2: Clean, Validate, and Enrich ===
cleaned_data = []

for article in data.get("articles", []):
    headline = article.get("headline", "").strip()
    symbol = article.get("symbol", "").strip().upper()
    urgency = article.get("urgency")
    pubdate_raw = article.get("pubdate", "")
    subject = article.get("subject", "").strip().lower()
    body = article.get("body", "").strip()
    source = article.get("source", "").strip()
    category = article.get("category", "").strip().lower()

    # Validate mandatory fields
    if not (headline and symbol and pubdate_raw):
        print(f"⚠️ Skipping incomplete article: {article}")
        continue

    # Parse and normalize date
    try:
        pubdate = datetime.fromisoformat(pubdate_raw.replace("Z", "+00:00"))
    except ValueError:
        print(f"❌ Invalid date format: {pubdate_raw}")
        continue

    # Tagging
    if "earnings" in subject:
        tag = "earnings"
    elif "crypto" in subject:
        tag = "cryptocurrency"
    elif "forex" in subject:
        tag = "forex"
    else:
        tag = "other"

    cleaned_data.append([
        headline, symbol, urgency, pubdate.isoformat(), tag, body, source, category
    ])

# === STEP 3: Write to CSV ===
try:
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "headline", "symbol", "urgency", "pubdate", "tag", "body", "source", "category"
        ])
        writer.writerows(cleaned_data)
    print(f"✅ Cleaned data written to {OUTPUT_CSV}")
except Exception as e:
    print("❌ Failed to write CSV:", e)
    exit(1)
