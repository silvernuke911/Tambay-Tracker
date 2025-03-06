import pandas as pd

# Load the CSV file
daw = r'TambayTracker2.0\data\raw_data.csv'
raw_data_file = pd.read_csv(daw, sep=':')

df = raw_data_file.copy()
# Split members into lists and strip spaces
df["Members Present"] = df["Members Present"].str.split(",").apply(lambda members: [member.strip() for member in members])
# Group by date and remove duplicates
df = df.groupby("Date")["Members Present"].sum()  # Flatten lists per date
df = df.apply(lambda members: sorted(set(members))).reset_index()  # Remove duplicates
df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%y")
# Create a complete date range
all_dates = pd.date_range(start=df["Date"].min(), end=df["Date"].max(), freq="D")
df_full = pd.DataFrame({"Date": all_dates})
# Merge with the original DataFrame
df = df_full.merge(df, on="Date", how="left")
# Fill missing members with empty lists and attendance count with 0
df["Members Present"] = df["Members Present"].apply(lambda x: x if isinstance(x, list) else [])
df["Attendance Count"] = df["Members Present"].apply(len)
# Convert Date back to the desired format
df["Date"] = df["Date"].dt.strftime("%m/%d/%y")
df = df.drop(columns=["Members Present"])
df.to_csv('attendance_summary.csv', index = False)
