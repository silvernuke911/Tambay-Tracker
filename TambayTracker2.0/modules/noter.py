from modules import filepaths
from modules import utils

import numpy as np
import pandas as pd
import textwrap
from datetime import datetime

def note_add(flags):
    notefile = filepaths.notefile_path
    has_note = False
    has_author = False
    print(utils.sepline(65))
    print('Write note. Press enter to save note')
    print(utils.sepline(65))
    while not has_note:
        note = input("> ")
        if note == '':
            print('Blank note. Please enter a note')
            continue
        if note.lower() in ['quit', 'qt']:
            print('Operation cancelled')
            return
        has_note = True
    print(utils.sepline(65))
    print("Please write author name. Press [Enter] when done")
    while not has_author:
        author = input("> ")
        if author.lower() in ['quit', 'qt']:
            print('Operation cancelled')
            return
        if author == '':
            utils.clearline()
            print('> Anon')
            author = 'Anon'
        has_author = True
    date = np.nan if flags.get("nodate", False) else datetime.now().strftime("%m/%d/%y")
    time = np.nan if flags.get("nodate", False) else datetime.now().strftime("%I:%M:%S %p")
    new_entry = pd.DataFrame([[date, time, author, note]], columns=["Date","Time", "Author", "Note"])
    try:
        df = pd.read_csv(notefile)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date","Time", "Author", "Note"])
    print(utils.sepline(65))
    print('Confirm note [Y/N]')
    print(utils.sepline(65))
    print(f'Date   : {new_entry["Date"].iloc[0]}')
    print(f'Time   : {new_entry["Time"].iloc[0]}')
    print(f'Author : {new_entry["Author"].iloc[0]}')
    print(f'Note   : {new_entry["Note"].iloc[0]}')
    print(utils.sepline(65))
    prompt = utils.yes_no_query('> ')
    print(utils.sepline(65))
    if prompt:
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(notefile, index=False)
        print("Note added successfully.")
    else:
        print("Note cancelled.")
    print(utils.sepline(65))
    return


def note_read(flags):
    notefile = filepaths.notefile_path
    notes = pd.read_csv(notefile, dtype=str).fillna("")
    if flags.get("today", False):
        target_date = datetime.now().strftime("%m/%d/%y")
    elif "date" in flags:
        target_date = flags["date"]
    else:
        target_date = None  # Read all if no specific date

    # Filter by date if needed
    if target_date:
        notes = notes[notes["Date"] == target_date]

    # Check if there are no matching entries
    if notes.empty and target_date:
        print(f"No entries for date {target_date}")
        return

    # Reset index for clean output
    notes = notes.reset_index(drop=True)

    # Print formatted header
    print(utils.sepline(85))
    print(
        f"{'Date':^10} "
        f"{'Time':^15} "
        f"{'Author':<15} " 
        f"{'Note':<50}"
    )
    print(utils.sepline(85))

    # Print each row with wrapped text
    for _, row in notes.iterrows():
        wrapped_note = textwrap.fill(row["Note"], width=40)
        note_lines = wrapped_note.split("\n")

        # Print first line with full row data
        print(
            f"{row['Date']:^10} "
            f"{row['Time']:^15} "
            f"{row['Author']:<15} " 
            f"{note_lines[0]:<50}"
        )

        # Print remaining wrapped lines, aligning them under the Note column
        for line in note_lines[1:]:
            print(
                f"{'':<10} "
                f"{'':<15} "
                f"{'':<15} "
                f"{line:<50}"
            )

    print(utils.sepline(85))