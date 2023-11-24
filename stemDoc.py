import json
import hashlib
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
nltk.download("stopwords")

nltk.download("punkt")
# nltk is a library to process natural language data for understandable by computer
from nltk.tokenize import word_tokenize, sent_tokenize
# Initialize the SnowballStemmer
stemmer = SnowballStemmer(language='english')
# Get the set of English stop words
stop_words = set(stopwords.words('english'))
# ******************* Printing the URLs from the documents *******************

# Specify the path to your JSON file
json_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\newsdata\\abcnews.json"

# Read the JSON data from the file
with open(json_file_path, "r") as file:
    json_data = file.read()

# Parse the JSON data
data = json.loads(json_data)




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
    tokens = [word_tokenize(content)]
    # Remove stop words and punctuation, and stem the remaining words
    stemmed_words = [stemmer.stem(token) for sentence_tokens in tokens for token in sentence_tokens if token.isalnum() and token.lower() not in stop_words]

    # Store tokens in the dictionary
    tokens_dict[i] = stemmed_words


    # Calculate token frequency
    # Flatten the list of lists (tokens)
    flat_tokens = [token for sentence_tokens in tokens for token in sentence_tokens]

    # Calculate token frequency using stemmed tokens
    token_frequency = {token: stemmed_words.count(token) for token in set(stemmed_words)}

    # Calculate token positions using stemmed tokens
    token_positions = {token: [i + 1 for i, word in enumerate(stemmed_words) if word == token] for token in set(stemmed_words)}

    # Create the forward index entry for the document
    forward_index[doc_id] = {
        "doc_id": doc_id,
        "stemmed_tokens": tokens_dict[i],
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
