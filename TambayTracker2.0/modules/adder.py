from modules import filepaths
from modules import updaters
from modules import utils
from modules import validators

import pandas as pd
from datetime import datetime

def add_entry():
    has_date = False 
    has_sender = False 
    has_attendees = False 
    entry_done = False
    has_quit = False
    print(utils.sepline(65))  
    while not entry_done:
        # Step 1: Ask for Date
        while not has_date:
            print('Date (MM/DD/YY) [Press Enter for Today]')
            date = utils.prompt(address=False, lower = False)
            if date in ['quit', 'qt', '..']:
                print('Entry cancelled.')
                entry_done = True
                has_quit = True
                break
            if date == '':
                date = datetime.now().strftime(r'%m/%d/%y')
                utils.clearline()
                print(f'> {date}')
            if validators.validate_date_format(date):
                has_date = True
            else:
                print("Invalid date format. Please enter the date in MM/DD/YY format. ")
        if entry_done:
            break

        # Step 2: Ask for Sender
        while not has_sender:
            print(utils.sepline(65))
            print('Sender Name:')
            sender = utils.prompt(address=False, lower = False)
            if sender.lower() in ['quit', 'qt', '..']:
                print('Entry cancelled.')
                entry_done = True
                has_quit = True
                break
            if validators.validate_member(sender):
                print(f'Sender confirmed: {sender}')
                print(utils.sepline(65))
                has_sender = True
            else:
                print("Invalid sender name. Please enter a valid name.")
        if entry_done:
            break
        
        # Step 3: Ask for Attendees
        attendees = []
        print("Enter attendees one by one. Type 'done' to finish, 'quit' to cancel.")
        while not has_attendees:
            attendee = utils.prompt(address=False, lower = False)
            # Handle quit
            if attendee.lower() in ['quit', 'qt', '..']:
                print('Entry cancelled.')
                entry_done = True
                has_quit = True
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
        
        if not has_quit:
            # Step 4: Save the Entry
            print(utils.sepline(65))
            print(f"Date       : {date}")
            print(f"Sender     : {sender}")
            print(f"Attendees  : {', '.join(attendees)}")
            print(utils.sepline(65))
            print(f"Entry Added Successfully")
            print(utils.sepline(65))
            updaters.save_entry(date, sender, attendees)
        
        # Step 5: Query for a new entry
        print('Would you like to add a new entry? [Y/N]')
        result = utils.yes_no_query('> ')
        if result == True:
            entry_done      = False
            has_date        = False 
            has_sender      = False 
            has_attendees   = False 
        if result == False:
            entry_done      = True
            
        if entry_done:
            updaters.update_all(silent=True)
            break
    print(utils.sepline(65))
    return
        
        
        
def add_member():
    print(utils.sepline(65))
    # Prompt for credential password
    valid_credentials = ['299792458', '2.718281828', '3.141592654', 
                         '1.414213562', 'Inuke', 'Silvernuke', 'Jieru']
    print("Enter your credential password (Type 'quit' to cancel):")
    password = utils.prompt(address=False, lower = False)
    if password.lower() in ['quit', 'qt', '..']:
        print("Operation cancelled.")
        return
    if password not in valid_credentials:
        print("Invalid credential password. Aborting.")
        return
    else:
        print('Valid password, proceed with adding new member')
    print(utils.sepline(65))
    # Prompt for new member name
    print("Enter the new member's name (Type 'quit' to cancel):")
    name = utils.prompt(address=False, lower = False)
    if name.lower() in ['quit', 'qt', ".."]:
        print("Operation cancelled.")
        return
    # Validate if the member already exists
    member_file = pd.read_csv(filepaths.member_filepath)
    if name in member_file['Name'].tolist():
        print(f"Member '{name}' already exists. Aborting.")
        return
    # Prompt for Batch, College, and Course (all optional)
    print("Enter the batch (Press Enter to leave blank, or 'quit' to cancel):")
    batch = utils.prompt(address=False, lower = False)
    if batch.lower() in ['quit', 'qt',".."]:
        print("Operation cancelled.")
        return
    print("Enter the college (Press Enter to leave blank, or 'quit' to cancel):")
    college = utils.prompt(address=False, lower = False)
    if college.lower() in ['quit', 'qt']:
        print("Operation cancelled.")
        return
    print("Enter the course (Press Enter to leave blank, or 'quit' to cancel):")
    course = utils.prompt(address=False, lower = False)
    if course.lower() in ['quit', 'qt']:
        print("Operation cancelled.")
        return
    # Add the new member to the member file
    new_member = pd.DataFrame({
        'Name': [name],
        'Batch': [batch],
        'College': [college],
        'Course': [course]
    })
    member_file = pd.concat([member_file, new_member], ignore_index=True)
    member_file.to_csv(filepaths.member_filepath, index=False)
    member_file['Batch'] = member_file['Batch'].astype(int)
    print(f"Member '{name}' successfully added.")
    # Add the new member to the score file with zero scores
    try:
        score_file = pd.read_csv(filepaths.score_filepath)
    except FileNotFoundError:
        print("Score file not found. Creating a new one...")
        score_file = pd.DataFrame(columns=[
            'Name', 'Sender Count', 'Attendance Count', 'Special Points', 'Total Points'
        ])
    # Check if the member already has an entry (shouldn't happen but just in case)
    if name in score_file['Name'].tolist():
        print(f"Score entry for '{name}' already exists. Skipping score entry.")
        return
    new_score = pd.DataFrame({
        'Name': [name],
        'Sender Count': [0],
        'Attendance Count': [0],
        'Special Points': [0],
        'Total Points': [0]
    })
    score_file = pd.concat([score_file, new_score], ignore_index=True)
    score_file.to_csv(filepaths.score_filepath, index=False)
    print(f"Score entry for '{name}' successfully added.")
    print(utils.sepline(65))


def add_special_points():
    # Load the score file
    score_file = pd.read_csv(filepaths.score_filepath)

    # Step 1: Ask for the name
    while True:
        print('Enter the name to award special points (or type "quit" to cancel):')
        name = utils.prompt(address=False, lower = False)
        if name.lower() in ['quit', 'qt']:
            print('Operation cancelled.')
            return
        
        # Use your validate_member() function
        if not validators.validate_member(name):
            print(f'Invalid name: {name}. Please try again.')
            continue
        break

    # Step 2: Ask for the number of points
    while True:
        print(f'How many special points to add to {name}?')
        try:
            points = int(utils.prompt(address=False, lower = False))
            if points in ['quit', 'qt']:
                print('Operation cancelled.')
                return
            # if points < 0:
            #     print('Points cannot be negative. Try again.')
            #     continue
            break
        except ValueError:
            print('Invalid input. Please enter a valid integer.')

    # Step 3: Update the score file
    if name in score_file['Name'].values:
        # Add the points to the existing Special Points
        score_file.loc[score_file['Name'] == name, 'Special Points'] += points
        
        # Save the file
        score_file.to_csv(filepaths.score_filepath, index=False)
        print(f'Special points updated. {name} now has {score_file.loc[score_file["Name"] == name, "Special Points"].values[0]} points.')
    else:
        print(f'Could not find {name} in the score file.')
    print(utils.sepline(65))
