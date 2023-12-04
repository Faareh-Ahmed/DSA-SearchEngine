import json
import hashlib
import os

# Specify the path to the folder containing JSON files
folder_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\newsdata"

# Specify the output file for storing checksums and docIDs
checksum_file = "checksum.json"

# List all files in the specified folder
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

# Dictionary to store checksums and corresponding docIDs
checksum = {}

# Initialize docID to 1
doc_id = 1

# Iterate through each JSON file
for json_file in json_files:
    # Construct the full path to the JSON file
    json_file_path = os.path.join(folder_path, json_file)

    # Read the JSON data from the file
    with open(json_file_path, "r") as file:
        json_data = file.read()

    # Parse the JSON data
    data = json.loads(json_data)

    for i, article in enumerate(data, 1):
        if doc_id>100000:
            break

        # Generate checksum by hashing the URL
        url = article["url"]
        checksum_id = hashlib.sha256(url.encode("UTF-8")).hexdigest()

        # Check if the checksum already exists in the dictionary
        if checksum_id in checksum:
            print(f"Duplicate entry for checksum {checksum_id}. Skipping...")
            continue
        else:
            # Store checksum and corresponding docID in the dictionary
            print(f"{doc_id}")
            checksum[checksum_id] = doc_id

        # Increment docID for the next entry
        doc_id += 1

# Save the checksums and docIDs to a JSON file
with open(checksum_file, "w") as file:
    json.dump(checksum, file, indent=2)

print(f"Checksums and DocIDs stored in {checksum_file}")
