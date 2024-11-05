import numpy as np
import csv
import os
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

def visualize_data():
    scores = {}

    # Read scores.csv
    with open('scores_list.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 3:
                continue  # Skip rows with insufficient data

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
    plt.bar(names, total_scores, color='skyblue')
    plt.xlabel('Names')
    plt.ylabel('Total Score')
    plt.title('Scores Bar Graph (Sorted from Highest to Lowest)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()

def show_points():
    try:
        with open(r'scores_list.csv', mode='r') as file:
            reader = csv.reader(file, delimiter=',')
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

    # Read scores.csv
    with open('scores_list.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            if len(row) < 3:
                continue  # Skip rows with insufficient data

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

def plot_date_frequency():
    date_counts = {}

    # Read date_frequency.csv
    with open('date_list.csv', mode='r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            date = row[0]
            attendance_count = int(row[1]) if row[1].isdigit() else 0
            date_counts[date] = attendance_count

    # Prepare data for plotting, sorted by date
    dates = list(date_counts.keys())
    attendance_counts = list(date_counts.values())

    # Plot the bar graph
    plt.figure(figsize=(10, 6))
    plt.bar(dates, attendance_counts, color='lightgreen')
    plt.xlabel('Date')
    plt.ylabel('Attendance Count')
    plt.title('Attendance Frequency per Date')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.show()

# visualize_data()
# show_points()
# show_point_order()

plot_date_frequency()