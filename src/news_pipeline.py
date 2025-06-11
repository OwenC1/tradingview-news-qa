from lxml import etree
import sqlite3
import re
import csv

# Step 1: Sample XML content (simulate a feed)
sample_xml = """
<newsMessage xmlns="http://iptc.org/std/nar/2006-10-01/">
  <itemSet>
    <newsItem>
      <contentMeta>
        <headline>Bitcoin Soars Past $70K</headline>
        <subject qcode="subj:11000000" />
        <language tag="en" />
        <contentCreated>2024-06-06T14:00:00Z</contentCreated>
        <description role="descRole:caption">BTC rally driven by ETF optimism.</description>
      </contentMeta>
    </newsItem>
    <newsItem>
      <contentMeta>
        <headline>Gold Prices Dip Amid Dollar Strength</headline>
        <subject qcode="subj:05000000" />
        <language tag="en" />
        <contentCreated>2024-06-06T10:00:00Z</contentCreated>
        <description role="descRole:caption">XAU struggles as USD surges.</description>
      </contentMeta>
    </newsItem>
  </itemSet>
</newsMessage>
"""

# Step 2: Parse XML from string
tree = etree.fromstring(sample_xml.encode())

# Step 3: Validation + Enrichment
news_data = []
allowed_qcodes = {"subj:04000000", "subj:05000000", "subj:11000000"}

for item in tree.xpath("//*[local-name()='newsItem']"):
    headline = item.xpath(".//*[local-name()='headline']/text()")
    subject = item.xpath(".//*[local-name()='subject']/@qcode")
    language = item.xpath(".//*[local-name()='language']/@tag")
    pubdate = item.xpath(".//*[local-name()='contentCreated']/text()")
    description = item.xpath(".//*[local-name()='description']/text()")

    if not headline or not subject or subject[0] not in allowed_qcodes or not pubdate:
        continue

    # Use regex to pull out any capitalized tickers (symbol-like)
    extracted_symbols = re.findall(r"\b[A-Z]{2,5}\b", headline[0])

    news_data.append({
        "headline": headline[0],
        "subject": subject[0],
        "language": language[0] if language else "unknown",
        "pubdate": pubdate[0],
        "description": description[0] if description else "",
        "symbols": ",".join(extracted_symbols)
    })

# Step 4: Save to SQLite DB
conn = sqlite3.connect("tradingview_news.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    headline TEXT,
    subject TEXT,
    language TEXT,
    pubdate TEXT,
    description TEXT,
    symbols TEXT
)
""")

for entry in news_data:
    cur.execute("""
    INSERT INTO news (headline, subject, language, pubdate, description, symbols)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        entry["headline"],
        entry["subject"],
        entry["language"],
        entry["pubdate"],
        entry["description"],
        entry["symbols"]
    ))

conn.commit()
conn.close()

# Step 5: Save to CSV
with open("parsed_news.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["headline", "subject", "language", "pubdate", "description", "symbols"])
    writer.writeheader()
    writer.writerows(news_data)

print("✅ News feed parsed, validated, and saved to database and CSV.")
