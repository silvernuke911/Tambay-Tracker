import itertools

days = [("M", "Monday"), 
        ("T", "Tuesday"), 
        ("W", "Wednesday"), 
        ("Th", "Thursday"), 
        ("F", "Friday"), 
        ("S", "Saturday"), 
        ("Su", "Sunday")]

day_map = {}

# Generate all non-empty combinations
for r in range(1, len(days)+1):
    for combo in itertools.combinations(days, r):
        # key = concatenated short codes (e.g., "MWF", "TTh")
        key = "".join([c[0] for c in combo])
        # value = list of full names
        value = [c[1] for c in combo]
        day_map[key] = value

# Example: print some
for k in list(day_map):
    print(k, ":", day_map[k])

print("Total combos:", len(day_map))
