import pdfplumber
import re
import os
from pathlib import Path
import json

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
        day = sched_field[0]
        time = sched_field[1]
        times = time.split("-")
        time_start = times[0].upper()
        time_end = times[1].upper()
        if not has_am_pm(time_start) and has_am_pm(time_end):
            time_start += time_end[-2:]
        time_start = add_colon_zero(time_start)
        time_end = add_colon_zero(time_end)
        class_type = sched_field[2]
        if sched_field[-1] == "TBA":
            room_no = sched_field[-1]
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

def parse_text_block(textblock, form_type):
    if form_type == "FORM5":
        return parse_form5_block(textblock)
    elif form_type == "FORM5A":
        return parse_form5a_block(textblock)
    else:
        return "UNKNOWN FORM TYPE"
    
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
        name_list = nameline_words[name_index:BS_index]
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
                "200.00"]
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
                subject = " ".join(subject_line[1:4])  # PE 2 XYZ
                section = subject_line[4]
                units = subject_line[5]
                offset = 6
        elif second_word == "FA":
            subject = " ".join(subject_line[1:3])  # FA XYZ
            section = "".join(subject_line[3:6])
            units = subject_line[6]
            offset = 7
        else:
            subject = " ".join(subject_line[1:3])  # e.g., MATH 100
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
    student_dict = {
        "name": name,
        "student number": student_number,
        "college": college,
        "degree major": degree_major,
        "subjects": subject_entries
    }
    return student_dict

def parse_form5a_block(textblock):
    lines = textblock.split('\n')
    nameline = lines[1]
    nameline_words = nameline.split(" ")
    student_number = nameline_words[0]
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
                subject = " ".join(subject_line[1:3])  # PE 1
                section = subject_line[3]
                units = subject
                offset = 4
            else:
                subject = " ".join(subject_line[1:4])  # PE 2 XYZ
                section = subject_line[4]
                offset = 5
        elif second_word == "FA":
            subject = " ".join(subject_line[1:3])  # FA XYZ
            section = "".join(subject_line[3:6])
            offset = 6
        else:
            subject = " ".join(subject_line[1:3])  # e.g., MATH 100
            section = subject_line[3]
            offset = 4
        units = subject_line[-1]
        if subject_line[-2] in ["TBA", "CONCEALED"]:
            instructor = subject_line[-2]
        else:
            instructor = " ".join(subject_line[-3:-1])
        schedule_words = subject_line[offset:-3] if subject_line[-2] not in ["TBA", "CONCEALED"] else subject_line[offset:-2]
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
    student_dict = {
        "name": name,
        "student number": student_number,
        "college": college,
        "degree major": degree_major,
        "subjects": subject_entries
    }
    return student_dict

def parse_text_block(textblock, form_type):
    if form_type == "FORM5":
        return parse_form5_block(textblock)
    elif form_type == "FORM5A":
        return parse_form5a_block(textblock)
    else:
        return "UNKNOWN FORM TYPE"
    
def pdfread(form5_dir, pdftext_dir):
    pdf_files = list(form5_dir.glob("*.pdf"))
    for pdf_path in pdf_files:
        print(pdf_path)
        text = read_pdf(pdf_path)
        filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".txt"
        save_path = os.path.join(
            pdftext_dir,
            filename
        )
        if os.path.exists(save_path):
            overwrite = "y"  # Change to input(...) if you want to prompt
            if overwrite != 'y':
                print(f"Skipped: {filename}")
                continue
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
            print(f"Saved to: {save_path}")


def pdf_load(pdftext_dir):
    # --- Step 2: Read and parse textblocks from directory ---
    for fname in os.listdir(pdftext_dir):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(pdftext_dir, fname), "r", encoding="utf-8") as f:
            text = f.read()
        form_type = determine_form_type(text)
        textblock = textblock_up_form(text, form_type)
        parsed = parse_text_block(textblock, form_type)
        print("*"*130)
        print("="*130)
        print(f"NAME            : {parsed["name"]}")
        print(f"STUDENT NO     : {parsed["student number"]}")
        print(f"COLLEGE/MAJOR  : {" ".join([parsed["college"], parsed["degree major"]])}")
        for subject in parsed["subjects"]:
            print("-"*100)
            print(f"  CLASS CODE : {subject["class code"]}")
            print(f"  SUBJECT    : {subject["subject"]}")
            print(f"  SECTION    : {subject["section"]}")
            print(f"  UNITS      : {subject["units"]}")
            print("- "*50 + '-')
            for schedline in subject["schedule"]:
                print(f"    DAY        : {schedline["day"]}")
                print(f"    TIME START : {schedline["time start"]}")
                print(f"    TIME END   : {schedline["time end"]}")
                print(f"    TYPE       : {schedline["type"]}")
                print(f"    ROOM       : {schedline["room"]}")
        print("=" * 130)

def save_json(filename, pdftext_dir, base_dir):
    all_data = []
    for fname in os.listdir(pdftext_dir):
        if not fname.endswith(".txt"):
            continue
        with open(os.path.join(pdftext_dir, fname), "r", encoding="utf-8") as f:
            full_text = f.read()
        form_type = determine_form_type(full_text)
        textblock = textblock_up_form(full_text, form_type)
        parsed = parse_text_block(textblock, form_type)
        all_data.append(parsed)
    save_path = base_dir / filename
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
    print(f"Saved all data to {filename}")

def load_json(filename, base_dir):
    source_path = base_dir / filename
    with open(source_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for student in data:
        print("*"*130)
        print("="*130)
        print(f"NAME            : {student["name"]}")
        print(f"STUDENT NO     : {student["student number"]}")
        print(f"COLLEGE/MAJOR  : {" ".join([student["college"], student["degree major"]])}")
        for subject in student["subjects"]:
            print("-"*100)
            print(f"  CLASS CODE : {subject["class code"]}")
            print(f"  SUBJECT    : {subject["subject"]}")
            print(f"  SECTION    : {subject["section"]}")
            print(f"  UNITS      : {subject["units"]}")
            print("- "*50 + '-')
            for schedline in subject["schedule"]:
                print(f"    DAY        : {schedline["day"]}")
                print(f"    TIME START : {schedline["time start"]}")
                print(f"    TIME END   : {schedline["time end"]}")
                print(f"    TYPE       : {schedline["type"]}")
                print(f"    ROOM       : {schedline["room"]}")
        print("=" * 130)

base_dir = Path(r"C:\Users\verci\Documents\Python Code\Tambay-Tracker\AutoMobChart1.0\tests")
form5_dir = base_dir / "sample_form5"
pdf_files = list(form5_dir.glob("*.pdf"))
pdftext_dir = base_dir / "pdftext"
os.makedirs(pdftext_dir, exist_ok=True)
json_filename = "brod_data.json"
## pdfread()
save_json(form5_dir, pdftext_dir, base_dir)
load_json(json_filename, base_dir)
