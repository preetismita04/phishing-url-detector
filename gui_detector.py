import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import joblib
from urllib.parse import urlparse
import ipaddress

# Load trained model
model = joblib.load('phishing_model.pkl')

# Feature extraction
def extract_features(url):
    features = []
    features.append(len(url))
    features.append(url.count('.'))
    features.append(1 if '@' in url else 0)
    features.append(1 if '-' in url else 0)
    features.append(1 if url.startswith("https") else 0)

    try:
        hostname = urlparse(url).hostname
        features.append(len(hostname.split('.')) - 2 if hostname else 0)
    except:
        features.append(0)

    features.append(sum(char.isdigit() for char in url))

    try:
        ipaddress.ip_address(urlparse(url).hostname)
        features.append(1)
    except:
        features.append(0)

    return features

# Prediction logic
def predict():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Input Error", "Please enter or select a URL.")
        return

    features = extract_features(url)
    prediction = model.predict([features])[0]

    label = "Phishing" if prediction == 1 else "Legitimate"
    result_label.config(
        text=f"⚠️ {label} URL Detected!" if prediction == 1 else f"✅ {label} URL",
        fg="red" if prediction == 1 else "green"
    )

    # Save to log
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("url_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([now, url, label])


# Example URL suggestions
example_urls = [
    "http://192.168.1.1/login",
    "https://www.google.com",
    "http://verify-account-login.com@phishingsite.com",
    "https://secure-bank-login.com",
    "https://www.amazon.com",
    "http://login-facebook.com/account"
]

# GUI setup
root = tk.Tk()
root.title("Phishing URL Detector")
root.geometry("500x250")
root.configure(bg="#f2f2f2")

tk.Label(root, text="Enter or select a URL:", font=("Arial", 12), bg="#f2f2f2").pack(pady=10)

# Combobox for suggestions
url_entry = ttk.Combobox(root, values=example_urls, font=("Arial", 12), width=50)
url_entry.pack(pady=5)
url_entry.set("")  # Blank by default, user can type

tk.Button(root, text="Check URL", font=("Arial", 12), command=predict, bg="#4CAF50", fg="white").pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#f2f2f2")
result_label.pack(pady=10)

root.mainloop()

