import os
from pathlib import Path

print("=== SYSTEM CHECK ===")
print(f"Python running from: {os.getcwd()}")
print("\nFiles in directory:")
for f in os.listdir():
    print(f"- {f}")

key_path = Path(r"D:\doctor_data_system\serviceAccountKey.json")
print(f"\nKey exists at specified path: {key_path.exists()}")
print(f"Absolute path: {key_path.absolute()}")
print(f"File size: {key_path.stat().st_size if key_path.exists() else 0} bytes")
