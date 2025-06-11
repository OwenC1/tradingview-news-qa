# Full TradingView-style ECB Feed Processing Script

from lxml import etree
import csv
import datetime

# === CONFIG ===
INPUT_XML = "tests/ecb.xml"
OUTPUT_CSV = "tests/parsed_feed.csv"

# === STEP 1: Parse XML ===
try:
    with open(INPUT_XML, "rb") as f:
        tree = etree.parse(f)
    print("✅ XML parsed successfully")
except Exception as e:
    print("❌ Failed to parse XML:", e)
    exit(1)

# === STEP 2: Extract & Clean Data ===
currency_nodes = tree.xpath("//*[local-name()='Cube'][@currency]")
cleaned_data = []

for node in currency_nodes:
    code = node.get("currency", "").strip().upper()
    rate_raw = node.get("rate", "").strip()

    try:
        rate = float(rate_raw)
        if rate <= 0:
            print(f"⚠️ Skipping invalid rate for {code}: {rate}")
            continue
    except ValueError:
        print(f"❌ Could not convert rate for {code}: '{rate_raw}'")
        continue

    # === STEP 3: Enrichment ===
    if code in ["USD", "EUR", "JPY", "GBP", "CHF", "CAD"]:
        asset_class = "forex"
    else:
        asset_class = "other"

    cleaned_data.append((code, rate, asset_class))

# === STEP 4: Basic QA Checks ===
if len(cleaned_data) < 5:
    print("⚠️ Warning: Unusually small dataset (less than 5 currencies)")

# === STEP 5: Write to CSV ===
try:
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["currency", "rate", "asset_class"])
        writer.writerows(cleaned_data)
    print(f"✅ Data saved to {OUTPUT_CSV}")
except Exception as e:
    print("❌ Failed to write CSV:", e)
    exit(1)
