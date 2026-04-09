import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(file_path):

    data = pd.read_csv(file_path, nrows=200000)

    # clean column names
    data.columns = data.columns.str.strip()

    # label encoding
    le = LabelEncoder()
    data['Label'] = le.fit_transform(data['Label'])

    # shuffle
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    # split features & target
    X = data.drop('Label', axis=1)
    y = data['Label']

    # scaling
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # handle NaN
    X = np.nan_to_num(X)

    return X, y, scaler