from lxml import etree

file_path = "tests/ecb.xml"

try:
    # Try to parse the XML file
    with open(file_path, "rb") as f:
        tree = etree.parse(f)
    print("✅ XML is valid!")

    # Find all currencies and rates
    currencies = tree.xpath("//*[local-name()='Cube'][@currency]")

    for node in currencies:
        code = node.get("currency")
        rate = node.get("rate")
        print(f"{code}: {rate}")

except etree.XMLSyntaxError as e:
    print("❌ XML is not valid!")
    print("Details:", e)
except FileNotFoundError:
    print(f"❌ File not found: {file_path}")
except Exception as e:
    print("❌ Unexpected error:", e)
