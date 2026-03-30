import pandas as pd 

data = pd.read_csv("data/combine.csv" , nrows=50000)

print("shape:", data.shape)
print("\nColumns:\n", data.columns)
print("\nFirst 50 rows\n", data.head(50))

# Remove extra space from columns names 
data.columns = data.columns.str.strip()
print("\nColumns after cleaning", data.columns)



