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
    pass 

def list_raw_data(flags):
    raw_points = filepaths.load_raw_data().copy()
    raw_points = raw_points.reset_index(drop=True)
    # Print the formatted outputs
    print(utils.sepline(65))
    print(
        f"{raw_points.columns[0]:<10} "
        f"{raw_points.columns[1]:<15} "
        f"{raw_points.columns[2]:<50}"
    )  
    print(utils.sepline(65))
    for _, row in raw_points.iterrows():
        print(
            f"{row.iloc[0]:<10} "
            f"{row.iloc[1]:<15} "
            f"{row.iloc[2]:<50}"
        ) 
    print(utils.sepline(65))
    return

def list_date_frequency(flags):
    utils.temporary_output()
    
def list_attendance_proportion(flags):
    utils.temporary_output()

def list_points():
    points = filepaths.load_score_data()
    points = points.reset_index(drop=True)
    print(utils.sepline(80))
    print(
        f"{points.columns[0]:<10} "
        f"{points.columns[1]:^15} "
        f"{points.columns[2]:^20} "
        f"{points.columns[3]:^15} "
        f"{points.columns[4]:^15}"
    )
    print(utils.sepline(80))
    for _, row in points.iterrows():
        print(
            f"{row.iloc[0]:<10} "
            f"{row.iloc[1]:^15} "
            f"{row.iloc[2]:^20} "
            f"{row.iloc[3]:^15} "
            f"{row.iloc[4]:^15}"
        ) 
    print(utils.sepline(80))

def list_point_names():
    utils.temporary_output()
    
def list_point_order():
    utils.temporary_output()
    
def list_individual_attendance(flags):
    utils.temporary_output()