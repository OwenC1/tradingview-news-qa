import yaml

# Load YAML config
with open("feed_config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Access top-level values
print("Provider:", config['provider'])
print("Feed URL:", config['url'])

# Access nested XPath paths
headline_xpath = config['fields']['headline_path']
qcode_xpath = config['fields']['qcode_path']
print("Headline XPath:", headline_xpath)
print("Qcode XPath:", qcode_xpath)

# Print validation settings
print("Required fields:", config['validation']['required_fields'])
print("Regex rule:", config['validation']['regex_rules'][0])
