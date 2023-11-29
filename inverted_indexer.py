

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
json_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\codeSpace\\forward_index_0.json"

# Opening the file
with open(json_file_path, "r") as file:
    data = json.load(file)

for test_entry in data:
    doc_id = test_entry["doc_id"]
    stemmed_tokens = test_entry["stemmed_tokens"]
    frequency = test_entry["token_frequency"]

    for position, token in enumerate(stemmed_tokens, start =1):
        frequency = test_entry["token_frequency"][token]
        if token not in inverted_index:
            inverted_index[token] = {"documents": [], "positions": {}, "frequency": {}}

        if doc_id not in inverted_index[token]["documents"]:
            inverted_index[token]["documents"].append(doc_id)
        
        if doc_id not in inverted_index[token]["positions"]:
            inverted_index[token]["positions"][doc_id]=[position]
        else:
            inverted_index[token]["positions"][doc_id].append(position)

        if doc_id not in inverted_index[token]["frequency"]:
            inverted_index[token]["frequency"][doc_id] = frequency
        

inverted_index_test_file = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\codeSpace\\inverted_index_test_file.json"
inverted_index_file = "inverted_index.json"
with open(inverted_index_test_file, "w") as file:
    json.dump(inverted_index, file, indent=2)

print("Inverted index stored in 'inverted_index.json'")