# Remove extra space from columns names 
data.columns = data.columns.str.strip()
print("\nColumns after cleaning", data.columns)
