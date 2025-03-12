# Tambay-Tracker

A terminal application to track the tambay attendance and for point marking

The official tambay tracker of UP PSF 2425A.

# Tambay Tracker 1.0
## Operation

Can show data in graphs for visual analysis, add attendance entries, show points and raw data, and add / delete members from the system, has additional dependencies such as the presence of database csv's to store data, but otherwise, completely understandable and friendly for users.

Here is the procedure:
> In the official UPPSF GC, if someone sends a picture of them in the tambayan, the tambay auditor must record that instance on to the application.

Has the following options
1.   `Add entry` - Add a new tambay entry, asks for the date, the sender, and the members present in the tambay
2.   `Show raw data` - Shows the raw data from the csv files
3.   `Update scores` - Update the relevant scores, you must enter this before using graphs or other visual interfaces
4.   `Show Points` - Delineates the points for each member alphabetically arranged
5.   `Show Point Order` - Delineates points for each member, ordered by points, and shows a bar graph to visually assess the data
6.   `Show Date Frequency` - Shows the attendance count for each day
7.   `Show Attendance Proportion` - Shows the attendance proportion in relation to the total count of the members
8.   `Enter Special Points` - Used to enter special points to members
9.   `Enter New Member` - Used to add a new name to the member list, to be only done once inducted to JB's
10.  `Exit` - Exits the program

Functionalities to remove special points and remove names to be added later. A major code refactoring is also in order, since most of the project is a mess and quite spaghettified right now. But it works like a charm.

## Contributions

To new developers of this project, add your name to the count
1. Juan V.

# Tambay Tracker 2.0

A New Semester is Afoot!

Well, it's the same old thing except I plan on using pandas and implementing JL's requests of showing individual attendance points, so and so. Just an update of the old codebase, really. Maybe the next few updates, we're gonna do JavaScript as a website, but oh well.

Current developer is yours truly, but an assistant to me is Jam Fernandez for the data collection, which is lovely. 

Work on this on your free time, we're gonna get there.

---- 

ADD AN OPERATING SYSTEM EMULATOR WITH Commands

## Tambay Tracker Operating System Emulator

## Commands
Follows a **verb-noun** system.

### Nouns

#### `help`
- Shows all the commands in the system.
- `\command` shows help for the specific command.

#### `add`
- Add new entries:
  - `entry` - Add new entry.
  - `new member` - Add new member.
  - `special points` - Add special points.
  - `` - (empty string) Shortcut for help; shows available commands.

#### `list`
- Lists entries in plain text.
  - `raw points` - Lists the raw points.
  - `date frequency` - Lists the date frequency.
    - `--rm wknd` - Remove weekends.
    - `--start` - Set start date (default: start of semester).
    - `--end` - Set end date (default: today).
  - `attendance proportion` - Lists attendance proportion.
    - `--rm wknd` - Remove weekends.
    - `--start` - Set start date (default: start of semester).
    - `--end` - Set end date (default: today).
  - `point order` - Lists point order.
  - `individual attendance` - Lists individual attendance.
    - `--name` - Enter name.
  - `` - Shortcut for help.

#### `show`
- Displays graphs.
  - `point order` - Graphs point order.
    - `--top` - Shows top N pointers.
    - `--save` - Save image (default: yes).
    - `--unsave` - Do not save image.
  - `attendance frequency` - Graphs attendance frequency.
    - `--rm wknd` - Remove weekends (default: no).
    - `--start date` - Set start date (default: start of semester).
    - `--end date` - Set end date (default: now).
    - `--save` - Save image (default: yes).
    - `--unsave` - Do not save image.
  - `attendance proportion` - Graphs attendance proportion.
    - `--rm wknd` - Remove weekends (default: no).
    - `--start date` - Set start date (default: start of semester).
    - `--end date` - Set end date (default: now).
    - `--save` - Save image (default: yes).
    - `--unsave` - Do not save image.
  - `individual attendance` - Graphs individual attendance.
    - `--name` - Specify name.
    - `--rm wknd` - Remove weekends (default: no).
    - `--start date` - Set start date (default: start of semester).
    - `--end date` - Set end date (default: now).
    - `--save` - Save image (default: yes).
    - `--unsave` - Do not save image.

#### `update`
- Updates all necessary data.
  - `--scores` - Updates only scores.

#### `exit`
- Exits the program.
- Requires confirmation with `y` or `n`.

#### `e`
- Shortcut for `exit`.

#### `home`
- Returns to the home page header.

#### `hm`
- Shortcut for `home`.

#### `quit`
- Quits the entry and returns to home.

#### `qt`
- Shortcut for `quit`.

#### `clearscreen`
- Clears the screen.

#### `cls`
- Shortcut for `clearscreen`.

---

## Error Handling
If an invalid command is entered:
```plaintext
"{term} is not in the accepted valid commands for {noun}".
```

---

# Tasks
- [x] Implement Pandas
- [x] Make OS commands
- [x] Add functionality
- [x] Generate data
- [ ] Generate Graphs for Each Individual
- [x] Remove Weekends from Attendance Data
- [ ] Display Only Weekly Attendance
- [ ] Add More Graph Information (e.g., Days)
- [ ] Per batch graph
- [ ] Improve UI
- [ ] Add notes system


