import csv
from collections import Counter

def update_scores():
    # Initialize two Counters to keep track of occurrences as sender and as attendee
    sender_counts = Counter()
    attendee_counts = Counter()

    # Read 'data.csv' and count occurrences of each name as sender or attendee
    with open('fabricated_data.csv', mode='r') as data_file:
        reader = csv.reader(data_file, delimiter=':')
        for row in reader:
            # Count the sender name in `row[1]`
            sender_name = row[1].strip()
            sender_counts[sender_name] += 1

            # Count the attendees in `row[2]`
            members_present = row[2].split(', ')
            attendee_counts.update(members_present)

    # Read 'scores.csv' to get the list of names and update both sender and attendee counts
    updated_scores = []
    with open('scores_list.csv', mode='r') as scores_file:
        reader = csv.reader(scores_file)
        next(reader)  # Skip the header row
        for row in reader:
            name = row[0]
            # # Get current scores if they exist
            # current_sender_count = int(row[1]) if len(row) > 1 else 0
            # current_attendee_count = int(row[2]) if len(row) > 2 else 0
            # Update counts from sender and attendee Counters
            updated_sender_count = sender_counts.get(name, 0)
            updated_attendee_count = attendee_counts.get(name, 0)
            updated_total_score = updated_sender_count + updated_attendee_count
            # Append the updated scores for each name
            updated_scores.append([name, updated_sender_count, updated_attendee_count, updated_total_score ])

    # Write the updated scores back to 'scores.csv'
    with open('scores_list.csv', mode='w', newline='') as scores_file:
        writer = csv.writer(scores_file)
        writer.writerow(["Name", "Sender Count", "Attendance Count", 'Total points'])  # Write headers
        writer.writerows(updated_scores)

    print("Scores updated successfully.")

import csv
from collections import Counter

def update_date_freq():
    # Initialize a Counter to track attendance per date with dates from 'date_list.csv'
    date_attendance_count = Counter()
    
    # Read 'date_list.csv' to get all possible dates and initialize them with 0 attendance
    with open('date_list.csv', mode='r') as date_file:
        reader = csv.reader(date_file)
        next(reader)  # Skip header
        for row in reader:
            if row:
                date = row[0].strip()
                date_attendance_count[date] = 0

    # Read 'fabricated_data.csv' and count attendees per date
    with open('fabricated_data.csv', mode='r') as data_file:
        reader = csv.reader(data_file, delimiter=':')
        for row in reader:
            if not row or len(row) < 3:
                continue  # Skip empty or incomplete rows

            date = row[0].strip()
            members_present = row[2].split(', ')
            # Update the count only if the date is in 'date_list.csv'
            if date in date_attendance_count:
                date_attendance_count[date] += len(members_present)

    # Write the updated attendance frequency per date back to 'date_list.csv'
    with open('date_list.csv', mode='w', newline='') as date_file:
        writer = csv.writer(date_file)
        writer.writerow(["Date", "Attendance Count"])  # Write header
        for date, count in date_attendance_count.items():
            writer.writerow([date, count])

    print("Date attendance frequency updated successfully.")

# Run the function
update_date_freq()
update_scores()
