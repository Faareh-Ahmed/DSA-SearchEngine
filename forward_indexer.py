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

# Create a folder to store forward index files
output_folder = "forward_index_files"
os.makedirs(output_folder, exist_ok=True)

# List all files in the specified folder
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

# Maximum file size in bytes
max_file_size = 1024 * 1024  # 1 MB

# Initializing a dictionary to store tokens
tokens_dict = {}

# Set to keep track of existing doc_ids
existing_doc_ids = set()
existing_doc_ids_file = "existing_doc_ids.txt"

# Load existing doc_ids from the file if it exists
if os.path.exists(existing_doc_ids_file):
    with open(existing_doc_ids_file, "r") as file:
        existing_doc_ids = set(file.read().splitlines())

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

# def hash_forwardindex(doc_id_hash):
#     # Perform modulo 10 to split the forward index into 10 files
#     result = doc_id_hash % 10
#     return result

# Example usage:
print("Trying Forward Index")
count=0
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
        # file_index = hash_forwardindex(doc_id)
        # Check if the doc_id already exists
        if doc_id in existing_doc_ids:
            print("DocID already exists")
            continue

            # Update the set of existing doc_ids
        existing_doc_ids.add(doc_id)
        # Check if that DocID is already present in that File_index
        forward_index_file = f"{output_folder}\\forward_index_{count}.json"

        try:
            # Read existing forward index data
            with open(forward_index_file, "r") as file:
                forward_index_data = json.load(file)
            # Check if the document with the same doc_id already exists in the file
            
            # Check if the file size exceeds the threshold
            if os.path.exists(forward_index_file) and os.path.getsize(forward_index_file) > max_file_size:
                # If so, create a new file with an incremented index
                count+=1
                forward_index_file = f"{output_folder}\\forward_index_{count}.json"
                forward_index_data = []

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

# Save the updated set of existing doc_ids to the file
with open(existing_doc_ids_file, "w") as file:
    file.write("\n".join(map(str, existing_doc_ids)))
print("Forward index Stored in Multiple Files with Size Limit and Organized in a Folder")