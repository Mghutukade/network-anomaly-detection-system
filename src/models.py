from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, IsolationForest

# Logistic Regression
def get_logistic():
    return LogisticRegression(max_iter=1000)

# Random Forest
def get_rf():
    return RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

# Isolation Forest (Unsupervised)
def get_isolation():
    return IsolationForest(
        n_estimators=100,
        contamination='auto',
        random_state=42
    )