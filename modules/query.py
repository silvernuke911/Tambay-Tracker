import matplotlib.pyplot as plt
from datetime import datetime
from modules import safe_exit

def get_input_with_quit(prompt):
    """Helper function to get input and check for 'QUIT' condition."""
    user_input = input(prompt)
    if user_input == 'QUIT':
        return None  # Signal to quit
    return user_input  # Return the normal input

def get_yes_no_input(prompt_text, raw_data_file, score_file, date_file, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        response = input(prompt_text).strip().lower()
        if response in ['y', 'n']:
            return response
        print('Invalid entry, please try again.')
        attempts += 1
    print("Too many invalid attempts. Exiting program.")
    # print("Please stop putting wrong inputs, I will destroy you and your entire fucking bloodline, it's a yes/no question why you gotta put in random shit you fucking retard")
    safe_exit.safe_exit(raw_data_file, score_file, date_file)

def get_option_input(options, raw_data_file, score_file, date_file, max_attempts=5):
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
    safe_exit.safe_exit(raw_data_file, score_file, date_file)

def prompt_for_integer(prompt_message):
        while True:
            user_input = input(prompt_message)
            try:
                return int(user_input)
            except ValueError:
                if user_input == 'QUIT':
                    return None
                else: 
                    print("Invalid input. Please enter a valid integer.")

def save_image_query(filename,  raw_data_file, score_file, date_file):
    response = get_yes_no_input('Do you want to save the image? (Y/N) :', raw_data_file, score_file, date_file)
    if response == 'y':
        current_datetime = datetime.now().strftime(r"%Y%m%d-%H%M%S")
        plt.savefig(f'Images\\{filename} {current_datetime}.png', format="png", dpi=300)
        print('Image saved')
    return 

def get_valid_date():
    """Prompt the user for a date in MM/DD/YY format and validate it."""
    while True:
        date_str = input("Until what date should the graph be plotted? (MM/DD/YY) (press Enter for date today): ")
        if date_str == '':
            date_str = datetime.now().strftime(r"%m/%d/%y")  # Use %y for 2-digit year
        try:
            # Try to parse the date to ensure it's in the correct format
            date_obj = datetime.strptime(date_str, r"%m/%d/%y")
            return date_obj
        except ValueError:
            print("Invalid date format. Please enter the date in MM/DD/YY format.")