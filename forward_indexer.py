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
output_folder = "faareh_forward_index"
os.makedirs(output_folder, exist_ok=True)

# List all files in the specified folder
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

# Maximum file size in bytes to make the speed faster
max_file_size = 1024 * 1024  # 1 MB

# Initializing a dictionary to store tokens
tokens_dict = {}
glb_doc_id = 0

documents_read = 0

# Load checksums and docIDs from the checksum file if it exists
checksum_file = "checksum.json"
urlfile="docURL.json"
urlfile_data ={}
checksum_data = {}
# check if the file exists
if os.path.exists(checksum_file):
    # If it exists, load the existing data
    with open(checksum_file, "r") as file:
        checksum_data = json.load(file)

    with open(urlfile,"r") as file:
        urlfile_data=json.load(file)
    # Find the maximum doc_id among existing entries
    max_existing_doc_id = max(checksum_data.values(), default=0)
    documents_read=max_existing_doc_id
    glb_doc_id = max_existing_doc_id + 1
else:
    # If it doesn't exist, initialize with an empty dictionary
    # glb_doc_id = 1
    with open(checksum_file, "w") as file:
        json.dump({}, file)



# Counter to track the number of documents read

# Maximum number of documents to read
max_documents = 10000


def get_doc_id_from_checksum(checksum,url):
    global glb_doc_id  # Declare glb_doc_id as a global variable
    if checksum in checksum_data:
        # If checksum is already present, retrieve the associated doc_id
        return 0
    else:
        # If checksum is not present, add it to the checksum file along with its associated doc_id
        glb_doc_id += 1
        checksum_data[checksum] = glb_doc_id
        urlfile_data[glb_doc_id] = url  # Store the URL in the urlfile_data

        # with open(checksum_file, "w") as file:
        #     json.dump(checksum_data, file, indent=2)
        # with open(urlfile, "w") as url_file:
        #     json.dump(urlfile_data, url_file, indent=2)
        return glb_doc_id


# Example usage:
print("Trying Forward Index")
count = 0
forward_index_file = f"{output_folder}\\forward_index_{count}.json"
try:
    # Read existing forward index data
    with open(forward_index_file, "r") as file:
        forward_index_data = json.load(file)

except FileNotFoundError:
    forward_index_data = []
# Iterate through each JSON file
for json_file in json_files:
    if documents_read >= max_documents:
        break
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

        # print(f"{documents_read}.{article['title']}")

        document_title = article["url"]
        checksum = hashlib.sha256(document_title.encode("UTF-8")).hexdigest()
        doc_id = get_doc_id_from_checksum(checksum,document_title)

        # Check if the doc_id already exists
        if doc_id == 0:
            print("DocID already exists")
            continue

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
        forward_index_data.append(
            {
                "di": doc_id,
                "st": tokens_dict[i],
                "tf": token_frequency,
                "tp": token_positions,
                "u": article["url"],
                "d": article["date"],
                "p": article["published_utc"],
                "c": article["collection_utc"],
            }
        )

        documents_read += 1

try:
    # Write the forward index to a JSON file
    with open(forward_index_file, "w") as file:
        json.dump(forward_index_data, file, indent=2)
    with open(checksum_file, "w") as file:
        json.dump(checksum_data, file, indent=2)
    with open(urlfile, "w") as url_file:
        json.dump(urlfile_data, url_file, indent=2)
except Exception as e:
    print(f"Error writing to the file: {e}")



print("Forward index Stored ")
