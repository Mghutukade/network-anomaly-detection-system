from src.preprocessing import preprocess_data
from src.models import get_rf
from src.train import train_model
from src.evaluate import evaluate
from src.sniffer import start_sniffing

from sklearn.model_selection import train_test_split

# preprocess
X, y, scaler = preprocess_data("data/combine.csv")

# split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# model
rf = get_rf()

# train
rf = train_model(rf, X_train, y_train)

# predict
y_pred = rf.predict(X_test)

# Sniffing 
start_sniffing()

# evaluate
evaluate(y_test, y_pred)

