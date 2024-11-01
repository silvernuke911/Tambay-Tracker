import numpy as np
import csv
import os
from datetime import datetime

# Validation Functions
def validate_date_format(date_string):
    """Validates if the date string is in MM/DD/YY format."""
    try:
        # Attempt to parse the date string
        datetime.strptime(date_string, '%m/%d/%y')
        return True  # Return True if successful
    except ValueError:
        return False  # Return False if there's a ValueError

def load_valid_names(filename):
    """Loads valid names from a CSV file into a list."""
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        valid_names = [row[0] for row in reader]  # Assumes names are in the first column
    return valid_names

def is_valid_sender(sender_name, valid_names):
    """Checks if the sender's name is valid."""
    return sender_name in valid_names

valid_names = load_valid_names('member_list.csv')
def is_valid_members(members, valid_names):
    """Check if all members are valid names from the list."""
    invalid_members = [name for name in members if name not in valid_names]
    return invalid_members  # Return the list of invalid members, or an empty list if all are valid


program_options = ['Enter new entry','Show raw data', 'Visualize Data', 'Show Points', 'Show Point Order', 'Show Date Frequency', 'Exit']

# Terminal options
def clear_screen():
    """Clears the terminal screen."""
    # Clear command based on operating system
    os.system('cls' if os.name == 'nt' else 'clear')

def set_terminal_size(width=100, height=30):
    os.system(f'mode con: cols={width} lines={height}')

def safe_exit():
    update_points()
    update_date_frequency()
    exit()

# Main system
def get_yes_no_input(prompt_text, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        response = input(prompt_text).strip().lower()
        if response in ['y', 'n']:
            return response
        print('Invalid entry, please try again.')
        attempts += 1
    print("Too many invalid attempts. Exiting program.")
    safe_exit()

def get_option_input(options, max_attempts=5):
    print('What else would you like to do?')
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    attempts = 0
    while attempts < max_attempts:
        try:
            choice = int(input('Input number of desired option: ').strip())
            if 1 <= choice <= len(options):
                return choice
            else:
                print('Invalid entry, please try again.')
        except ValueError:
            print('Invalid entry, please enter a number.')
        attempts += 1
    print("Too many invalid attempts. Exiting program.")
    safe_exit()

def starting_menu():
    print(f'WELCOME TO THE TAMBAY TRACKER!\n')
    prompt = get_yes_no_input('Do you want to put a new entry? (Y/N): ')
    if prompt == 'y':
        return 'y'
    elif prompt == 'n':
        return get_option_input(program_options)
    
def get_input_with_quit(prompt):
    """Helper function to get input and check for 'QUIT' condition."""
    user_input = input(prompt)
    if user_input == 'QUIT':
        return None  # Signal to quit
    return user_input  # Return the normal input

def get_entry_input():
    while True:
        # Validate date input
        date = get_input_with_quit('Date (MM/DD/YY) : ')
        if date is None:  # Check if 'QUIT' was entered
            break
        while not validate_date_format(date):
            print("Invalid date format. Please enter the date in MM/DD/YY format.")
            date = get_input_with_quit('Date (MM/DD/YY) : ')
            if date is None:  # Check again for 'QUIT'
                break
        if date is None:
            break  # Exit the main loop if 'QUIT' was entered

        # Validate sender name input
        sender = get_input_with_quit('Sender name : ')
        if sender is None:
            break
        while not is_valid_sender(sender, valid_names):
            print("Invalid sender name. Please enter a valid name from the list.")
            sender = get_input_with_quit('Sender name : ')
            if sender is None:
                break
        if sender is None:
            break

        # Validate members present input
        while True:
            members_present = get_input_with_quit('Members present (comma-separated) : ')
            if members_present is None:
                break
            members_present_list = [name.strip() for name in members_present.split(',')]  # Split and strip whitespace

            # Validate members present using the is_valid_members function
            invalid_members = is_valid_members(members_present_list, valid_names)
            if not invalid_members:  # If no invalid members, break out of the loop
                break  # Exit the member validation loop
            print(f"Invalid member(s) present: {', '.join(invalid_members)}. Please enter valid names.")
        
        if date is None or sender is None:  # Check if 'QUIT' was entered during input
            break

        # Save entry
        save_entry(date, sender, members_present)

        # Ask if the user wants to add another entry
        another_entry = get_yes_no_input('Do you want to add another entry? (Y/N): ')
        if another_entry == 'n':
            break
        
def save_entry(date, sender, members_present):
    # Saving the entry to a CSV file with ':' as the delimiter
    with open('shit_tests/tambay_tracker_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=':')
        writer.writerow([date, sender, members_present])
    print("Entry saved successfully.")
    return 

def handle_option_choice(option_choice):
    """Handle the user's selection from program options."""
    if   option_choice == 1:
        get_entry_input()
    elif option_choice == 2:
        print("Executing 'Showing raw data'...")
        print('\n')
        show_raw_data()
        print('\n')
    elif option_choice == 3:
        print("Executing 'Visualizing Data'...")
        # Insert functionality here for 'Visualize Data'
    elif option_choice == 4:
        print("Executing 'Showing Points List'...")
        # Insert functionality here for 'Show Points'
    elif option_choice == 5:
        print("Executing 'Showing Point Order List and Graph'...")
        # Insert functionality here for 'Show Point Order'
    elif option_choice == 6:
        print("Executing 'Show Date Frequency List and Graph'...")
        # Insert functionality here for 'Show Date Frequency'
    elif option_choice == 7:
        exit_question = get_yes_no_input('Are you sure you want to exit? (Y/N): ')
        if exit_question == 'y':
            safe_exit()
        else:
            input('Returning to the main menu. Press enter')

# Options
def update_points():
    pass

def update_date_frequency():
    pass

def show_raw_data():
    try:
        with open(r'shit_tests\tambay_tracker_data.csv', mode='r') as file:
            reader = csv.reader(file, delimiter=':')
            for row in reader:
                sender_name = row[1].ljust(10)
                print(f"Date: {row[0]},\t Sender: {sender_name},\t Members Present: {row[2]}")
    except FileNotFoundError:
        print("The data file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def visualize_data():
    pass 

def show_points():
    pass 

def show_point_order():
    pass 

def show_date_freq():
    pass 

def random_data_generator():
    pass

def main():
    prompt = starting_menu() 
    if prompt == 'y':
        # clear_screen()
        get_entry_input()  
    while True:
        option_choice = get_option_input(program_options)
        # clear_screen()
        handle_option_choice(option_choice)

if __name__ == '__main__':
    main()

