from lxml import etree

# Load your XML file
tree = etree.parse("data/newsMessage_sample.xml")

# Run XPath to get the headline text
headline = tree.xpath("//*[local-name()='headline']/text()")
headline = headline[0].strip() if headline else "N/A"

# Get subject qcode
subject_code = tree.xpath("//*[local-name()='subject']/@qcode")
print("Subject qcode:", subject_code)

# Get country name
country = tree.xpath("//*[local-name()='name']/text()")
print("Country:", country)

# Get language
language = tree.xpath("//*[local-name()='language']/@tag")
print("Language:", language)

# Get copywright holder qcode
copyright_code = tree.xpath("//*[local-name()='copyrightHolder']/@qcode")
print("copyright Holder qcode:", copyright_code)

