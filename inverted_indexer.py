import json
import nltk
import os
from math import log

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
for char1 in range(ord('a'), ord('z') + 1):
    for char2 in range(ord('a'), ord('z') + 1):
        char = str(chr(char1) + chr(char2))
        barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
        if os.path.exists(barrel_file):
            with open(barrel_file, "r") as file:
                barrels[char] = json.load(file)
        else:
            barrels[char] = {}

# Include combinations where the second character is from '0' to '9'
for char1 in range(ord('a'), ord('z') + 1):
    for char2 in range(ord('0'), ord('9') + 1):
        char = str(chr(char1) + chr(char2))
        barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
        if os.path.exists(barrel_file):
            with open(barrel_file, "r") as file:
                barrels[char] = json.load(file)
        else:
            barrels[char] = {}


for char in range(10):
    barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
    if os.path.exists(barrel_file):
        with open(barrel_file, "r") as file:
            barrels[str(char)] = json.load(file)
    else:
        barrels[str(char)]={}

barrel_file_other = os.path.join(output_folder, "inverted_index_other.json")
if os.path.exists(barrel_file_other):
    with open(barrel_file_other, "r") as file:
        barrels['other'] = json.load(file)
else:
        barrels['other']={}

# print(barrels)

# Path to test file
json_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\forward_index_0.json"
count=0
# Opening the file of forward index
with open(json_file_path, "r") as file:
    data = json.load(file)

for test_entry in data:
    count+=1
    print(count)
    if(count>10000):
        break
    doc_id = test_entry["doc_id"]
    stemmed_tokens = test_entry["stemmed_tokens"]
    frequency = test_entry["token_frequency"]

    for position, token in enumerate(stemmed_tokens, start=1):
        frequency = test_entry["token_frequency"][token]
        position = test_entry["token_positions"].get(token, [])

        # Calculate TF-IDF rank
        tf = frequency / len(stemmed_tokens)
        idf = log(len(stemmed_tokens) / (frequency + 1))  # Adding 1 to avoid division by zero
        rank = tf * idf
        # Get the first character of the token
        first_char = str(token)[0].lower() if str(token) else None


        # Ensure first_char is not None (empty or not a string)
        if first_char is not None:
            # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
            if '0' <= first_char <= '9':
                barrel = first_char

            elif 'a' <= first_char <= 'z':
                # print(token)
                if(len(token)<2):
                    second_char=first_char
                    char=str(first_char+second_char)
                    barrel=char
                else:
                    second_char = str(token)[1].lower() if str(token) else None
                    # Check if the second_char is not a lowercase letter or a digit
                    if('0' <= second_char <= '9') or ('a' <= second_char <= 'z'):
                        char=str(first_char+second_char)
                        barrel = char
                    else:
                        barrel = 'other'
            else:
                barrel = 'other'


        # Create the inverted index entry for the token if not present in the barrel
            if token not in barrels[barrel]:
                barrels[barrel][token] ={}

            # Update the inverted index entry
            if doc_id not in barrels[barrel][token]:
                word_details={
                    "frequency":frequency,
                    "position":position,
                    "rank":rank
                }
                barrels[barrel][token][doc_id]=word_details

                

            # if doc_id not in barrels[barrel][token]["positions"]:
            #     barrels[barrel][token]["positions"][doc_id] = [position]
            # else:
            #     barrels[barrel][token]["positions"][doc_id].append(position)

            # if doc_id not in barrels[barrel][token]["frequency"]:
            #     barrels[barrel][token]["frequency"][doc_id] = frequency

# Save inverted index barrels to separate files
print("Starting Writing to FIle\n")
for char, inverted_index in barrels.items():
    inverted_index_file = os.path.join(output_folder, f"inverted_index_{char}.json")
    with open(inverted_index_file, "w") as file:
        json.dump(inverted_index, file, indent=2)

print("Inverted Index barrels stored in files.")
