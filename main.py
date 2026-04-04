import pandas as pd 
import numpy as np
from sklearn.preprocessing import LabelEncoder 

data = pd.read_csv("data/combine.csv" , nrows=200000)

print("shape:", data.shape)
print("\nColumns:\n", data.columns)
print("\nFirst 50 rows\n", data.head(50))

# Remove extra space from columns names 
data.columns = data.columns.str.strip()
print("\nColumns after cleaning", data.columns)


# Check data problems

# Missing values
print("\n Missing value: \n")
print(data.isnull().sum())  #This checks missing values (NaN)

#Remove Infinite values

#select only numeric value 
numeric_data = data.select_dtypes(include=[np.number])

print("\n Infinite values \n")
print(np.isinf(numeric_data).sum())

#-----------------
# Label encoding
#----------------- 

# convert label to binary  using label encoding 
le = LabelEncoder()

data['Label'] = le.fit_transform(data['Label'])
print("\nEncoded Label Distribution : \n")
print(data['Label'].value_counts())

#show mapping 
print("\nLabel Mapping:")
for i, label in enumerate(le.classes_):
    print(f"{label} --> {i}")
    
data = data.sample(frac=1, random_state=42).reset_index(drop=True)  #shuffle the data   
print(data['Label'].head(10))
print(data['Label'].tail(10))


# Split features & target (test and train data )

X = data.drop('Label', axis=1)
Y = data['Label']

print("X shape:" , X.shape)
print("Y shape:" , Y.shape)

# Train-Test split 

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=42
)

print("Train:", X_train.shape)
print("Test:", X_test.shape)

# FEATURE SCALING 

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

#fit on training data 
# FEATURE SCAILING 

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# fit on training data 
X_train = scaler.fit_transform(X_train)

# transfrom test data 
X_test = scaler.transform(X_test)

print("Scaling Done ✅")

print("NaN in X_train:" , pd.DataFrame(X_train).isnull().sum().sum())
print("NaN in X_test:" , pd.DataFrame(X_test).isnull().sum().sum())

X_train = np.nan_to_num(X_train)
X_test = np.nan_to_num(X_test)

print("NaN handled sucessfully")

# -------------------------------
# MODEL TRAINING
# -------------------------------

# from sklearn.linear_model import LogisticRegression

# model = LogisticRegression(max_iter=1000)

# model.fit(X_train, Y_train)

# print("Model trained ✅")