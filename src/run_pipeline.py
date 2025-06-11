import yaml
import requests
from lxml import etree
import re

# 1. Load YAML config
with open("feed_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# 2. Fetch feed content
response = requests.get(config["url"])
response.raise_for_status()
xml_content = response.content

# 3. Parse XML
tree = etree.fromstring(xml_content)

# 4. Extract fields from config
headline_xpath = config["fields"]["headline_path"]
body_xpath = config["fields"]["body_path"]
qcode_xpath = config["fields"]["qcode_path"]

# 5. Iterate over news items (assumes each item is in <item> or similar tag)
items = tree.xpath("//*[local-name()='entry']")

# 6. Validation parameters
required_fields = config["validation"]["required_fields"]
regex_rule = config["validation"]["regex_rules"][0]
regex_field = regex_rule["field"]
pattern = regex_rule["pattern"]
must_match = regex_rule["must_match"]
compiled_pattern = re.compile(pattern)

print(f"🔎 Found {len(items)} items")
print("---")

for i, item in enumerate(items[:5]):  # limit to first 5 for demo
    # Extract fields using XPath relative to item
    headline = item.xpath("title/text()")
    body = item.xpath("summary/text()")
    qcode = item.xpath("link/@href")

    # Convert to string if exists
    headline = headline[0].strip() if headline else None
    body = body[0].strip() if body else None
    qcode = qcode[0].strip() if qcode else None

    # Validate required fields
    missing = []
    if 'headline' in required_fields and not headline: missing.append("headline")
    if 'body' in required_fields and not body: missing.append("body")
    if 'qcode' in required_fields and not qcode: missing.append("qcode")

    # Validate regex rule
    regex_target = body if regex_field == "body" else ""
    regex_match = compiled_pattern.search(regex_target or "")

    print(f"Item {i+1}:")
    print(" Headline:", headline)
    print(" Qcode:", qcode)
    if missing:
        print(" ⚠️  Missing fields:", missing)
    if must_match and not regex_match:
        print(" ⚠️  Regex pattern NOT matched in body")
    print("---")
