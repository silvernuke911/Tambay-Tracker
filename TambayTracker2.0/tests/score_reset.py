import pandas as pd

mem_dir = r"C:\Users\verci\Documents\code\Tambay-Tracker\TambayTracker2.0\data\member_list.csv"
mems = pd.read_csv(mem_dir)

# Sort alphabetically by "Name"
mems = mems.sort_values(by=["Name"])

# Print each member line
for name in mems["Name"]:
    print(f"{name},0,0,0,0")
