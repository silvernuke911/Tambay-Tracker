from modules import filepaths
from modules import utils

def list_members():
    member_list = filepaths.load_member_data().copy()
    member_list = member_list.reset_index(drop=True)
    print(utils.sepline(80))
    print(f"{member_list.columns[0]:<15} {member_list.columns[1]:^5} {member_list.columns[2]:^10} {member_list.columns[3]:^10}")  
    print(utils.sepline(80))
    for _, row in member_list.iterrows():
        print(f"{row.iloc[0]:<15} {row.iloc[1]:^5} {row.iloc[2]:^10} {row.iloc[3]:^10}") 
    print(utils.sepline(80))
    pass 

def list_raw_data():
    raw_points = filepaths.load_raw_data().copy()
    raw_points = raw_points.reset_index(drop=True)
    # Print the formatted outputs
    print(utils.sepline(65))
    print(f"{raw_points.columns[0]:<10} {raw_points.columns[1]:<15} {raw_points.columns[2]:<50}")  
    print(utils.sepline(65))
    for _, row in raw_points.iterrows():
        print(f"{row.iloc[0]:<10} {row.iloc[1]:<15} {row.iloc[2]:<50}") 
    print(utils.sepline(65))
    return

def list_date_frequency():
    utils.temporary_output()
    
def list_attendance_proportion():
    utils.temporary_output()

def list_point_order():
    utils.temporary_output()
    
def list_individual_attendance():
    utils.temporary_output()