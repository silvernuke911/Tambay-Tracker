import textwrap
import pandas as pd 

from datetime import datetime
from modules import filepaths
from modules import utils

def list_members(flags):
    member_list = filepaths.load_member_data().copy()
    member_list = member_list.reset_index(drop=True)
    print(utils.sepline(80))
    print(
        f"{member_list.columns[0]:<15} "
        f"{member_list.columns[1]:^5} "
        f"{member_list.columns[2]:^10} " 
        f"{member_list.columns[3]:^10}"
    )  
    print(utils.sepline(80))
    for _, row in member_list.iterrows():
        print(
            f"{row.iloc[0]:<15} "
            f"{row.iloc[1]:^5} "
            f"{row.iloc[2]:^10} "
            f"{row.iloc[3]:^10}"
        ) 
    print(utils.sepline(80))
    return

def list_raw_data(flags):
    raw_points = filepaths.load_raw_data().copy()
    raw_points = raw_points.reset_index(drop=True)
    # Print the formatted outputs
    print(utils.sepline(80))
    print(
        f"{raw_points.columns[0]:<10} "
        f"{raw_points.columns[1]:<15} "
        f"{raw_points.columns[2]:<50}"
    )  
    print(utils.sepline(80))
    for _, row in raw_points.iterrows():
        print(
            f"{row.iloc[0]:<10} "
            f"{row.iloc[1]:<15} "
            f"{row.iloc[2]:<50}"
        ) 
    print(utils.sepline(80))
    return

def list_date_frequency(flags):
    data = filepaths.load_date_data()
    data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%y')
    try:
        start_date = pd.to_datetime(
            flags.get(
                'startdate',
                '01/20/25'
            ), format='%m/%d/%y'
        )
        end_date = pd.to_datetime(
            flags.get(
                'enddate', 
                datetime.today().strftime('%m/%d/%y')
            ), 
            format='%m/%d/%y'
        )
    except ValueError:
        print("Error: Date format is wrong, please use MM/DD/YY")
        return
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    if flags.get('rmwknd', False):
        filtered_data = filtered_data[~filtered_data['Day'].isin(['Saturday', 'Sunday'])]
    filtered_data = filtered_data.copy()
    filtered_data['Date'] = filtered_data['Date'].dt.strftime('%m/%d/%y')
    if flags.get('rmdays', False):
        filtered_data = filtered_data.drop(columns=['Day'])
    filtered_data = filtered_data.reset_index(drop=True)
    
    print(utils.sepline(80))
    if flags.get('rmdays', False):
        print(
            f"{filtered_data.columns[0]:^8} "
            f"{filtered_data.columns[1]:^15}"
        )
    else:
        print(
            f"{filtered_data.columns[0]:^8} "
            f"{filtered_data.columns[1]:^15} "
            f"{filtered_data.columns[2]:^15}"
        )
    print(utils.sepline(80))
    for _, row in filtered_data.iterrows():
        if flags.get('rmdays', False):
            print(
                f"{row.iloc[0]:^8} "  
                f"{row.iloc[1]:^15}"  
            )
        else:
            print(
                f"{row.iloc[0]:^8} " 
                f"{row.iloc[1]:^15} "  
                f"{row.iloc[2]:^15}"  
            )
    print(utils.sepline(80))
    # Handle the 'wkave' flag (average weekly attendance)
    if flags.get('wkave', False):
        # TODO: Implement weekly average attendance calculation
        print("Warning: The --wkave flag is not yet implemented.")
    return

def list_points():
    point_list = filepaths.load_score_data().copy()
    point_list = point_list.reset_index(drop=True)
    print(utils.sepline(80))
    print(
        f"{point_list.columns[0]:<15} "
        f"{point_list.columns[1]:^15} "
        f"{point_list.columns[2]:^15} "
        f"{point_list.columns[3]:^15} "
        f"{point_list.columns[4]:^15}"
    )
    print(utils.sepline(80))
    for _, row in point_list.iterrows():
        print(
            f"{row.iloc[0]:<15} "
            f"{row.iloc[1]:^15} "
            f"{row.iloc[2]:^15} "
            f"{row.iloc[3]:^15} "
            f"{row.iloc[4]:^15}"
        )
    print(utils.sepline(80))
    pass

def list_cmdlog(flags):
    if not flags:  # Default to --today
        flags = {"today": True}
    cmdlog_file = filepaths.cmdlog_path
    cmd_list = pd.read_csv(cmdlog_file, dtype=str).fillna("")
    target_date = None
    if flags.get("today", False):
        target_date = datetime.now().strftime("%m/%d/%Y")
    elif "date" in flags:
        raw_date = flags["date"]
        if not isinstance(raw_date, str) or not raw_date.strip():
            target_date = datetime.now().strftime("%m/%d/%Y")
        else:
            for fmt in ("%m/%d/%Y", "%m/%d/%y"):
                try:
                    dt = datetime.strptime(raw_date, fmt)
                    target_date = dt.strftime("%m/%d/%Y")
                    break
                except ValueError:
                    continue
            else:
                print(utils.sepline(60))
                print(f"Invalid date format: '{raw_date}' (use MM/DD/YYYY or MM/DD/YY)")
                return
    if target_date:
        cmd_list = cmd_list[cmd_list["Date"] == target_date]
    if cmd_list.empty and target_date:
        print(utils.sepline(40))
        print(f"No command logs found for {target_date}")
        print(utils.sepline(40))
        return
    cmd_list = cmd_list.reset_index(drop=True)
    print(utils.sepline(85))
    print(
        f"{'Date':^15} "
        f"{'Time':^15} "
        f"{'Input':^50}"
    )
    print(utils.sepline(85))
    for _, row in cmd_list.iterrows():
        wrapped_cmd = textwrap.fill(row["Input"], width=50)
        cmd_lines = wrapped_cmd.split("\n")
        print(
            f"{row['Date']:^15} "
            f"{row['Time']:^15} "
            f"{cmd_lines[0]:<50}"
        )
        for line in cmd_lines[1:]:
            print(
                f"{'':<15} "
                f"{'':<15} "
                f"{line:<50}"
            )
    print(utils.sepline(85))

def list_attendance_proportion(flags):
    ## attendance proportion
    utils.temporary_output()

def list_point_names():
    utils.temporary_output()
    
def list_point_order(flags):
    point_list = filepaths.load_score_data().copy()
    sort_factor = 'Total Points'
    if flags.get('total'):
        sort_factor = 'Total Points'
    elif flags.get('attendance'):
        sort_factor = 'Attendance Count'
    elif flags.get('sender'):
        sort_factor = 'Sender Count'
    point_list = point_list.sort_values(by=sort_factor, ascending=False).reset_index(drop=True)
    print(utils.sepline(80))
    print(
        f"{point_list.columns[0]:<15} "
        f"{point_list.columns[1]:^15} "
        f"{point_list.columns[2]:^15} "
        f"{point_list.columns[3]:^15} "
        f"{point_list.columns[4]:^15}"
    )
    print(utils.sepline(80))
    for _, row in point_list.iterrows():
        print(
            f"{row.iloc[0]:<15} "
            f"{row.iloc[1]:^15} "
            f"{row.iloc[2]:^15} "
            f"{row.iloc[3]:^15} "
            f"{row.iloc[4]:^15}"
        )
    print(utils.sepline(80))
    return
    utils.temporary_output()
    
def list_individual_attendance(flags):
    utils.temporary_output()