from lxml import etree

with open("tests/ecb.xml", "rb") as f:
    tree = etree.parse(f)

# Find all currencies and rates
currencies = tree.xpath("//*[local-name()='Cube'][@currency]")

for node in currencies:
    code = node.get("currency")
    rate = node.get("rate")
    print(f"{code}: {rate}")
