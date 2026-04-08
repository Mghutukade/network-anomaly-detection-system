# -------------------------------
# MODEL TRAINING
# -------------------------------

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

print("Model trained ✅")

y_pred = model.predict(X_test)

from sklearn.metrics import accuracy_score, classification_report

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print(data.corr()['Label'].sort_values(ascending=False))

# remove constant from the column 
data = data.loc[:, data.nunique() > 1]


#-----------------------------------------
# RANDOM FOREST MODLE
#-----------------------------------------

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)

rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

from sklearn.metrics import accuracy_score

print("RF Accuracy:", accuracy_score(y_test, y_pred_rf))

#  Feature importance --------------
importance = rf.feature_importances_

imp_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

print(imp_df.head(10))


# # visualize using matplot library 
# import matplotlib.pyplot as plt # for visualization 

# imp_df.head(10).plot(kind='barh', x='Feature', y='Importance')
# plt.show()


#---------------------------
# Isolation forest Algo 
#---------------------------

from sklearn.ensemble import IsolationForest

iso = IsolationForest(
    n_estimators=100,
    contamination='auto',  # % of anomalies (tune later) 
    random_state=42
)

iso.fit(X_train)

# Predict 
y_pred_iso = iso.predict(X_test) 

# Convert to 0 (normal) and 1 (attack)
y_pred_iso = [1 if x == -1 else 0 for x in y_pred_iso]


# Evaluate 
from sklearn.metrics import classification_report, accuracy_score

print("Isolation Forest Accuracy:", accuracy_score(y_test, y_pred_iso))
print(classification_report(y_test, y_pred_iso))

rf_pred = rf.predict(X_test) 
