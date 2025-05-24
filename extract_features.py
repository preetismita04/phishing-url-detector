import pandas as pd
import re
from urllib.parse import urlparse

def has_ip_address(url):
    # Check if URL contains an IP address instead of a domain
    ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
    return 1 if ip_pattern.search(urlparse(url).netloc) else 0

def count_subdomains(url):
    domain = urlparse(url).netloc
    # Count subdomains by counting dots in domain minus 1 (for main domain)
    return domain.count('.') - 1 if domain.count('.') > 1 else 0

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_dots'] = url.count('.')
    features['has_at'] = 1 if '@' in url else 0
    features['has_hyphen'] = 1 if '-' in urlparse(url).netloc else 0
    features['is_https'] = 1 if url.startswith('https://') else 0
    features['num_subdomains'] = count_subdomains(url)
    features['digit_count'] = sum(c.isdigit() for c in url)
    features['has_ip'] = has_ip_address(url)
    return features

# Load urls.csv
df = pd.read_csv("urls.csv")

# Extract features for each URL
features_list = []
for url in df['url']:
    features_list.append(extract_features(url))

# Create a dataframe from features
##features_df = pd.DataFrame(features_list)
features_df = extract_features(url)
print(features_df)
print(type(features_df))
print(features_df.dtypes)
# Combine features and label
final_df = pd.concat([features_df, df['label']], axis=1)

# Save to url_features.csv
final_df.to_csv("url_features.csv", index=False)

print("✅ Features extracted and saved to 'url_features.csv'")
