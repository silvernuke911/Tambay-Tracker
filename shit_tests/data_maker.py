# tester.py
import random
import csv
random.seed(42)
# Load valid names from member_names.csv
with open('member_list.csv', mode='r') as file:
    valid_names = [line.strip() for line in file.readlines()]


with open('fabricated_data.csv', mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=':')
    
    for i in range(1, 32):
        date = f'10/{i:02}/24'
        sender = random.choice(valid_names)
        remaining_members = [name for name in valid_names if name != sender]
        members = random.sample(remaining_members, k=3)
        members_present = ', '.join(members + [sender])
        writer.writerow([date, sender, members_present])
        
        # Optionally print to the console for confirmation
        print(date, sender, members_present)
