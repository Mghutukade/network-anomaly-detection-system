import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    print("Model trained ✅")

    # Save model
    model_path = os.path.join(BASE_DIR, "model.pkl")
    joblib.dump(model, model_path)

    print(f"Model saved at {model_path} ✅")
    return model