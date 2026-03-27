import pandas as pd 

data = pd.read_csv("data/combine.csv" , nrows=50000)

print("shape:", data.shape)
print("\nColumns:\n", data.columns)
print("\nFirst 5 rows\n", data.head(50))

