import re
from urllib.parse import urlparse

def has_ip_address(url):
    ip_pattern = re.compile(r'(\d{1,3}\.){3}\d{1,3}')
    return 1 if ip_pattern.search(urlparse(url).netloc) else 0

def count_subdomains(url):
    domain = urlparse(url).netloc
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
