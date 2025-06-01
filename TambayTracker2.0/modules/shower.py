from modules import filepaths
from modules import utils
from modules import sciplots

from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates 
import pandas as pd
import os

sciplots.science_plot(fontsize=12)

def show_point_order(flags):
    print(utils.sepline(80))
    print('Loading image ... ')
    # Load the data
    data = filepaths.load_score_data()
    
    # Sort the data by 'Total Points' in descending order
    data_sorted = data.sort_values(by='Total Points', ascending=False)
    
    # Handle the 'top' flag
    if 'top' in flags:
        top_n = int(flags['top'])
        data_sorted = data_sorted.head(top_n)  # Filter top N scorers
    
    # Extract names and scores
    names = data_sorted['Name']
    scores = data_sorted['Total Points']
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(
        names,
        scores,
        edgecolor='k',
        width=1
    )
    
    # Customize the plot
    current_datetime = datetime.now().strftime(r"%m/%d/%Y %H:%M")
    plt.xlabel('Brod Names')
    plt.ylabel('Total Score')
    plt.title(rf'\textbf{{Tambay Scores (As of {current_datetime})}}')
    plt.xticks(rotation=90, ha='center')
    plt.grid(axis='x', visible=False)
    max_score = int(max(scores))
    step  = 5
    plt.yticks(range(0, max_score + step, step))
    plt.tight_layout()
    
    # Handle the 'save' and 'unsave' flags..
    save_path = filepaths.imsave_path
    if flags.get('unsave', False):  # Do not save if 'unsave' is True
        pass
    else:  # Save by default or if 'save' is True
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Create the directory if it doesn't exist
        current_datetime = datetime.now().strftime(r"%y%m%d-%H%M%S")
        filename = os.path.join(save_path, f'TambayScores_{current_datetime}.png')
        plt.savefig(
            filename,
            format = 'png', 
            dpi=300, 
        )
        print(f"Plot saved to {filename}")
    plt.show()
    print(utils.sepline(80))

def show_attendance_frequency(flags):
    print(utils.sepline(80))
    print('Loading image ... ')
    # Load the datas
    data = filepaths.load_date_data()
    
    # Convert the 'Date' column to datetime format
    data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%y')
    
    # Handle start date and end date flags
    try:
        start_date = pd.to_datetime(
            flags.get(
                'startdate', 
                '01/20/25'
            ), 
            format='%m/%d/%y'
        )
        end_date = pd.to_datetime(
            flags.get(
                'enddate', 
                datetime.today().strftime('%m/%d/%y')
            ), 
            format='%m/%d/%y'
        )
    except ValueError:
        print("Error: Date format is wrong, please use MM/DD/YY")
        return
    
    # Filter the data to include only rows between start_date and end_date
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    
    # Handle the 'rmwknd' flag (remove weekends)
    if flags.get('rmwknd', False):
        filtered_data = filtered_data[~filtered_data['Day'].isin(['Saturday', 'Sunday'])]
    
    dates  = filtered_data['Date']
    counts = filtered_data['Attendance Count']

    # Plot the bar graph
    plt.figure(figsize=(12, 6))
    plt.bar(
        dates  ,
        counts ,
        color='r',
        edgecolor='k',
        width=1
    )
    
    # Customize the plot
    plt.title(r'\textbf{Attendance Count}')
    plt.xlabel('Date')
    plt.ylabel('Attendance Count')
    # Format x-axis ticks to MM-DD-YY
    ax = plt.gca()  # Get the current axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))  # Set date format
    plt.xticks(rotation=80)  # Rotate x-axis labels for better readability
    step = 5
    max_count = int(max(counts))
    plt.yticks(range(0, max_count + step, step))
    plt.tight_layout()
    
    # Handle the 'save' and 'unsave' flags..
    save_path = filepaths.imsave_path
    if flags.get('unsave', False):  # Do not save if 'unsave' is True
        pass
    else:  # Save by default or if 'save' is True
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Create the directory if it doesn't exist
        current_datetime = datetime.now().strftime(r"%y%m%d-%H%M%S")
        filename = os.path.join(save_path, f'DateFrequency_{current_datetime}.png')
        plt.savefig(
            filename,
            format = 'png', 
            dpi=300, 
        )
        print(f"Plot saved to {filename}")
    # Show the plot
    plt.show()
    print(utils.sepline(80))
    
    # TODO: Implement 'wkave' flag for average week attendance
    # if flags.get('wkave', False):
    #     # Calculate and plot weekly average attendance
    #     pass

def show_raw_attendance(flags):
    print(utils.sepline(80))
    print('Loading image ... ')
    # Load the data
    data = filepaths.load_score_data()
    
    # Sort the data by 'Total Points' in descending order
    data_sorted = data.sort_values(by='Attendance Count', ascending=False)
    
    # Handle the 'top' flag
    if 'top' in flags:
        top_n = int(flags['top'])
        data_sorted = data_sorted.head(top_n)  # Filter top N scorers
    
    # Extract names and scores
    names = data_sorted['Name']
    scores = data_sorted['Attendance Count']
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.bar(
        names,
        scores,
        edgecolor='k',
        color = 'g',
        width=1
    )
    
    # Customize the plot
    current_datetime = datetime.now().strftime(r"%m/%d/%Y %H:%M")
    plt.xlabel('Brod Names')
    plt.ylabel('Attendance')
    plt.title(rf'\textbf{{Tambay Attendance (As of {current_datetime})}}')
    plt.xticks(rotation=90, ha='center')
    plt.grid(axis='x', visible=False)
    max_score = int(max(scores))
    step  = 5
    plt.yticks(range(0, max_score + step, step))
    plt.tight_layout()
    
    # Handle the 'save' and 'unsave' flags..
    save_path = filepaths.imsave_path
    if flags.get('unsave', False):  # Do not save if 'unsave' is True
        pass
    else:  # Save by default or if 'save' is True
        if not os.path.exists(save_path):
            os.makedirs(save_path)  # Create the directory if it doesn't exist
        current_datetime = datetime.now().strftime(r"%y%m%d-%H%M%S")
        filename = os.path.join(save_path, f'TambayAttendance_{current_datetime}.png')
        plt.savefig(
            filename,
            format = 'png', 
            dpi=300, 
        )
        print(f"Plot saved to {filename}")
    plt.show()
    print(utils.sepline(80))

def show_attendance_proportion(flags):
    utils.temporary_output()

def show_individual_attendance(flags):
    utils.temporary_output()