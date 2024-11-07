import csv
from modules import validators
from modules import entry
from modules import query

# Data files
raw_data_file = r'Data\tambay_tracker_data.csv'
date_file = r'Data\date_list.csv'
score_file = r'Data\scores_list.csv'
member_file = r'Data\member_list.csv'

# Valid entries / options
valid_names = validators.load_valid_names(member_file)
program_options = ['Enter new entry','Show raw data', 'Update scores', 'Show Points', 'Show Point Order', 'Show Date Frequency', 'Enter special points','Exit']

def main():
    prompt = entry.starting_menu(raw_data_file, score_file, date_file) 
    if prompt == 'y':
        entry.get_entry_input(raw_data_file, score_file, date_file, valid_names)
    while True:
        option_choice = query.get_option_input(program_options, raw_data_file, score_file, date_file)
        entry.handle_option_choice(option_choice, raw_data_file, score_file, date_file, valid_names)

if __name__ == '__main__':
    main()