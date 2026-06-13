import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = {
    "length": [10, 15, 20, 40, 50, 60],
    "dots": [1, 1, 2, 3, 4, 5],
    "has_https": [1, 1, 1, 0, 0, 0],
    "label": [0, 0, 0, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["length", "dots", "has_https"]]
y = df["label"]

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "phishing_model.pkl")

print("Model trained successfully")