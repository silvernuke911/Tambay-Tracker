import json
from datetime import datetime

# path to your JSON
JSON_PATH = r"C:\Users\verci\Documents\code\Tambay-Tracker\AutoMobChart1.0\truedata\alldata_json\alldata.json"

# normalize day mappings (expand shorthand like TTh → T, Th)
day_map = {
    "M": ["M"],
    "T": ["T"],
    "W": ["W"],
    "Th": ["Th"],
    "F": ["F"],
    "S": ["S"],
    "Su": ["Su"],
    "MWF": ["M", "W", "F"],
    "TTh": ["T", "Th"],
    "WF": ["W", "F"],
}

def load_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def check_availability(data, target_day, start_time, end_time):
    fmt = "%I:%M%p"

    start = datetime.strptime(start_time.upper(), fmt)
    end = datetime.strptime(end_time.upper(), fmt)

    unavailable = []
    available = []

    for student in data:
        busy = False
        for subj in student["subjects"]:
            for sched in subj["schedule"]:
                raw_day = sched.get("day", "")
                mapped_days = []
                for k, v in day_map.items():
                    if raw_day == k:
                        mapped_days = v
                        break

                if target_day not in mapped_days:
                    continue

                try:
                    s = datetime.strptime(sched["time start"].upper(), fmt)
                    e = datetime.strptime(sched["time end"].upper(), fmt)
                except:
                    continue

                # Overlap check
                if s < end and e > start:
                    busy = True
                    unavailable.append({
                        "name": student["name"],
                        "subject": subj["subject"],
                        "room": sched.get("room", "TBA")
                    })
        if not busy:
            available.append(student["name"])

    return unavailable, available

def main():
    data = load_data()

    print("=== Availability Checker ===")
    day = input("Enter day (M/T/W/Th/F/S/Su): ").strip()
    start = input("Enter start time (e.g. 9:00AM): ").strip()
    end = input("Enter end time (e.g. 10:30AM): ").strip()
    if end == "":
        end = start
    unavail, avail = check_availability(data, day, start, end)

    print("\n--- UNAVAILABLE ---")
    if not unavail:
        print("None")
    else:
        for u in unavail:
            print(f"- {u['name']} | {u['subject']} | {u['room']}")

    print("\n--- AVAILABLE ---")
    if not avail:
        print("None")
    else:
        for a in avail:
            print(f"- {a}")

if __name__ == "__main__":
    main()
