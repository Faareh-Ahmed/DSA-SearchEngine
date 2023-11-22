import json
import hashlib
import nltk

nltk.download("punkt")
# nltk is a library to process natural language data for understandable by computer
from nltk.tokenize import word_tokenize, sent_tokenize


# ******************* Printing the URLs from the documents *******************

# Specify the path to your JSON file
json_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\newsdata\\abcnews.json"

# Read the JSON data from the file
with open(json_file_path, "r") as file:
    json_data = file.read()

# Parse the JSON data
data = json.loads(json_data)

# Extract and print URL's of the first 10 documents
for i, article in enumerate(data[:10], 1):
    print(f"{i}. {article['url']}")
print("Hello")


# ************ Printing the total Documents in the abcnews *******

count = 0
for i in enumerate(data):
    if article["title"]:
        count += 1


print("Total Documents = ", count)


# *********** Forward index of First Document ***********

# Initialize the forward index dictionary
forward_index = {}
# Initializing a dictionary to store tokens
tokens_dict = {}


def generate_doc_id(content):
    # Use SHA-256 hash function to generate a unique identifier
    hash_object = hashlib.sha256(content.encode("UTF-8"))
    doc_id = hash_object.hexdigest()
    # Convert the hexadecimal string to a long integer
    doc_id = int(doc_id, 16)
    return doc_id


# Example usage:
print("Trying Forward INdex")

for i, article in enumerate(data[:1], 1):
    print(f" {i}.{article['title']}")
    document_title = article["id"]
    doc_id = generate_doc_id(document_title)
    # Tokenize the content
    content = article["content"]
    sentences = sent_tokenize(content)
    tokens = [word_tokenize(sentence) for sentence in sentences]

    # Store tokens in the dictionary
    tokens_dict[i] = tokens
    # Calculate token frequency
    # Flatten the list of lists (tokens)
    flat_tokens = [token for sentence_tokens in tokens for token in sentence_tokens]

    # Calculate token frequency
    token_frequency = {token: flat_tokens.count(token) for token in set(flat_tokens)}
    # Calculate token positions
    token_positions = {
        token: [i + 1 for i, word in enumerate(flat_tokens) if word == token]
        for token in set(flat_tokens)
    }

    # Create the forward index entry for the document
    forward_index[doc_id] = {
        "doc_id": doc_id,
        "tokens": tokens,
        "token_frequency": token_frequency,
        "token_positions": token_positions,
        "url": article["url"],
        "date": article["date"],
        "published_utc": article["published_utc"],
        "collection_utc": article["collection_utc"],
    }

# Write the forward index to a JSON file
output_file_path = "forward_index.json"
with open(output_file_path, "w") as output_file:
    json.dump(forward_index, output_file, indent=2)

print(f"Original Content: {document_title}")
print(f"Generated DocID: {doc_id}")

# Print the forward index for the first document
print("Forward index Stored in File")
