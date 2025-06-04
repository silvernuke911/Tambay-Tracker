import pdfplumber
import re
from pathlib import Path

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
    
def parse_form5_block(textblock, ifprint = True):
    #print(textblock)
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
        name_list = nameline_words[name_index:]
    if "BS" in nameline_words:
        BS_index = nameline_words.index("BS")
        name_list = nameline_words[name_index:BS_index]
        degree_major = " ".join(nameline_words[BS_index:])
    name = " ".join(name_list)
    if ifprint:
        print(f"NAME            : {name}")
        print(f"STUDENT NUMBER  : {student_number}")
        print(f"COLLEGE         : {college}")
        print(f"DEGREE MAJOR    : {degree_major}")
        print("="*50)
    subject_words = lines[4:-1]
    out_list = ["Admission", "Entrance", "Registration/Residence", "Library", "Laboratory", "Computer", "Athletic", "Cultural", "Medical","Dental","Guidance", "Handbook", "School", "Development", "EDF", "200.00"]
    for line in subject_words:
        subject_line = line.split(" ")
        if len(subject_line)<2:
            continue
        for outword in out_list:
            if outword in subject_line:
                out_index = subject_line.index(outword)
                subject_line = subject_line[:out_index]
        # print(subject_line)
        class_code = subject_line[0]
        second_word = subject_line[1]
        subject = ""
        section = ""
        units = ""
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
        if ifprint:
            print(f"CLASS CODE    : {class_code}")
            print(f"SUBJECT       : {subject}")
            print(f"SECTION       : {section}")
            print(f"UNITS         : {units}")
            print(f"SCHEDULE      : {schedule}")
        schedlines = [s.strip() for s in schedule.split(";")]
        for sched in schedlines:     
            sched_field = sched.split(" ")
            day = sched_field[0]
            time = sched_field[1]
            class_type = sched_field[2]
            if sched_field[-1] == "TBA":
                room_no = sched_field[-1]
            else:
                room_no = " ".join(sched_field[-2:])
            if ifprint:
                print('-'*50)
                print(f"DAY      : {day}")
                print(f"TIME     : {time}")
                print(f"TYPE     : {class_type}")
                print(f"ROOM     : {room_no}")
        if ifprint:
            print('='*50)

def parse_form5a_block(textblock, ifprint = True):
    lines = textblock.split('\n')
    nameline = lines[1]
    nameline_words = nameline.split(" ")
    student_number = nameline_words[0]
    degree_major = " ".join(nameline_words[-2:])
    college = nameline_words[-3]
    name = " ".join(nameline_words[1:-3])
    if ifprint:
        print(f"NAME            : {name}")
        print(f"STUDENT NUMBER  : {student_number}")
        print(f"COLLEGE         : {college}")
        print(f"DEGREE MAJOR    : {degree_major}")
        print("="*50)
    subject_words = lines[4:-1]
    for line in subject_words:
        subject_line = line.split(" ")
        # Remove trailing info if "Cancel" appears
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

        # Collect lines not used as 'schedule'
        schedule_words = subject_line[offset:-3] if subject_line[-2] not in ["TBA", "CONCEALED"] else subject_line[offset:-2]
        schedule = " ".join(schedule_words)
        if ifprint:
            print(f"CLASS CODE    : {class_code}")
            print(f"SUBJECT       : {subject}")
            print(f"SECTION       : {section}")
            print(f"UNITS         : {units}")
            print(f"INSTRUCTOR    : {instructor}")
            print(f"SCHEDULE      : {schedule}")
        schedlines = [s.strip() for s in schedule.split(";")]
        for sched in schedlines:
            
            sched_field = sched.split(" ")
            day = sched_field[0]
            time = sched_field[1]
            class_type = sched_field[2]
            if sched_field[-1] == "TBA":
                room_no = sched_field[-1]
            else:
                room_no = " ".join(sched_field[-2:])
            if ifprint:
                print('-'*50)
                print(f"DAY      : {day}")
                print(f"TIME     : {time}")
                print(f"TYPE     : {class_type}")
                print(f"ROOM     : {room_no}")
        if ifprint:
            print('='*50)
        
def parse_text_block(textblock, form_type):
    if form_type == "FORM5":
        return parse_form5_block(textblock)
    elif form_type == "FORM5A":
        return parse_form5a_block(textblock)
    else:
        return "UNKNOWN FORM TYPE"

form5_dir = Path(r"C:\Users\verci\Documents\Python Code\Tambay-Tracker\AutoMobChart1.0\tests\sample_form5")
pdf_files = list(form5_dir.glob("*.pdf"))  # Only .pdf files
for pdf_path in pdf_files:
    print(pdf_path)
    text = read_pdf(pdf_path)
    form_type = determine_form_type(text)
    textblock = textblock_up_form(text, form_type)
    # print(textblock)
    print("*"*130)
    parsed = parse_text_block(textblock, form_type)
    print("="*130)

