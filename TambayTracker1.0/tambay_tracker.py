from modules import validators
from modules import entry
from modules import query

## Something something, comment here on the purpose of this shit and shit like that, something something.

<<<<<<< HEAD
# Data files
raw_data_file = r'TambayTracker1.0\Data\tambay_tracker_data.csv'
date_file     = r'TambayTracker1.0\Data\date_list.csv'
score_file    = r'TambayTracker1.0\Data\scores_list.csv'
member_file   = r'TambayTracker1.0\Data\member_list.csv'
=======
# Data files path
raw_data_file = r'Data\tambay_tracker_data.csv'
date_file     = r'Data\date_list.csv'
score_file    = r'Data\scores_list.csv'
member_file   = r'Data\member_list.csv'
>>>>>>> ff2dc8ade2718d57f3bc69d10edfcedf300293ca

# Valid entries / options
valid_names = validators.load_valid_names(member_file)
program_options = [
    'Enter new entry',
    'Show raw data', 
    'Update scores', 
    'Show Points', 
    'Show Point Order', 
    'Show Date Frequency', 
    'Show Attendance Proportion', 
    'Enter Special Points', 
    'Enter New Member',
    'Exit'
]

def main():
    prompt = entry.starting_menu(
        raw_data_file, 
        score_file, 
        date_file, 
        valid_names
    ) 
    if prompt in ['y','']:
        entry.get_entry_input(
            raw_data_file, 
            score_file, 
            date_file, 
            valid_names
        )
    while True:
        option_choice = query.get_option_input(
            program_options, 
            raw_data_file, 
            score_file, 
            date_file, 
            valid_names
        )
        entry.handle_option_choice(
            option_choice, 
            raw_data_file, 
            score_file, 
            date_file, 
            valid_names, 
            member_file
        )

# Run main program 
if __name__ == '__main__':
    main()