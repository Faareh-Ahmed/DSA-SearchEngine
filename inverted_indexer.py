import json
import hashlib
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import os

nltk.download("stopwords")
nltk.download("punkt")

# Initialize the inverted index dictionary
inverted_index = {}

# Path to test file
json_file_path = "C:\\Users\\Ghouri\\Desktop\\Git\\DSA-SearchEngine\\Test_forward_index.json"

# Opening the file
with open(json_file_path, "r") as file:
    data = json.load(file)

for test_entry in data:
    doc_id = test_entry["doc_id"]
    stemmed_tokens = test_entry["stemmed_tokens"]

    for token in stemmed_tokens:
        

inverted_index_test_file = "C:\\Users\\Ghouri\\Desktop\\Git\\DSA-SearchEngine\\inverted_index_test_file.json"
inverted_index_file = "inverted_index.json"
with open(inverted_index_test_file, "w") as file:
    json.dump(inverted_index, file, indent=2)

print("Inverted index stored in 'inverted_index.json'")
# Separation

# Initialize the inverted index dictionary
inverted_index = {}

forward_index_path = "C:\\Users\\Ghouri\\Desktop\\Git\\DSA-SearchEngine\\forward_index_0.json"

with open(forward_index_path, "r") as file:
     forward_index_data = json.load(file)
# Iterate through each document in the forward index data
for document_entry in forward_index_data:
    doc_id = document_entry["doc_id"]
    stemmed_tokens = document_entry["stemmed_tokens"]

    # Update the inverted index for each token in the document
    for position, token in enumerate(stemmed_tokens, start=1):
        if token not in inverted_index:
            inverted_index[token] = {"documents": [], "positions": {}}

        # Update document information
        if doc_id not in inverted_index[token]["documents"]:
            inverted_index[token]["documents"][doc_id] = 1
        else:
            inverted_index[token]["documents"][doc_id] += 1

        # Update position information
        if doc_id not in inverted_index[token]["positions"]:
            inverted_index[token]["positions"][doc_id] = [position]
        else:
            inverted_index[token]["positions"][doc_id].append(position)

# Write the inverted index to a JSON file

