import joblib
import os

MODEL_PATH = "coupon_app/ml/coupon_model.pkl"

def predict_coupon(amount_spent, visits):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Please train the model first.")

    model = joblib.load(MODEL_PATH)
    
    # Normalize input (based on assumed normalization during training)
    sample = [[amount_spent / 10000, visits / 50]]

    
    prediction = model.predict(sample)
    return "Yes" if prediction[0] == 1 else "No"

