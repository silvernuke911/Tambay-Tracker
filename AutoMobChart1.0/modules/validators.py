from datetime import datetime
from modules import filepaths
from modules import utilities

def validate_date_format(date_string):
    """Validates if the date string is in MM/DD/YY format"""
    try:
        # Attempt to parse the date string to check if it's in the correct format
        datetime.strptime(date_string, r'%m/%d/%y')
        return True  # Return True if successful
    except ValueError:
        return False  # Return False if there's a ValueError
    
def validate_member(name):
    """Validates if the name in the member is valid"""
    member_file = filepaths.load_member_data().copy() # df of valid members
    name = name.strip().lower()
    valid_names = member_file['Name'].str.strip().str.lower().tolist()
    if name in valid_names:
        return True
    else:
        return False
    
def validate_flags(flags, valid_flags, noun):
    for flag in flags.keys():
        if flag not in valid_flags:
            print(utilities.sepline)
            print(f"Error: '{flag}' is not a known flag for {noun}")
            print(utilities.sepline)
            return False
    return True