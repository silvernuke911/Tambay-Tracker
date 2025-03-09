from modules import filepaths
from modules import updaters
from modules import utils
from modules import validators

from datetime import datetime


def add_entry():
    has_date = False 
    has_sender = False 
    has_attendees = False 
    entry_done = False
    print(utils.sepline(65))  
    while not entry_done:
        # Step 1: Ask for Date
        while not has_date:
            print('Date (MM/DD/YY) [Press Enter for Today]')
            date = input('> ').strip().lower()
            if date in ['quit', 'qt']:
                print('Entry cancelled.\n')
                entry_done = True
                break
            if date == '':
                date = datetime.now().strftime(r'%m/%d/%y')
                print('\033[F\033[K', end='')  # Move cursor up and clear line
                print(f'> {date}')
            if validators.validate_date_format(date):
                has_date = True
            else:
                print("Invalid date format. Please enter the date in MM/DD/YY format. \n")
        if entry_done:
            break

        # Step 2: Ask for Sender
        while not has_sender:
            print('Sender Name:')
            sender = input('> ').strip()
            if sender.lower() in ['quit', 'qt']:
                print('Entry cancelled.\n')
                entry_done = True
                break
            if validators.validate_member(sender):
                print(f'Sender confirmed: {sender}')
                print(utils.sepline(65))
                has_sender = True
            else:
                print("Invalid sender name. Please enter a valid name. \n")
        if entry_done:
            break
        
        # Step 3: Ask for Attendees
        attendees = []
        print("Enter attendees one by one. Type 'done' to finish, 'quit' to cancel.")
        while not has_attendees:
            attendee = input('> ').strip()
            # Handle quit
            if attendee.lower() in ['quit', 'qt']:
                print('Entry cancelled.')
                entry_done = True
                break
            # Handle "done"
            if attendee.lower() in ['done','.',',']:
                if len(attendees) == 0:
                    print("You need to enter at least one attendee.")
                    continue
                has_attendees = True
                break
            # Handle "delete last"
            if attendee.lower() == 'delete last':
                if len(attendees) == 0:
                    print("No attendees to delete.")
                else:
                    removed = attendees.pop()
                    print(f"Removed: {removed}")
                continue
            # Validate member
            if not validators.validate_member(attendee):
                print(f"Invalid member: {attendee}. Please try again.")
                continue
            # Append the valid attendee
            attendees.append(attendee)
            print(f"Added: {attendee}")
            
        # Step 4: Save the Entry
        print(utils.sepline(65))
        print(f"Date       : {date}")
        print(f"Sender     : {sender}")
        print(f"Attendees  : {', '.join(attendees)}")
        print(utils.sepline(65))
        print(f"Entry Added Successfully")
        updaters.save_entry(date, sender, attendees)
        
        # Step 5: Query for a new entry
        print('Would you like to add a new entry? [Y/N]')
        result = utils.yes_no_query('> ')
        if result == True:
            entry_done = False
            has_date = False 
            has_sender = False 
            has_attendees = False 
        if result == False:
            entry_done = True
            
        if entry_done:
            break
        
def add_member():
    valid_credit = ['299792458', '2.718281828', '3.141592654', '1.414213562', 'Inuke', 'Silvernuke','Jieru']
    pass

def add_special_points():
    utils.temporary_output()