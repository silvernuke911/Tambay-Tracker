# Tambay-Tracker

A terminal application to track the tambay attendance and for point marking

The official tambay tracker of UP PSF 2425A.

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

## Tambay Tracker 2.0

A New Semester is Afoot!

Well, it's the same old thing except I plan on using pandas and implementing JL's requests of showing individual attendance points, so and so. Just an update of the old codebase, really. Maybe the next few updates, we're gonna do JavaScript as a website, but oh well.

Work on this on your free time, we're gonna get there.

# Tasks
- [ ] Implement Pandas
- [ ] Generate Graphs for Each Individual
- [ ] Remove Weekends from Attendance Data
- [ ] Display Only Weekly Attendance
- [ ] Add More Graph Information (e.g., Days)
- [ ] Improve UI