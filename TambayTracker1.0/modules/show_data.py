import csv
import matplotlib.pyplot as plt
from datetime import datetime
from modules import latex_font
from modules import query

latex_font.latex_font2()

def show_raw_data(raw_data_file):
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

def show_points(score_file):
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

def visualize_data(score_file):
    names = []
    total_scores = []
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if len(row) < 4:
                continue  
            name = row[0]
            total_score = row[4]
            total_scores[name] = int(total_score)
    # Plot the bar graph
    plt.bar(names, total_scores, color='r')
    plt.xlabel('Names')
    plt.ylabel('Total Score')
    plt.title('Scores Bar Graph (Original Order)')
    plt.xticks(rotation=60, ha='right')
    plt.tight_layout()
    plt.show()

def visualize_data_ordered(raw_data_file, score_file, date_file, valid_names):
    current_datetime = datetime.now().strftime(r"%m/%d/%Y %H:%M")
    scores = {}
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            if len(row) < 3:
                continue 
            name = row[0]
            total_score = row[4]
            scores[name] = int(total_score)
    # Sort scores from highest to lowest
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    names, total_scores = zip(*sorted_scores)
    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(names, total_scores, color='b', zorder = 2)
    plt.xlabel('Brod Names')
    plt.ylabel('Total Score')
    plt.title(rf'\textbf{{Tambay Scores (As of {current_datetime})}}')
    plt.xticks(rotation=60, ha='right')
    max_score = max(total_scores)
    plt.yticks(range(0, max_score, 5))
    plt.grid(axis='y', linestyle='--', zorder = 0)
    plt.tight_layout()
    query.save_image_query('Ordered Points', raw_data_file, score_file, date_file, valid_names)
    plt.show()

def show_points(score_file):
    try:
        with open(score_file, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)
            for row in reader:
                member_name = row[0].ljust(10)
                sender_points = row[1].ljust(3)
                attendance_points = row[2].ljust(3)
                special_points = row[3].ljust(3)
                total_points = row[4].ljust(3)
                print(f"Member: {member_name} Sender pts: {sender_points}, Attd pts: {attendance_points}, Special pts: {special_points},  Total points: {total_points}")
    except FileNotFoundError:
        print("The data file does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_point_order(score_file):
    scores = {}
    with open(score_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader) 
        for row in reader:
            if len(row) < 3:
                continue
            name = row[0]
            total_score = int(row[4]) if row[4].isdigit() else 0
            scores[name] = total_score
    # Sort scores from highest to lowest
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    names, total_scores = zip(*sorted_scores)

    for i in range(len(names)):
        print(f'Member: {names[i].ljust(10)}, \t Points: {total_scores[i]}')

def show_date_data(date_file, cutoff_date, mode):
    if mode == 'raw':
        date_counts = {}

        # Read date_file
        with open(date_file, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)  # Skip header
            for row in reader:
                date_str = row[0]
                attendance_count = int(row[1]) if row[1].isdigit() else 0
                date_counts[date_str] = attendance_count

        # Filter the data based on the cutoff date
        filtered_dates = []
        filtered_counts = []
        for date_str, count in date_counts.items():
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            if date_obj <= cutoff_date:
                filtered_dates.append(date_str)
                filtered_counts.append(count)
        for i in range(len(filtered_dates)):
            print(f'Date : {filtered_dates[i]}  ,  Attendance count = {filtered_counts[i]}')

    elif mode == 'proportion':
        # Store attendance proportions
        date_proportions = {}

        # Read date_file
        with open(date_file, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            next(reader)  # Skip header
            for row in reader:
                date_str = row[0]
                attendance_count = int(row[1]) if row[1].isdigit() else 0
                member_count = int(row[2]) if row[2].isdigit() and int(row[2]) > 0 else 1  # Avoid division by zero
                proportion = (attendance_count / member_count) * 100  # Calculate proportion as a percentage
                date_proportions[date_str] = proportion

        # Filter the data based on the cutoff date
        filtered_dates = []
        filtered_proportions = []
        for date_str, proportion in date_proportions.items():
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            if date_obj <= cutoff_date:
                filtered_dates.append(date_str)
                filtered_proportions.append(proportion)
        for i in range(len(filtered_dates)):
            print(f'Date : {filtered_dates[i]}  ,  Attendance proportion = {filtered_proportions[i]:.2f}%')     
    
def plot_date_frequency(raw_data_file, score_file, date_file, valid_names):
    date_counts = {}

    # Read date_frequency.csv
    with open(date_file, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            date_str = row[0]
            attendance_count = int(row[1]) if row[1].isdigit() else 0
            date_counts[date_str] = attendance_count

    # Get the cutoff date from the user
    cutoff_date = query.get_valid_date()
    show_date_data(date_file, cutoff_date, mode ='raw')

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
    plt.bar(filtered_dates, filtered_counts, color='r', zorder = 2)
    plt.xlabel('Date')
    plt.ylabel('Attendance Count')
    plt.title(r'\textbf{Attendance Frequency}')
    plt.xticks(rotation=90, ha='right', fontsize = 8)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', zorder = 0)
    max_count = max(filtered_counts)
    plt.yticks(range(0, max_count, 5))
    
    # Prompt for image saving
    query.save_image_query('Date Frequency', raw_data_file, score_file, date_file, valid_names)
    plt.show()

def show_date_frequency_proportion(raw_data_file, date_file, valid_names, score_file):
    date_proportions = {}

    # Read date_file to calculate the proportion of attendance
    with open(date_file, mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header
        for row in reader:
            date_str = row[0]
            attendance_count = int(row[1]) if row[1].isdigit() else 0
            member_count = int(row[2]) if row[2].isdigit() and int(row[2]) > 0 else 1  # Avoid division by zero
            proportion = (attendance_count / member_count) * 100  # Calculate proportion as a percentage
            date_proportions[date_str] = proportion

    # Get the cutoff date from the user
    cutoff_date = query.get_valid_date()
    show_date_data(date_file, cutoff_date, mode = 'proportion')

    # Filter the data based on the cutoff date
    filtered_dates = []
    filtered_proportions = []
    for date_str, proportion in date_proportions.items():
        date_obj = datetime.strptime(date_str, "%m/%d/%y")
        if date_obj <= cutoff_date:
            filtered_dates.append(date_str)
            filtered_proportions.append(proportion)

    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_dates, filtered_proportions, color='g', zorder = 2) 
    plt.xlabel('Date')
    plt.ylabel(r'Attendance (\%)')
    plt.title(r'\textbf{Attendance Percentage compared to Total Member Count}')
    plt.xticks(rotation=90, ha='right', fontsize = 8)
    plt.yticks(list(range(0,120,20)))
    plt.tight_layout()
    plt.ylim(0, 100)  # Set y-axis limit to 0-100% for clarity
    
    # Prompt for image saving
    query.save_image_query('Date Frequency Proportion', raw_data_file, score_file, date_file, valid_names)
    plt.grid(axis='y', linestyle='--', zorder = 0)
    plt.show()
