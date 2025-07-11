import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from .preprocessing import preprocess_dataset

MODEL_PATH = "coupon_app/ml/coupon_model.pkl"

def train_model(csv_file_path):
    df = preprocess_dataset(csv_file_path)

    # Ensure required columns exist
    if not {'amount_spent', 'visits', 'issue_coupon'}.issubset(df.columns):
        raise ValueError("Dataset must include 'amount_spent', 'visits', and 'issue_coupon' columns.")
    
    # Use only selected features
    X = df[['amount_spent', 'visits']].copy()
    
    # Normalize features to match prediction scaling
    X['amount_spent'] = X['amount_spent'] / 10000
    X['visits'] = X['visits'] / 50

    # Convert labels to binary (Yes → 1, No → 0)
    y = df['issue_coupon'].map({'Yes': 1, 'No': 0})

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, MODEL_PATH)
    return f"Model trained and saved to {MODEL_PATH}"
