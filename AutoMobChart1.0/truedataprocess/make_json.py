import json
import os

output_dir = r"C:\Users\verci\Documents\code\Tambay-Tracker\AutoMobChart1.0\truedata\individual_json_manual"
os.makedirs(output_dir, exist_ok=True)

def prompt(input_prompt, tabspace = 0):
    print(" "*4*tabspace + input_prompt)
    return input(" "*4*tabspace+"> ")

def get_schedule():
    schedules = []
    while True:
        print("-"*100)
        print(" SCHEDULE FIELD")
        print("-"*100)
        day = prompt("Enter schedule day (e.g., MWF, TTh):",2)
        time_start = prompt("Enter start time (e.g., 1:00PM):",2)
        time_end = prompt("Enter end time (e.g., 2:30PM):",2)
        type_ = prompt("Enter type (e.g., lec, lab, PE):",2)
        room = prompt("Enter room:",2)
        schedules.append({
            "day": day,
            "time start": time_start,
            "time end": time_end,
            "type": type_,
            "room": room
        })
        more = prompt("Add another schedule for this subject? [yes/no]", 2).lower()
        if more not in ["yes",'y']:
            break
    return schedules

def get_subject():
    subjects = []
    while True:
        print("-"*100)
        print(" SUBJECT FIELD ")
        print("-"*100)
        class_code = prompt("Enter class code:",tabspace=1)
        subject_name = prompt("Enter subject name:",tabspace=1)
        section = prompt("Enter section:",tabspace=1)
        units = prompt("Enter units:",tabspace=1)
        instructor = prompt("Enter instructor (or leave blank):",tabspace=1)
        schedule = get_schedule()
        subjects.append({
            "class code": class_code,
            "subject": subject_name,
            "section": section,
            "units": units,
            "instructor": instructor,
            "schedule": schedule
        })
        more = prompt("Add more subjects? [yes/no]",tabspace=1).lower()
        if more not in ["yes","y"]:
            break
    print("-"*100)
    return subjects

def main():
    print("="*100)
    print("MOBCHART MANUAL FIELD INPUT")
    print("="*100)
    student = {}
    student["name"] = prompt("Enter student name:").upper()
    student["student number (with dash)"] = prompt("Enter student number:")
    student["college (abbrev)"] = prompt("Enter college:").upper()
    student["degree major (abbrev)"] = prompt("Enter degree/major:")
    student["total units"] = prompt("Enter total units:")
    
    student["subjects"] = get_subject()
    
    filename = f"{student['name']}.json"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        json.dump(student, f, indent=4)
    print("="*100)
    print(f"Data saved to {filepath.name}")
    print("="*100)

if __name__ == "__main__":
    main()
