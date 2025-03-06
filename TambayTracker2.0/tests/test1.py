import pandas as pd

data_path = r'TambayTracker2.0\data\raw_data.csv'

df = pd.read_csv(data_path, sep = ":")
print(df)