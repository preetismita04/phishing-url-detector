import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Load features and labels from url_features.csv
df = pd.read_csv("url_features.csv")

# Separate features (X) and target label (y)
X = df.drop("label", axis=1)
y = df["label"]

# Split data into train and test sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize the Random Forest Classifier
model = RandomForestClassifier()

# Train the model on training data
model.fit(X_train, y_train)

# Predict on the test data
y_pred = model.predict(X_test)

# Calculate and print accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.2f}")

# Save the trained model to model.pkl
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved as 'model.pkl'")
