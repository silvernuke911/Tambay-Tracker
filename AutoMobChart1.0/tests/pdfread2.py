import pdfplumber
import re
from pathlib import Path
from typing import Optional, Dict, List, Union

class Form5Parser:
    """Parser for UP Form 5 and Form 5A documents."""
    
    # Constants
    FORM5A_IDENTIFIER = "U.P. FORM 5A"
    FORM5_IDENTIFIER = "UP FORM 5."
    OUT_WORDS = [
        "Admission", "Entrance", "Registration/Residence", "Library", 
        "Laboratory", "Computer", "Athletic", "Cultural", "Medical",
        "Dental", "Guidance", "Handbook", "School", "Development", 
        "EDF", "200.00"
    ]
    
    @staticmethod
    def read_pdf(path: Union[str, Path]) -> str:
        """Extract text from PDF file."""
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ''
        return text
    
    @staticmethod
    def extract_form5a_block(text: str) -> Optional[str]:
        """Extract Form 5A block from text."""
        match = re.search(
            r"STUDENT NUMBER[\s\S]+?Total units enlisted\s+[\d.]+",
            text, re.IGNORECASE
        )
        return match.group(0).strip() if match else None
    
    @staticmethod
    def extract_form5_block(text: str) -> Optional[str]:
        """Extract Form 5 block from text."""
        match = re.search(
            r"COLLEGE DEGREE[\s\S]+?\*+nothing follows\*+",
            text, re.IGNORECASE
        )
        return match.group(0).strip() if match else None
    
    def determine_form_type(self, text: str) -> str:
        """Determine which form type the text represents."""
        if self.FORM5A_IDENTIFIER in text:
            return "FORM5A"
        elif self.FORM5_IDENTIFIER in text:
            return "FORM5"
        return "UNKNOWN"
    
    def extract_text_block(self, text: str, form_type: str) -> Optional[str]:
        """Extract the relevant text block based on form type."""
        extractors = {
            "FORM5A": self.extract_form5a_block,
            "FORM5": self.extract_form5_block
        }
        return extractors.get(form_type, lambda x: None)(text)
    
    def parse_student_info_form5(self, lines: List[str]) -> Dict[str, str]:
        """Parse student information from Form 5."""
        course_line = lines[2].split()
        nameline_words = lines[1].split()
        
        info = {
            "college": course_line[0],
            "degree_major": " ".join(course_line[1:3]),
            "student_number": nameline_words[2]
        }
        
        if "NAME" in nameline_words:
            name_index = nameline_words.index("NAME")
            if "BS" in nameline_words:
                bs_index = nameline_words.index("BS")
                info["name"] = " ".join(nameline_words[name_index:bs_index])
                info["degree_major"] = " ".join(nameline_words[bs_index:])
            else:
                info["name"] = " ".join(nameline_words[name_index:])
        
        return info
    
    def parse_student_info_form5a(self, lines: List[str]) -> Dict[str, str]:
        """Parse student information from Form 5A."""
        nameline_words = lines[1].split()
        return {
            "student_number": nameline_words[0],
            "name": " ".join(nameline_words[1:-3]),
            "college": nameline_words[-3],
            "degree_major": " ".join(nameline_words[-2:])
        }
    
    def clean_subject_line(self, line: str, form_type: str) -> List[str]:
        """Clean and split a subject line."""
        words = line.split()
        
        if form_type == "FORM5":
            for outword in self.OUT_WORDS:
                if outword in words:
                    words = words[:words.index(outword)]
                    break
        elif form_type == "FORM5A" and "Cancel" in words:
            words = words[:words.index("Cancel")]
            
        return words
    
    def parse_subject_info(self, words: List[str]) -> Dict[str, str]:
        """Parse subject information from cleaned words."""
        subject_type = words[1]
        
        if subject_type == "PE":
            return self._parse_pe_subject(words)
        elif subject_type == "FA":
            return self._parse_fa_subject(words)
        return self._parse_regular_subject(words)
    
    def _parse_pe_subject(self, words: List[str]) -> Dict[str, str]:
        """Parse PE subject information."""
        if words[2] == "1":
            return {
                "subject": " ".join(words[1:3]),
                "section": words[3],
                "units": words[4],
                "offset": 5
            }
        return {
            "subject": " ".join(words[1:4]),
            "section": words[4],
            "units": words[5],
            "offset": 6
        }
    
    def _parse_fa_subject(self, words: List[str]) -> Dict[str, str]:
        """Parse FA subject information."""
        return {
            "subject": " ".join(words[1:3]),
            "section": "".join(words[3:6]),
            "units": words[6],
            "offset": 7
        }
    
    def _parse_regular_subject(self, words: List[str]) -> Dict[str, str]:
        """Parse regular subject information."""
        return {
            "subject": " ".join(words[1:3]),
            "section": words[3],
            "units": words[4],
            "offset": 5
        }
    
    def parse_instructor(self, words: List[str]) -> str:
        """Parse instructor information."""
        if words[-2] in ["TBA", "CONCEALED"]:
            return words[-2]
        return " ".join(words[-3:-1])
    
    def parse_schedule(self, schedule_str: str) -> List[Dict[str, str]]:
        """Parse schedule information."""
        schedule = []
        for sched in [s.strip() for s in schedule_str.split(";") if s.strip()]:
            parts = sched.split()
            if not parts:
                continue
                
            schedule.append({
                "day": parts[0],
                "time": parts[1],
                "class_type": parts[2],
                "room": "TBA" if parts[-1] == "TBA" else " ".join(parts[-2:])
            })
        return schedule
    
    def print_student_info(self, info: Dict[str, str]):
        """Print formatted student information."""
        print(f"NAME            : {info['name']}")
        print(f"STUDENT NUMBER  : {info['student_number']}")
        print(f"COLLEGE         : {info['college']}")
        print(f"DEGREE MAJOR    : {info['degree_major']}")
        print("=" * 50)
    
    def print_class_info(self, class_info: Dict[str, Union[str, List]]):
        """Print formatted class information."""
        print(f"CLASS CODE    : {class_info['class_code']}")
        print(f"SUBJECT       : {class_info['subject']}")
        print(f"SECTION       : {class_info['section']}")
        print(f"UNITS         : {class_info['units']}")
        
        if "instructor" in class_info:
            print(f"INSTRUCTOR    : {class_info['instructor']}")
            
        print(f"SCHEDULE      : {'; '.join([f'{s['day']} {s['time']}' for s in class_info['schedule']])}")
        
        for sched in class_info["schedule"]:
            print("-" * 50)
            print(f"DAY      : {sched['day']}")
            print(f"TIME     : {sched['time']}")
            print(f"TYPE     : {sched['class_type']}")
            print(f"ROOM     : {sched['room']}")
        
        print("=" * 50)
    
    def parse_form5_block(self, textblock: str, ifprint: bool = True) -> List[Dict]:
        """Parse Form 5 text block."""
        lines = [line.strip() for line in textblock.split("\n") if line.strip()]
        if len(lines) < 4:
            return []
        
        student_info = self.parse_student_info_form5(lines)
        if ifprint:
            self.print_student_info(student_info)
        
        classes = []
        for line in lines[4:-1]:
            if not line.strip():
                continue
                
            words = self.clean_subject_line(line, "FORM5")
            if len(words) < 2:
                continue
                
            class_info = {
                "class_code": words[0],
                **self.parse_subject_info(words),
                "schedule": self.parse_schedule(" ".join(words[5:]))
            }
            
            classes.append(class_info)
            if ifprint:
                self.print_class_info(class_info)
        
        return classes
    
    def parse_form5a_block(self, textblock: str, ifprint: bool = True) -> List[Dict]:
        """Parse Form 5A text block."""
        lines = [line.strip() for line in textblock.split("\n") if line.strip()]
        if len(lines) < 4:
            return []
        
        student_info = self.parse_student_info_form5a(lines)
        if ifprint:
            self.print_student_info(student_info)
        
        classes = []
        for line in lines[4:-1]:
            if not line.strip():
                continue
                
            words = self.clean_subject_line(line, "FORM5A")
            if len(words) < 2:
                continue
                
            subject_info = self.parse_subject_info(words)
            offset = subject_info.pop("offset")
            
            class_info = {
                "class_code": words[0],
                **subject_info,
                "instructor": self.parse_instructor(words),
                "schedule": self.parse_schedule(" ".join(
                    words[offset:-3] if words[-2] not in ["TBA", "CONCEALED"] 
                    else words[offset:-2]
                ))
            }
            
            classes.append(class_info)
            if ifprint:
                self.print_class_info(class_info)
        
        return classes
    
    def parse_text_block(self, textblock: str, form_type: str, ifprint: bool = True) -> List[Dict]:
        """Parse text block based on form type."""
        parsers = {
            "FORM5": self.parse_form5_block,
            "FORM5A": self.parse_form5a_block
        }
        return parsers.get(form_type, lambda x, y: [])(textblock, ifprint)


def main():
    parser = Form5Parser()
    form5_dir = Path(r"C:\Users\verci\Documents\code\Tambay-Tracker\AutoMobChart1.0\tests\sample_form5")
    
    for pdf_path in form5_dir.glob("*.pdf"):
        print(pdf_path)
        text = parser.read_pdf(pdf_path)
        form_type = parser.determine_form_type(text)
        textblock = parser.extract_text_block(text, form_type)
        
        print("*" * 130)
        parsed = parser.parse_text_block(textblock, form_type)
        print("=" * 130)


if __name__ == "__main__":
    main()