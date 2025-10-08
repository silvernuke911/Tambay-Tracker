import datetime as dt

def generate_date_list(start_date, end_date, filename="date_list_blank.csv"):
    """
    Generates a CSV with format:
    MM/DD/YY,DayOfWeek,0,0
    from start_date to end_date (inclusive)
    """

    # Parse inputs (e.g. "2025-09-09")
    start = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end = dt.datetime.strptime(end_date, "%Y-%m-%d")

    # Open file and write
    with open(filename, "w") as f:
        current = start
        while current <= end:
            line = f"{current.strftime('%m/%d/%y')},{current.strftime('%A')},0,0\n"
            f.write(line)
            current += dt.timedelta(days=1)

    print(f"✅ File saved as '{filename}' ({start_date} → {end_date})")

# Example usage:
generate_date_list("2025-09-20", "2026-09-20")
