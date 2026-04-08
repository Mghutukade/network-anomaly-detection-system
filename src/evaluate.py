# Evaluate fina model      
from sklearn.metrics import accuracy_score, classification_report

print("Hybrid Accuracy:", accuracy_score(y_test, final_pred))
print(classification_report(y_test, final_pred))