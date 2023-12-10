import json
import nltk
import os

nltk.download("punkt")

# Initialize the inverted index dictionaries for each barrel
# barrels = {chr(i): {} for i in range(ord('a'), ord('z') + 1)}
# barrels.update({str(i): {} for i in range(10)})  # Include numeric characters 0-9
# barrels['other'] = {}  # Barrel for other characters


# Path to the folder for inverted index files
output_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

# Load existing inverted index barrels if they exist
barrels = {}
for char in range(ord('a'), ord('z') + 1):
    barrel_file = os.path.join(output_folder, f"inverted_index_{chr(char)}.json")
    if os.path.exists(barrel_file):
        with open(barrel_file, "r") as file:
            barrels[chr(char)] = json.load(file)

for char in range(10):
    barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
    if os.path.exists(barrel_file):
        with open(barrel_file, "r") as file:
            barrels[str(char)] = json.load(file)

barrel_file_other = os.path.join(output_folder, "inverted_index_other.json")
if os.path.exists(barrel_file_other):
    with open(barrel_file_other, "r") as file:
        barrels['other'] = json.load(file)

# print(barrels)

# Path to test file
json_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\forward_index_0.json"

# Opening the file of forward index
with open(json_file_path, "r") as file:
    data = json.load(file)

for test_entry in data:
    doc_id = test_entry["doc_id"]
    stemmed_tokens = test_entry["stemmed_tokens"]
    frequency = test_entry["token_frequency"]

    for position, token in enumerate(stemmed_tokens, start=1):
        frequency = test_entry["token_frequency"][token]

        # Get the first character of the token
        first_char = str(token)[0].lower() if str(token) else None


        # Ensure first_char is not None (empty or not a string)
        if first_char is not None:
            # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
            if '0' <= first_char <= '9':
                barrel = first_char
            elif 'a' <= first_char <= 'z':
                barrel = first_char
            else:
                barrel = 'other'


        # Create the inverted index entry for the token if not present in the barrel
            if token not in barrels[barrel]:
                barrels[barrel][token] = {"documents": [], "positions": {}, "frequency": {}}

            # Update the inverted index entry
            if doc_id not in barrels[barrel][token]["documents"]:
                barrels[barrel][token]["documents"].append(doc_id)

            if doc_id not in barrels[barrel][token]["positions"]:
                barrels[barrel][token]["positions"][doc_id] = [position]
            else:
                barrels[barrel][token]["positions"][doc_id].append(position)

            if doc_id not in barrels[barrel][token]["frequency"]:
                barrels[barrel][token]["frequency"][doc_id] = frequency

# Save inverted index barrels to separate files
for char, inverted_index in barrels.items():
    inverted_index_file = os.path.join(output_folder, f"inverted_index_{char}.json")
    with open(inverted_index_file, "w") as file:
        json.dump(inverted_index, file, indent=2)

print("Inverted Index barrels stored in files.")
