import joblib
import pandas as pd
from urllib.parse import urlparse
import re

def extract_features(url):
    parsed = urlparse(url)
    hostname = parsed.netloc
    return {
        'url': url,
        'url_length': len(url),
        'num_dots': url.count('.'),
        'has_at_symbol': int('@' in url),
        'has_hyphen': int('-' in hostname),
        'is_https': int(parsed.scheme == 'https'),
        'num_subdomains': max(0, hostname.count('.') - 1),
        'num_digits': len(re.findall(r'\d', url)),
        'has_ip_address': int(bool(re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', hostname))),
    }

# Load model
model = joblib.load('phishing_model.pkl')

# Loop for user input
while True:
    url = input("🔗 Enter a URL (or type 'exit' to quit): ").strip()
    if url.lower() == 'exit':
        break
    features = extract_features(url)
    X = pd.DataFrame([features]).drop(columns=['url'])
    prediction = model.predict(X)[0]
    result = "Phishing" if prediction == 1 else "Legitimate"
    print(f"✅ Prediction for '{url}': {result}")
