import numpy as np
import csv
import os
from datetime import datetime
from collections import Counter, defaultdict
import matplotlib.pyplot as plt

raw_data_file = 'tambay_tracker_data.csv'
date_file = 'date_list.csv'
score_file = 'scores_list.csv'
member_file = 'member_list.csv'

def latex_font(): # Aesthetic choice
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=12)

def latex_font1(): # Aesthetic choice
    import matplotlib as mpl
    import matplotlib.font_manager as font_manager
    plt.rcParams.update({
        'font.family': 'serif',
        'mathtext.fontset': 'cm',
        'axes.unicode_minus': False,
        'axes.formatter.use_mathtext': True,
        'font.size': 12
    })
    cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
latex_font()

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
        valid_names = [row[0] for row in reader]
    return valid_names

def is_valid_sender(sender_name, valid_names):
    """Checks if the sender's name is valid."""
    return sender_name in valid_names

valid_names = load_valid_names(member_file)

def is_valid_members(members, valid_names):
    """Check if all members are valid names from the list."""
    invalid_members = [name for name in members if name not in valid_names]
    return invalid_members 

program_options = ['Enter new entry','Show raw data', 'Visualize Data', 'Show Points', 'Show Point Order', 'Show Date Frequency', 'Exit']

# Update functions
def update_scores():
    sender_counts = Counter()
    attendee_counts = Counter()
    with open(raw_data_file, mode='r') as data_file:
        reader = csv.reader(data_file, delimiter=':')
        for row in reader:
          
            sender_name = row[1].strip()
            sender_counts[sender_name] += 1

            members_present = row[2].split(', ')
            attendee_counts.update(members_present)
    updated_scores = []
    with open(score_file, mode='r') as scores_file:
        reader = csv.reader(scores_file)
        next(reader)  
        for row in reader:
            name = row[0]
            updated_sender_count = sender_counts.get(name, 0)
            updated_attendee_count = attendee_counts.get(name, 0)
            updated_total_score = updated_sender_count + updated_attendee_count
            updated_scores.append([name, updated_sender_count, updated_attendee_count, updated_total_score ])
    with open(score_file, mode='w', newline='') as scores_file:
        writer = csv.writer(scores_file)
        writer.writerow(["Name", "Sender Count", "Attendance Count", 'Total points']) 
        writer.writerows(updated_scores)
    print("Scores updated successfully.")

def update_date_freq():
    date_attendance_count = defaultdict(set)  # Using a set to ensure uniqueness
    
    # Initialize attendance count from 'date_file'
    with open(date_file, mode='r') as date_file_:
        reader = csv.reader(date_file_)
        next(reader)  # Skip header
        for row in reader:
            if row:
                date = row[0].strip()
                date_attendance_count[date] = set()  # Initialize an empty set for each date

    # Read entries from 'raw_data_file' and collect unique members per date
    with open(raw_data_file, mode='r') as data_file:
        reader = csv.reader(data_file, delimiter=':')
        for row in reader:
            if not row or len(row) < 3:
                continue  # Skip empty or incomplete rows
            date = row[0].strip()
            members_present = row[2].split(', ')
            if date in date_attendance_count:
                date_attendance_count[date].update(members_present)  # Add members uniquely

    # Calculate attendance count per date and write to 'date_file'
    with open(date_file, mode='w', newline='') as date_file_:
        writer = csv.writer(date_file_)
        writer.writerow(["Date", "Attendance Count"])  # Write header
        for date, members in date_attendance_count.items():
            writer.writerow([date, len(members)])  # Count unique members per date

    print("Date attendance frequency updated successfully.")

# Terminal options
def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def set_terminal_size(width=100, height=30):
    os.system(f'mode con: cols={width} lines={height}')

def safe_exit():
    update_scores()
    update_date_freq()
    print('Exiting...')
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
    # print("Please stop putting wrong inputs, I will destroy you and your entire fucking bloodline, it's a yes/no question why you gotta put in random shit you fucking retard")
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
    return get_yes_no_input('Do you want to put a new entry? (Y/N): ')
    
def get_input_with_quit(prompt):
    """Helper function to get input and check for 'QUIT' condition."""
    user_input = input(prompt)
    if user_input == 'QUIT':
        return None  # Signal to quit
    return user_input  # Return the normal input

def save_entry(date, sender, members_present):
    # Saving the entry to a CSV file with ':' as the delimiter
    with open(raw_data_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=':')
        writer.writerow([date, sender, members_present])
    print("Entry saved successfully.")
    return 

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

def handle_option_choice(option_choice):
    """Handle the user's selection from program options."""
    if   option_choice == 1:
        get_entry_input()
    elif option_choice == 2:
        print("Showing raw data...")
        print('\n')
        show_raw_data()
        print('\n')
    elif option_choice == 3:
        print("Visualizing Data...")
        visualize_data()
    elif option_choice == 4:
        print("Showing Points List...")
        show_points()
    elif option_choice == 5:
        print("Showing Point Order List and Graph...")
        show_point_order()
        visualize_data_ordered()
    elif option_choice == 6:
        print("Showing Date Frequency List and Graph...")
        plot_date_frequency()
    elif option_choice == 7:
        exit_question = get_yes_no_input('Are you sure you want to exit? (Y/N): ')
        if exit_question == 'y':
            safe_exit()
        else:
            input('Returning to the main menu. Press enter')

def show_raw_data():
    try:
        with open(raw_data_file, mode='r') as file:
            reader = csv.reader(file, delimiter=':')
            for row in reader:
                date_ = row[0].ljust(5)
                sender_name = row[1].ljust(10)
                print(f"Date: {date_},\t Sender: {sender_name},\t Members Present: {row[2]}")

    except FileNotFoundError:
        print("The data file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_points():
    try:
        with open(score_file, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                member_name = row[0].ljust(10)
                points = row[3].ljust(3)
                print(f"Member: {member_name},\t Points: {points}")
    except FileNotFoundError:
        print("The data file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def visualize_data():
    names = []
    total_scores = []
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if len(row) < 3:
                continue  
            name = row[0]
            sender_count = int(row[1]) if row[1].isdigit() else 0
            attendance_count = int(row[2]) if row[2].isdigit() else 0
            total_score = sender_count + attendance_count
            names.append(name)
            total_scores.append(total_score)
    # Plot the bar graph
    plt.bar(names, total_scores, color='r')
    plt.xlabel('Names')
    plt.ylabel('Total Score')
    plt.title('Scores Bar Graph (Original Order)')
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()
    plt.show()

def visualize_data_ordered():
    scores = {}
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) < 3:
                continue 
            name = row[0]
            sender_count = int(row[1]) if row[1].isdigit() else 0
            attendance_count = int(row[2]) if row[2].isdigit() else 0
            total_score = sender_count + attendance_count
            scores[name] = total_score
    # Sort scores from highest to lowest
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    names, total_scores = zip(*sorted_scores)
    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(names, total_scores, color='b')
    plt.xlabel('Brod Names')
    plt.ylabel('Total Score')
    plt.title(r'\textbf{Scores Bar Graph (Sorted)}')
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()
    save_image_query('Ordered Points')
    plt.show()

def show_points():
    try:
        with open(score_file, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for row in reader:
                member_name = row[0].ljust(10)
                points = row[3].ljust(3)
                print(f"Member: {member_name},\t Points: {points}")
    except FileNotFoundError:
        print("The data file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_point_order():
    scores = {}
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if len(row) < 3:
                continue
            name = row[0]
            sender_count = int(row[1]) if row[1].isdigit() else 0
            attendance_count = int(row[2]) if row[2].isdigit() else 0
            total_score = sender_count + attendance_count
            scores[name] = total_score
    # Sort scores from highest to lowest
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    names, total_scores = zip(*sorted_scores)

    for i in range(len(names)):
        print(f'Member: {names[i].ljust(10)}, \t Points: {total_scores[i]}')

def show_date_data():
    date_counts = {}
    with open(date_file, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            date = row[0]
            attendance_count = int(row[1]) if row[1].isdigit() else 0
            date_counts[date] = attendance_count

def get_valid_date():
    """Prompt the user for a date in MM/DD/YY format and validate it."""
    while True:
        date_str = input("Until what date should the graph be plotted? (MM/DD/YY): ")
        try:
            # Try to parse the date to ensure it's in the correct format
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            return date_obj
        except ValueError:
            print("Invalid date format. Please enter the date in MM/DD/YY format.")

def plot_date_frequency():
    date_counts = {}

    # Read date_frequency.csv
    with open('date_list.csv', mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            date_str = row[0]
            attendance_count = int(row[1]) if row[1].isdigit() else 0
            date_counts[date_str] = attendance_count

    # Get the cutoff date from the user
    cutoff_date = get_valid_date()

    # Filter the data based on the cutoff date
    filtered_dates = []
    filtered_counts = []
    for date_str, count in date_counts.items():
        date_obj = datetime.strptime(date_str, "%m/%d/%y")
        if date_obj <= cutoff_date:
            filtered_dates.append(date_str)
            filtered_counts.append(count)

    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_dates, filtered_counts, color='r')
    plt.xlabel('Date')
    plt.ylabel('Attendance Count')
    plt.title(r'\textbf{Attendance Frequency}')
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()

    # Prompt for image saving
    save_image_query('Date Frequency')
    plt.show()

def save_image_query(filename):
    response = get_yes_no_input('Do you want to save the image? (Y/N) :')
    if response == 'y':
        current_datetime = datetime.now().strftime(r"%Y-%m-%d %H-%M-%S")
        plt.savefig(f'Images\\{filename} {current_datetime}.png', format="png", dpi=300)
        print('Image saved')
    return 

def main():
    prompt = starting_menu() 
    if prompt == 'y':
        get_entry_input()
    while True:
        option_choice = get_option_input(program_options)
        handle_option_choice(option_choice)

if __name__ == '__main__':
    main()

# You should probably encrypt member list and tambay tracker
# so that what get's stored in the member list is a hashed string which can be
# decrypted, and at the tambay tracker data, it will mostly be indices and numbers
# however, you can show the actual data by accessing the application
# this is to ensure security since you are releasing this shit to public eye. 


