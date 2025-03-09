from datetime import datetime
from modules import filepaths

def validate_date_format(date_string):
    """Validates if the date string is in MM/DD/YY format"""
    try:
        # Attempt to parse the date string to check if it's in the correct format
        datetime.strptime(date_string, r'%m/%d/%y')
        return True  # Return True if successful
    except ValueError:
        return False  # Return False if there's a ValueError
    
def validate_member(name):
    member_file = filepaths.load_member_data().copy() # df of valid members
    name = name.strip().lower()
    valid_names = member_file['Name'].str.strip().str.lower().tolist()
    if name in valid_names:
        return True
        return False