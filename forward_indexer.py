import json
import hashlib
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import os

nltk.download("stopwords")
nltk.download("punkt")

# nltk is a library to process natural language data for understandable by computer
from nltk.tokenize import word_tokenize, sent_tokenize

# Initialize the SnowballStemmer
stemmer = SnowballStemmer(language="english")

# Get the set of English stop words
stop_words = set(stopwords.words("english"))

# Specify the path to the folder containing JSON files
folder_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\newsdata"

# List all files in the specified folder
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

# Initializing a list to store forward index data
forward_index_data = []

# Initializing a dictionary to store tokens
tokens_dict = {}

# Counter to track the number of documents read
documents_read = 0

# Maximum number of documents to read
max_documents = 100000

def generate_doc_id(content):
    # Use SHA-256 hash function to generate a unique identifier
    hash_object = hashlib.sha256(content.encode("UTF-8"))
    doc_id = hash_object.hexdigest()
    # Convert the hexadecimal string to a long integer
    doc_id = int(doc_id, 16) 
    return doc_id

def hash_forwardindex(doc_id_hash):
    # Perform modulo 10 to split the forward index into 10 files
    result = doc_id_hash % 10
    return result

# Example usage:
print("Trying Forward Index")

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
        # Stop reading once the maximum number of documents is reached
        if documents_read >= max_documents:
            break

        print(f"{documents_read}.{article['title']}")

        document_title = article["url"]
        doc_id = generate_doc_id(document_title)
        file_index = hash_forwardindex(doc_id)

        # Check if that DocID is already present in that File_index
        forward_index_file = f"forward_index_{file_index}.json"

        try:
            with open(forward_index_file, "r") as file:
                forward_index_data = json.load(file)

            # Check if the doc_id is already present in the file
            if any(doc["doc_id"] == doc_id for doc in forward_index_data):
                print("\nThis DocID already exists\n")
                continue

        except FileNotFoundError:
            forward_index_data = []

        # Tokenize the content
        content = article["title"] + " " + article["content"]
        tokens = [word_tokenize(content)]

        # Remove stop words and punctuation, and stem the remaining words
        stemmed_words = [
            stemmer.stem(token)
            for sentence_tokens in tokens
            for token in sentence_tokens
            if token.isalnum() and token.lower() not in stop_words
        ]

        # Store tokens in the dictionary
        tokens_dict[i] = stemmed_words

        # Calculate token frequency
        # Flatten the list of lists (tokens)
        flat_tokens = [token for sentence_tokens in tokens for token in sentence_tokens]

        # Calculate token frequency using stemmed tokens
        token_frequency = {
            token: stemmed_words.count(token) for token in set(stemmed_words)
        }

        # Calculate token positions using stemmed tokens
        token_positions = {
            token: [i + 1 for i, word in enumerate(stemmed_words) if word == token]
            for token in set(stemmed_words)
        }

        # Create the forward index entry for the document
        forward_index_data.append({
            "doc_id": doc_id,
            "stemmed_tokens": tokens_dict[i],
            "token_frequency": token_frequency,
            "token_positions": token_positions,
            "url": article["url"],
            "date": article["date"],
            "published_utc": article["published_utc"],
            "collection_utc": article["collection_utc"],
        })

        # Write the forward index to a JSON file
        with open(forward_index_file, "w") as file:
            json.dump(forward_index_data, file, indent=2)

        documents_read += 1

print("Forward index Stored in Multiple Files")
 