import pandas as pd 
from pathlib import Path

base_dir = Path(r"C:\Users\verci\Documents\code\Tambay-Tracker\AutoMobChart1.0")
profiledir1 = base_dir / "truedata" / "Sigman_profile" / "UP PSF Residents Profile 1st Sem AY 25-26 (Responses).xlsx"
profiledir2 = base_dir / "truedata" / "Sigman_profile" / "First Semester AY 2025-2026 (Responses).xlsx"

profile1 = pd.read_excel(profiledir1)
profile2 = pd.read_excel(profiledir2)
print(profile1)
print(profile2)
sigmanprofile = pd.concat([profile1, profile2], axis=1)
print(sigmanprofile)
out_path = base_dir / "truedata" / "Sigman_profile" / "UP PSF SIGMAN PROFILE.csv"
sigmanprofile.to_csv(out_path, index=False, encoding="utf-8")