import pdfplumber
import re
import os
from pathlib import Path
import json
import shutil
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)
# ===============================
# PDF reading helpers
# ===============================

def read_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ''
    return text

def textblock_form5a(text):
    match = re.search(
        r"STUDENT NUMBER[\s\S]+?Total units enlisted\s+[\d.]+",
        text, re.IGNORECASE
    )
    return match.group(0).strip() if match else None
    
def textblock_form5(text):
    match = re.search(
        r"COLLEGE DEGREE[\s\S]+?\*+nothing follows\*+",
        text, re.IGNORECASE
    )
    return match.group(0).strip() if match else None

def determine_form_type(text):
    if "U.P. FORM 5A" in text:
        return "FORM5A"
    elif "UP FORM 5." in text:
        return "FORM5"
    else:
        return "Unknown form type"
    
def textblock_up_form(text, form_type):
    if form_type == 'FORM5A':
        return textblock_form5a(text)
    elif form_type == 'FORM5':
        return textblock_form5(text)
    else:
        raise ValueError("Unknown form type")

# ===============================
# Sched parsing helpers
# ===============================

def has_am_pm(t):
    return t.endswith("AM") or t.endswith("PM")

def add_colon_zero(t):
    if has_am_pm(t) and ":" not in t:
        return t[:-2] + ":00" + t[-2:]
    elif not has_am_pm(t) and ":" not in t:
        return t + ":00"
    return t

def process_schedlines(schedlines):
    sched_dicts = []
    for sched in schedlines:     
        sched_field = sched.split(" ")
        if len(sched_field) < 2:
            continue
        day = sched_field[0]
        time = sched_field[1]
        times = time.split("-")
        if len(times) != 2:
            continue
        time_start = times[0].upper()
        time_end = times[1].upper()
        if not has_am_pm(time_start) and has_am_pm(time_end):
            time_start += time_end[-2:]
        time_start = add_colon_zero(time_start)
        time_end = add_colon_zero(time_end)
        class_type = sched_field[2] if len(sched_field) > 2 else ""
        if sched_field[-1] == "TBA":
            room_no = sched_field[-1]
        elif sched_field[-1]=="Rm.":
            room_no = " ".join(sched_field[-3:])
        else:
            room_no = " ".join(sched_field[-2:])
        sched_dicts.append({
            "day": day,
            "time start" : time_start,
            "time end" : time_end,
            "type": class_type,
            "room": room_no
        })
    return sched_dicts

# ===============================
# Parsing logic
# ===============================

def safe_unit_parse(units):
    """
    Convert unit string to float if possible.
    Skip if wrapped in parentheses.
    """
    if not units:
        return 0.0
    u = units.strip()
    if u.startswith("(") and u.endswith(")"):  # skip units in parentheses
        return 0.0
    try:
        return float(u)
    except ValueError:
        return 0.0
    
def parse_form5_block(textblock):
    lines = textblock.split('\n')
    course_line = lines[2]
    courseline_words = course_line.split(" ")
    college = courseline_words[0]
    degree_major = " ".join(courseline_words[1:3])
    nameline = lines[1]
    nameline_words = nameline.split()
    student_number = nameline_words[2]
    if "NAME" in nameline_words:
        name_index = nameline_words.index("NAME")
        name_list = nameline_words[name_index+1:]
    if "BS" in nameline_words:
        BS_index = nameline_words.index("BS")
        name_list = nameline_words[name_index+1:BS_index]
        degree_major = " ".join(nameline_words[BS_index:])
    name = " ".join(name_list)
    subject_words = lines[4:-1]
    out_list = ["Admission", "Entrance", 
                "Registration/Residence", 
                "Library", "Laboratory", 
                "Computer", "Athletic", 
                "Cultural", "Medical",
                "Dental","Guidance", 
                "Handbook", "School", 
                "Development", "EDF", 
                "200.00", "400.00"]
    subject_entries = []
    for line in subject_words:
        subject_line = line.split(" ")
        if len(subject_line)<2:
            continue
        for outword in out_list:
            if outword in subject_line:
                out_index = subject_line.index(outword)
                subject_line = subject_line[:out_index]
        class_code = subject_line[0]
        second_word = subject_line[1]
        subject = ""
        section = ""
        units = ""
        instructor = ""
        if second_word == "PE":
            if subject_line[2] == "1":
                subject = " ".join(subject_line[1:3])  # PE 1
                section = subject_line[3]
                units = subject_line[4]
                offset = 5
            else:
                subject = " ".join(subject_line[1:4])  # PE 2 XYZ
                section = subject_line[4]
                units = subject_line[5]
                offset = 6
        elif second_word == "App":
            subject = " ".join(subject_line[1:4])  
            section = subject_line[4]
            units = subject_line[5]
            offset = 6
        elif second_word == "FA":
            subject = " ".join(subject_line[1:3])  
            section = "".join(subject_line[3:6])
            units = subject_line[6]
            offset = 7
        elif second_word == "ROTC":
            subject = " ".join(subject_line[1:5])  
            section = "".join(subject_line[5:6])
            units = subject_line[6]
            offset = 7
        else:
            subject = " ".join(subject_line[1:3])  
            section = subject_line[3]
            units = subject_line[4]
            offset = 5
        schedule_words = subject_line[offset:]
        schedule = " ".join(schedule_words)
        schedlines = [s.strip() for s in schedule.split(";")]
        sched_dicts = process_schedlines(schedlines)
        subject_entries.append({
            "class code": class_code,
            "subject": subject,
            "section": section,
            "units": units,
            "instructor": instructor,
            "schedule": sched_dicts
        })
    total_units = sum(safe_unit_parse(s["units"]) for s in subject_entries)
    student_dict = {
        "name": name,
        "student number": student_number,
        "college": college,
        "degree major": degree_major,
        "total units": f"{total_units:.1f}",
        "subjects": subject_entries
    }
    return student_dict

def parse_form5a_block(textblock):
    lines = textblock.split('\n')
    nameline = lines[1]
    nameline_words = nameline.split(" ")
    student_number = nameline_words[0]

    if nameline_words[-2] == "Law":
        college = nameline_words[-2]
        degree_major = nameline_words[-1]
        name = " ".join(nameline_words[1:-2])
    else:
        degree_major = " ".join(nameline_words[-2:])
        college = nameline_words[-3]
        name = " ".join(nameline_words[1:-3])
    subject_words = lines[4:-1]
    subject_entries = []
    for line in subject_words:
        subject_line = line.split(" ")
        if "Cancel" in subject_line:
            cancel_index = subject_line.index("Cancel")
            subject_line = subject_line[:cancel_index]
        class_code = subject_line[0]
        second_word = subject_line[1]
        subject = ""
        section = ""
        if second_word == "PE":
            if subject_line[2] == "1":
                subject = " ".join(subject_line[1:3])  
                section = subject_line[3]
                units = subject
                offset = 4
            else:
                subject = " ".join(subject_line[1:4])  
                section = subject_line[4]
                offset = 5
        elif second_word == "FA":
            subject = " ".join(subject_line[1:3])  
            section = "".join(subject_line[3:6])
            offset = 6
        elif second_word == "ROTC":
            subject = " ".join(subject_line[1:5])  
            section = "".join(subject_line[5:6])
            offset = 6
        else:
            subject = " ".join(subject_line[1:3])  
            section = subject_line[3]
            offset = 4
        units = subject_line[-1]
        schedule_line = subject_line[offset:-1]
        instructor_index = -2
        if schedule_line[-1] in ["TBA",'CONCEALED']:
            instructor_index = -1
        if schedule_line[-3] in ["DELA"]:
            instructor_index = -3 
        if schedule_line[-4] in ["CHUA,"]:
            instructor_index = -4
        instructor = " ".join(schedule_line[instructor_index:])
        schedule_line = schedule_line[:instructor_index]
        schedule = " ".join(schedule_line)
        schedlines = [s.strip() for s in schedule.split(";")]
        sched_dicts = process_schedlines(schedlines)
        subject_entries.append({
            "class code": class_code,
            "subject": subject,
            "section": section,
            "units": units,
            "instructor": instructor,
            "schedule": sched_dicts
        })
    total_units = sum(safe_unit_parse(s["units"]) for s in subject_entries)
    student_dict = {
        "name": name,
        "student number": student_number,
        "college": college,
        "degree major": degree_major,
        "total units": f"{total_units:.1f}",
        "subjects": subject_entries
    }
    return student_dict

def parse_text_block(textblock, form_type):
    if form_type == "FORM5":
        return parse_form5_block(textblock)
    elif form_type == "FORM5A":
        return parse_form5a_block(textblock)
    else:
        return None

# ===============================
# Main JSON save/load
# ===============================

def process_all_pdfs(base_dir):
    form5_dir = base_dir / "truedata" / "form5files"
    individual_dir = base_dir / "truedata" / "individual_json"
    all_dir = base_dir / "truedata" / "alldata_json"
    print("="*100)
    print("Processing PDF Files")
    print("="*100)
    # recreate/overwrite output dirs
    for d in [individual_dir, all_dir]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)
    error_list = []
    for file in form5_dir.iterdir():
        if not file.suffix.lower() == ".pdf":
            error_list.append(f"{file.name} is not pdf/ introduces errors, need's manual json input")
            continue
        
        text = read_pdf(file)
        if text == "":
            error_list.append(f"{file.name} is not pdf/introduces errors, need's manual json input")
            continue

        form_type = determine_form_type(text)
        textblock = textblock_up_form(text, form_type)
        parsed = parse_text_block(textblock, form_type)
        if not parsed:
            continue

        # save individual json
        indiv_path = individual_dir / f"{parsed['name']}.json"
        with open(indiv_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, ensure_ascii=False, indent=4)
            print(f"Saved {indiv_path.name}")
    print("-"*100)
    print("Error logs")
    print("-"*100)
    for error in error_list:
        print(error)
    print("-"*100)

def save_alldata(base_dir):
    all_dir = base_dir / "truedata" / "alldata_json"
    individual_dir = base_dir / "truedata" / "individual_json"
    individual_dir_manual = base_dir / "truedata" / "individual_json_manual"
    all_path = all_dir / "alldata.json"

    # make sure output dir exists
    all_dir.mkdir(parents=True, exist_ok=True)

    all_data = []

    # collect all json files in individual_json
    for file in individual_dir.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                all_data.append(data)
            except json.JSONDecodeError:
                print(f"⚠️ Skipping invalid JSON file: {file.name}")
    
    # collect all json files in individual_json
    for file in individual_dir_manual.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                all_data.append(data)
            except json.JSONDecodeError:
                print(f"⚠️ Skipping invalid JSON file: {file.name}")

    # save combined file
    with open(all_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print("="*100)
    print(f"Saved {len(all_data)} student records to {all_path.name}")
    print("="*100)

# ===============================
# RUN PROGRAM
# ===============================

if __name__ == "__main__":
    base_dir = Path(r"C:\Users\verci\Documents\code\Tambay-Tracker\AutoMobChart1.0")
    process_all_pdfs(base_dir)
    save_alldata(base_dir)
