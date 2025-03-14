import json
import os
import sys

# Get arguments from batch script
if len(sys.argv) < 5:
    print("Usage: python update_json.py <channel> <current_dir> <file_count> <json_file>")
    sys.exit(1)

channel = sys.argv[1]  # e.g., "Ex_639_Ch3"
current_dir = sys.argv[2] # e.g., "Ex_639_Ch3_stitched"
file_count = int(sys.argv[3])  # e.g., 3000
json_file = sys.argv[4]  # Path to JSON file (e.g., "C:/path/to/output.json")

# Ensure JSON file exists or create an empty dictionary
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)  # Read existing JSON
        except json.JSONDecodeError:
            data = {}  # If file is corrupt, start fresh
else:
    data = {}

# Update or add the new entry
data[channel] = {
    "current_directory": current_dir,
    "file_count": file_count
}

# Write updated JSON back to file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print(f"Updated JSON saved to: {json_file}")