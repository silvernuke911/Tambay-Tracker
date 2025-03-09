import pandas as pd

csvpath = r'C:\Users\ADMIN\Documents\TambayTracker2\TambayTracker2.0\data\sample.csv'
csvfile = pd.read_csv(csvpath)
print(csvfile)