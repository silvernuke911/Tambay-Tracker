from datetime import datetime
import csv

# Validation Functions
def validate_date_format(date_string):
    """Validates if the date string is in MM/DD/YY format"""
    try:
        # Attempt to parse the date string to check if it's in the correct format
        datetime.strptime(date_string, r'%m/%d/%y')
        return True  # Return True if successful
    except ValueError:
        return False  # Return False if there's a ValueError

def load_valid_names(filename):
    """Loads valid names from a CSV file into a list."""
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        valid_names = [row[0] for row in reader]
    return valid_names

def is_valid_sender(sender_name, valid_names):
    """Checks if the sender's name is valid."""
    return sender_name in valid_names

def is_valid_members(members, valid_names):
    """Check if all members are valid names from the list."""
    invalid_members = [name for name in members if name not in valid_names]
    return invalid_members 