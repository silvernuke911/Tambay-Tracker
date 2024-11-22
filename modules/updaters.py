import csv
from collections import defaultdict
from modules import validators
from modules import query

def update_scores(raw_data_file, score_file):
    # Initialize score data from score_file
    score_data = {}
    with open(score_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Read existing scores, retaining Special Points
            score_data[row['Name']] = {
                'Sender Count': 0,
                'Attendance Count': 0,
                'Special Points': int(row['Special Points']),
                'Total points': 0
            }

    # Load data from raw_data_file
    date_data = defaultdict(lambda: {'senders': set(), 'members': set()})
    with open(raw_data_file, 'r') as f:
        reader = csv.reader(f, delimiter=':')
        for row in reader:
            date, sender, members = row
            members_list = members.split(', ')
            date_data[date]['senders'].add(sender)
            date_data[date]['members'].update(members_list)

    # Update score data based on senders and members
    for date, info in date_data.items():
        for sender in info['senders']:
            if sender in score_data:
                score_data[sender]['Sender Count'] += 1
        for member in info['members']:
            if member in score_data:
                score_data[member]['Attendance Count'] += 1

    # Calculate total points as sum of sender, attendance, and special points
    for name, scores in score_data.items():
        scores['Total points'] = (
            scores['Sender Count'] +
            scores['Attendance Count'] +
            scores['Special Points']
        )

    # Save updated score data back to score_file
    with open(score_file, 'w', newline='') as f:
        fieldnames = ['Name', 'Sender Count', 'Attendance Count', 'Special Points', 'Total points']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for name, scores in score_data.items():
            writer.writerow({
                'Name': name,
                'Sender Count': scores['Sender Count'],
                'Attendance Count': scores['Attendance Count'],
                'Special Points': scores['Special Points'],
                'Total points': scores['Total points']
            })
    print("Scores updated successfully.")

def add_mem_count(date_file, valid_names):
    from datetime import datetime
    # Get today's date in the format MM/DD/YY
    today = datetime.now().strftime('%m/%d/%y')
    updated_data = []

    # Read the date_file and update today's member count
    with open(date_file, mode='r') as file:
        lines = file.readlines()
        updated_data.append(lines[0].strip())  # Add header row
        for line in lines[1:]:
            date, attendance, member_count = line.strip().split(',')
            if date == today:
                member_count = len(valid_names)  # Update member count for today
            updated_data.append(f"{date},{attendance},{member_count}")

    # Write the updated data back to the date_file
    with open(date_file, mode='w') as file:
        file.write('\n'.join(updated_data))

def update_date_freq(raw_data_file, date_file, valid_names):
    date_attendance_count = defaultdict(set)  # Using a set to ensure uniqueness
    member_counts = {}  # To store member counts from date_file

    # Initialize attendance count and member count from 'date_file'
    with open(date_file, mode='r') as date_file_:
        reader = csv.reader(date_file_)
        next(reader)  # Skip header
        for row in reader:
            if row:
                date = row[0].strip()
                attendance = int(row[1].strip())
                member_count = int(row[2].strip()) if row[2].strip().isdigit() else 0
                date_attendance_count[date] = set()  # Initialize an empty set for each date
                member_counts[date] = member_count  # Store the member count

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
        writer.writerow(["Date", "Attendance Count", "Member Count"])  # Write header
        for date, members in date_attendance_count.items():
            attendance_count = len(members)  # Count unique members per date
            member_count = member_counts.get(date, 0)  # Get stored member count
            writer.writerow([date, attendance_count, member_count])  # Write attendance and member count

    # Update today's member count using valid_names
    add_mem_count(date_file, valid_names)
    print("Date attendance frequency updated successfully.")

def update_special_points(valid_names, score_file):
    valid_credit = ['299792458', '2.718281828', '3.141592654', '1.414213562', 'Inuke', 'Silvernuke']
    # Get recipient's name and validate it
    while True:
        name = query.get_input_with_quit("Recipient name: ")
        if name is None:
            return  # Exit if user decides to quit
        while not validators.is_valid_sender(name, valid_names):
            print("Invalid member name. Please enter a valid name from the list.")
            name = query.get_input_with_quit("Recipient name: ")
            if name is None:
                return
        break
    
    # Get special points and validate it's an integer
    special_points = query.prompt_for_integer("Special points: ")

    # Get credentials
    credentials = query.get_input_with_quit('Please enter credentials to edit document: ')
    if credentials not in valid_credit:
        print("Invalid credenitals, Operation cancelled.")
        return
    
    # Load current score data
    score_data = {}
    with open(score_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            score_data[row['Name']] = row
    
    # Update the special points for the recipient
    if name in score_data:
        score_data[name]['Special Points'] = int(score_data[name].get('Special Points', 0)) + special_points
    
    # Write updated data back to the CSV
    with open(score_file, 'w', newline='') as f:
        fieldnames = ['Name', 'Sender Count', 'Attendance Count', 'Special Points', 'Total points']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in score_data.values():
            writer.writerow(row)

    print("Special scores updated successfully.")

def update_member_list(member_file, score_file):
    valid_credit = ['299792458', '2.718281828', '3.141592654', '1.414213562', 'Inuke', 'Silvernuke','Jieru']

    attempts = 0
    max_attempts = 5
    while attempts < max_attempts:
        new_name = query.get_input_with_quit('New member name: ').strip()
        if new_name:  # Check if input is not blank
            break
        print("Name cannot be blank. Please try again.")
        attempts += 1
    if not new_name:
        print("Maximum attempts reached. Exiting...")
        return
    credentials = query.get_input_with_quit('Please enter credentials to edit document: ')
    if credentials not in valid_credit:
        print("Invalid credentials, operation cancelled.")
        return
    with open(member_file, 'r') as f:
        members = [line.strip() for line in f.readlines()]
    if new_name in members:
        print("Member already exists, please pick a new name.")
        return
    members.append(new_name)
    members.sort()
    with open(member_file, 'w') as f:
        f.write('\n'.join(members) + '\n')
    with open(score_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  
        scores = list(reader) 
    scores.append([new_name, '0', '0', '0', '0'])
    scores.sort(key=lambda x: x[0])
    with open(score_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header) 
        writer.writerows(scores)
    print("Member list updated successfully.")