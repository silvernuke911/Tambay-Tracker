def is_leap_year(year):
    """Check if a given year (formatted as YY) is a leap year."""
    year_full = 2000 + year  # Convert YY to YYYY, assuming 2000s
    return (year_full % 4 == 0 and year_full % 100 != 0) or (year_full % 400 == 0)

def days_in_month(month, year):
    """Return the number of days in a given month, accounting for leap years."""
    if month in {4, 6, 9, 11}:
        return 30  # April, June, September, November have 30 days
    elif month == 2:
        return 29 if is_leap_year(year) else 28  # February depends on leap year
    else:
        return 31  # All other months have 31 days

for yr in range(25,26):  # Loop over years (e.g., 2024 and 2025)
    for mo in range(1, 12 + 1):  # Loop over each month
        for day in range(1, days_in_month(mo, yr) + 1):  # Loop up to the correct day count
            print(f'{mo:02}/{day:02}/{yr},0')
