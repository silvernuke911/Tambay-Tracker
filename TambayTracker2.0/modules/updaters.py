from modules import filepaths
from modules import utils
import pandas as pd
import os 
import csv 

def update_date_frequency(silent = False):
    # Attempt to load the date file or create it if it doesn't exist
    try:
        date_file = pd.read_csv(filepaths.date_filepath)
    except FileNotFoundError:
        print(f"{filepaths.date_filepath} not found. Creating new file...")
        start_date = pd.to_datetime('01/20/25', format='%m/%d/%y')
        end_date = pd.to_datetime('09/20/25', format='%m/%d/%y')
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        date_file = pd.DataFrame({
            'Date': date_range.strftime('%m/%d/%y'),  # Fix the date format here
            'Day': date_range.strftime('%A'),        # Add day of the week
            'Attendance Count': [0] * len(date_range),
            'Member Count': [0] * len(date_range)
        })
        date_file.to_csv(filepaths.date_filepath, index=False)
        print(f'✅ New date file created with zeros: {filepaths.date_filepath}')

    # Load raw data
    raw_data_file = pd.read_csv(filepaths.raw_data_filepath)

    # Ensure Date column is in datetime format
    date_file['Date'] = pd.to_datetime(date_file['Date'], format='%m/%d/%y')
    raw_data_file['Date'] = pd.to_datetime(raw_data_file['Date'], format='%m/%d/%y')

    # Create a dictionary to count unique attendees per day
    daily_attendance = {}
    for idx, row in raw_data_file.iterrows():
        date = row['Date']
        attendees = set(name.strip() for name in str(row['Attendees']).split(','))  # Unique attendees per row
        if date not in daily_attendance:
            daily_attendance[date] = set()
        daily_attendance[date].update(attendees)

    # Update the Attendance Count in date_file
    for idx, row in date_file.iterrows():
        date = row['Date']
        if date in daily_attendance:
            date_file.at[idx, 'Attendance Count'] = len(daily_attendance[date])
        else:
            date_file.at[idx, 'Attendance Count'] = 0  # Leave zero if no attendees

    # Convert the Date back to MM/DD/YY before saving
    date_file['Date'] = date_file['Date'].dt.strftime('%m/%d/%y')
    date_file['Day'] = date_file['Date'].apply(lambda x: pd.to_datetime(x, format='%m/%d/%y').strftime('%A'))

    # Save the updated file
    date_file.to_csv(filepaths.date_filepath, index=False)
    if not silent:
        print(f'Date frequency successfully updated')



def update_scores(silent = False):
    # Load the raw data and member list
    raw_data_file = pd.read_csv(filepaths.raw_data_filepath)
    member_file = pd.read_csv(filepaths.member_filepath)
    
    # Load the existing scores to preserve Special Points
    try:
        score_file = pd.read_csv(filepaths.score_filepath)
    except FileNotFoundError:
        # If the file doesn't exist, initialize Special Points to 0
        score_file = pd.DataFrame({
            'Name': member_file['Name'],
            'Special Points': [0] * len(member_file)
        })
    
    # Split attendees (comma-separated) into lists
    raw_data_file['Attendees'] = raw_data_file['Attendees'].apply(lambda x: [name.strip() for name in str(x).split(',')])
    
    # Create dictionaries to store daily counts
    sender_daily_count = {}
    attendance_daily_count = {}

    # Initialize counts for each member
    for name in member_file['Name']:
        sender_daily_count[name] = set()  # Using a set to avoid duplicates per day
        attendance_daily_count[name] = set()

    # Count the number of UNIQUE days each person was a sender
    for idx, row in raw_data_file.iterrows():
        sender = row['Sender']
        date = row['Date']
        if sender in sender_daily_count:
            sender_daily_count[sender].add(date)

    # Count the number of UNIQUE days each person was an attendee
    for idx, row in raw_data_file.iterrows():
        attendees = row['Attendees']
        date = row['Date']
        for attendee in attendees:
            if attendee in attendance_daily_count:
                attendance_daily_count[attendee].add(date)

    # Merge old Special Points into the new DataFrame
    score_data = pd.DataFrame({
        'Name': member_file['Name'],
        'Sender Count': [len(sender_daily_count[name]) for name in member_file['Name']],
        'Attendance Count': [len(attendance_daily_count[name]) for name in member_file['Name']],
    })

    # Merge the old Special Points back in
    score_data = pd.merge(score_data, score_file[['Name', 'Special Points']], on='Name', how='left')
    score_data['Special Points'] = score_data['Special Points'].astype(int)
    # Fill missing special points with 0 (for new members)
    score_data = score_data.assign(**{'Special Points': score_data['Special Points'].fillna(0)})

    # ✅ NEW: Calculate Total Points
    score_data['Total Points'] = (
        score_data['Sender Count'] + 
        score_data['Attendance Count'] + 
        score_data['Special Points']
    ).astype(int)
    # Overwrite the score file
    score_data.to_csv(filepaths.score_filepath, index=False)
    if not silent:
        print('Scores successfully updated.')


    
def save_entry(date, sender, attendees):
    # Define the CSV file name
    csv_file = filepaths.raw_data_filepath
    # Check if file exists to add header only once
    file_exists = os.path.isfile(csv_file)
    # Open the file in append mode
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write the header if file is new
        if not file_exists:
            writer.writerow(['Date', 'Sender', 'Attendees'])
        # Write the entry
        writer.writerow([
            date,
            sender,
            ', '.join(attendees)
        ])
    return

def update_all(silent = False):
    update_date_frequency(silent=silent)
    update_scores(silent=silent)