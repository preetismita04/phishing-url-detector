from flask import Flask, render_template, request
import pickle
import pandas as pd
from feature_extraction import extract_features

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=['GET', 'POST'])
def index():
    prediction = None
    url = None

    if request.method == 'POST':
        url = request.form['url']
        features_dict = extract_features(url)
        # Convert dict to DataFrame with a single row to feed into sklearn model
        features_df = pd.DataFrame([features_dict])
        
        # Predict using your model
        pred = model.predict(features_df)[0]
        prediction = "Phishing" if pred == 1 else "Legitimate"

    return render_template("index.html", prediction=prediction, url=url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


