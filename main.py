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


# Split features & target (Trian and Test d)

X = data.drop('Label', axis=1)
y = data['Label']

print("X shape:" , X.shape)
print("Y shape:" , y.shape)

# # FEATURE SCAILING 

# from sklearn.preprocessing import StandardScaler

# scaler = StandardScaler()

# # fit on training data 
# X_train = scaler.fit_transform(X_train)

# # transfrom test data 
# X_test = scaler.transform(X_test)

# print("Scaling Done ✅")


