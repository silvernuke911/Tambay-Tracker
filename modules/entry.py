import csv
from datetime import datetime
from modules import query
from modules import validators
from modules import show_data
from modules import updaters
from modules import safe_exit

def starting_menu(raw_data_file, score_file, date_file):
    print(f'--------------------------------\n WELCOME TO THE TAMBAY TRACKER!\n--------------------------------\n')
    print(f'================================')
    print(f'UP PI SIGMA FRATERNITY TAMBAY TRACKER \n CC: Juan. V\n')
    return query.get_yes_no_input('Do you want to put a new entry? (Y/N): ', raw_data_file, score_file, date_file)

def save_entry(raw_data_file,date, sender, members_present):
    # Saving the entry to a CSV file with ':' as the delimiter
    with open(raw_data_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=':')
        writer.writerow([date, sender, members_present])
    print("Entry saved successfully.")
    return 

def get_entry_input(raw_data_file, score_file, date_file, valid_names):
    while True:
        # Validate date input
        date = query.get_input_with_quit('Date (MM/DD/YY) (Press Enter for today): ')
        if date is None:  # Check if 'QUIT' was entered
            break
        if date == '':
            date = datetime.now().strftime(r'%m/%d/%y')
  
        while not validators.validate_date_format(date):
            print("Invalid date format. Please enter the date in MM/DD/YY format.")
            date = query.get_input_with_quit('Date (MM/DD/YY) : ')
            if date == '':
                date = datetime.now().strftime(r'%m/%d/%y')
            if date is None:  # Check again for 'QUIT'
                break
        if date is None:
            break  # Exit the main loop if 'QUIT' was entered
        # Validate sender name input
        sender = query.get_input_with_quit('Sender name : ')
        if sender is None:
            break
        while not validators.is_valid_sender(sender, valid_names):
            print("Invalid sender name. Please enter a valid name from the list.")
            sender = query.get_input_with_quit('Sender name : ')
            if sender is None:
                break
        if sender is None:
            break

        # Validate members present input
        while True:
            members_present = query.get_input_with_quit('Members present (comma-separated) : ')
            if members_present is None:
                break
            members_present_list = [name.strip() for name in members_present.split(',')]  # Split and strip whitespace

            # Validate members present using the is_valid_members function
            invalid_members = validators.is_valid_members(members_present_list, valid_names)
            if not invalid_members:  # If no invalid members, break out of the loop
                break  # Exit the member validation loop
            print(f"Invalid member(s) present: {', '.join(invalid_members)}. Please enter valid names.")

        # Save entry

        save_entry(raw_data_file, date, sender, members_present)

        # Ask if the user wants to add another entry
        another_entry = query.get_yes_no_input('Do you want to add another entry? (Y/N): ', raw_data_file, score_file, date_file)
        if another_entry == 'n':
            break
    print("Entry not saved. Please debug")

def handle_option_choice(option_choice, raw_data_file, score_file, date_file, valid_names, member_file):
    """Handle the user's selection from program options."""
    if   option_choice == 1:
        get_entry_input(raw_data_file, score_file, date_file, valid_names)
    elif option_choice == 2:
        print("Showing raw data...")
        print('\n')
        show_data.show_raw_data(raw_data_file)
        print('\n')
    elif option_choice == 3:
        print("Updating scores...")
        updaters.update_scores(raw_data_file, score_file)
        updaters.update_date_freq(raw_data_file, date_file)
    elif option_choice == 4:
        print("Showing Points List...")
        show_data.show_points(score_file)
    elif option_choice == 5:
        print("Showing Point Order List and Graph...")
        show_data.show_point_order(score_file)
        show_data.visualize_data_ordered(raw_data_file, score_file, date_file)
    elif option_choice == 6:
        print("Showing Date Frequency List and Graph...")
        show_data.plot_date_frequency(raw_data_file, score_file, date_file)
    elif option_choice == 7:
        updaters.update_special_points(valid_names, score_file)
    elif option_choice == 8:
        updaters.update_member_list(member_file, score_file)
    elif option_choice == 9:
        exit_question = query.get_yes_no_input('Are you sure you want to exit? (Y/N): ', raw_data_file, score_file, date_file)
        if exit_question == 'y':
            safe_exit.safe_exit(raw_data_file, score_file, date_file)
        else:
            input('Returning to the main menu. Press enter')