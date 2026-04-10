from src.preprocessing import preprocess_data
from src.models import get_rf
from src.train import train_model
from src.evaluate import evaluate
from src.sniffer import start_sniffing 

from sklearn.model_selection import train_test_split

def main():
    print("Step 1: Preprocessing...")
    X, y, scaler = preprocess_data("data/combine.csv")

    print("Step 2: Splitting...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Step 3: Model init...")
    rf = get_rf()

    print("Step 4: Training...")
    rf = train_model(rf, X_train, y_train)

    print("Step 5: Predicting...")
    y_pred = rf.predict(X_test)

    print("Step 6: Evaluating...")
    evaluate(y_test, y_pred)

    print("Step 7: Starting Sniffing 🚀")
    start_sniffing()


if __name__ == "__main__":
    main()

