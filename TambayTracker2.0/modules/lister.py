import pandas as pd

from modules import filepaths

def list_raw_data():
    raw_points = filepaths.raw_data_file.copy()
    raw_points = raw_points.reset_index(drop=True)
    sep_line = "-" * 100
    # Print the formatted outputs
    print(sep_line)
    print(f"{raw_points.columns[0]:<10} {raw_points.columns[1]:<15} {raw_points.columns[2]:<50}")  
    print(sep_line)
    for _, row in raw_points.iterrows():
        print(f"{row.iloc[0]:<10} {row.iloc[1]:<15} {row.iloc[2]:<50}") 
    print(sep_line)
    return

def list_date_frequency():
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
    pass

def list_attendance_proportion():
    pass