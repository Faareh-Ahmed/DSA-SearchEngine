import json
import hashlib
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import os

nltk.download("stopwords")
nltk.download("punkt")

# Initialize the inverted index dictionary and lexicon
inverted_index = {}
lexicon_file = "lexicon.json"
lexicon = {}


if os.path.exists(lexicon_file):
    # If it exists, load the existing data
    with open(lexicon_file, "r") as file:
        lexicon = json.load(file)

else:
    # If it doesn't exist, initialize with an empty dictionary
    with open(lexicon_file, "w") as file:
        json.dump({}, file)


# Path to test file
json_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\codeSpace\\test_forward_index_files\\forward_index_0.json"

# Opening the file
with open(json_file_path, "r") as file:
    data = json.load(file)

def get_word_id(word):
    if word in lexicon:
        # If word is already present, retrieve the associated word_id
        return lexicon[word]
    else:
        # If word is not present, add it to the lexicon along with its associated word_id
        word_id = len(lexicon) + 1  # Assign a unique word_id
        lexicon[word] = word_id
        with open(lexicon_file, "w") as file:
            json.dump(lexicon, file, indent=2)
        return word_id

for test_entry in data:
    doc_id = test_entry["doc_id"]
    stemmed_tokens = test_entry["stemmed_tokens"]
    frequency = test_entry["token_frequency"]

    for position, token in enumerate(stemmed_tokens, start=1):
        frequency = test_entry["token_frequency"][token]

        # Get word_id for the token from the lexicon
        word_id = get_word_id(token)

        if word_id not in inverted_index:
            inverted_index[word_id] = {"documents": [], "positions": {}, "frequency": {}}

        if doc_id not in inverted_index[word_id]["documents"]:
            inverted_index[word_id]["documents"].append(doc_id)

        if doc_id not in inverted_index[word_id]["positions"]:
            inverted_index[word_id]["positions"][doc_id] = [position]
        else:
            inverted_index[word_id]["positions"][doc_id].append(position)

        if doc_id not in inverted_index[word_id]["frequency"]:
            inverted_index[word_id]["frequency"][doc_id] = frequency



# Save inverted index to a file
inverted_index_file = "inverted_index.json"
with open(inverted_index_file, "w") as file:
    json.dump(inverted_index, file, indent=2)

print("Lexicon and Inverted Index stored in 'lexicon.json' and 'inverted_index.json'")
