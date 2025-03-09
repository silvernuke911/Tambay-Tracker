from modules import filepaths
from modules import updaters
from modules import utils

def list_members():
    pass 

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
    updaters.update_date_frequency()
    date_points = filepaths.date_file.copy()
    print(date_points)

def list_attendance_proportion():
    utils.temporary_output()

def list_point_order():
    utils.temporary_output()
    
def list_individual_attendance():
    utils.temporary_output()