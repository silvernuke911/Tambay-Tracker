import sys
import os

# Get the absolute path of the project root directory
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)  # Add parent directory to sys.path

# Now you can import from modules
from modules import filepaths
import pandas as pd 

df = filepaths.raw_data_file.copy()
attendance_count = df.groupby("Date")["Sender Name"].nunique()
df["Members Present"] = df["Members Present"].str.split(", ")
member_count = df.groupby("Date")["Members Present"].sum().apply(lambda x: len(set(x)))
all_dates = pd.date_range(start="2024-10-09", end="2024-10-13").strftime("%m/%d/%y")
final_df = pd.DataFrame({"Date": all_dates})
final_df = final_df.merge(attendance_count, on="Date", how="left").merge(member_count, on="Date", how="left")
final_df = final_df.fillna(0).astype(int)
final_df["Member Count"] = 23
final_df.to_csv("attendance_summary.csv", index=False)
print(final_df)