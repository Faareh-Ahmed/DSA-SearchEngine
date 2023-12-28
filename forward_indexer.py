import json
import hashlib
import nltk
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import os
import sys

from inverted_indexer import inverted_indexer

nltk.download("stopwords")
nltk.download("punkt")

# nltk is a library to process natural language data for understandable by computer
# We can use many methods like tokenizer and stemmer to clean the data and 
#  reduce it to its root form
from nltk.tokenize import word_tokenize, sent_tokenize

# Initializing the SnowballStemmer
stemmer = SnowballStemmer(language="english")

# Geting the set of English stop words from the library and storing in a data structure
stop_words = set(stopwords.words("english"))

# Here we are taking the path to the JSON file folder from the backend as a argument
# In order to process it to make its Forward index
try:
    folder_path = sys.argv[1]
except IndexError:
    folder_path = "default_folder_path"
    

# List all files in the specified folder of JSON files
json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]


# Initializing a dictionary to store tokens(words)
tokens_dict = {}
glb_doc_id = 0 #variable to store the DocID of the current document being processed


# Load checksum and docURL File if it exists
checksum_file = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\checksum.json"
urlfile="C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\docURL.json"
urlfile_data ={}
checksum_data = {}

# check if the file exists. We checked only for checksun File because both the files
# are created simultaneously in the code
if os.path.exists(checksum_file):
    # If it exists, load the existing data
    with open(checksum_file, "r") as file:
        checksum_data = json.load(file)

    with open(urlfile,"r") as file:
        urlfile_data=json.load(file)

    # Find the maximum DocID in the CheckSum file which will be present at the last of the file
    # Assign that DocID + 1 to the variable 
    max_existing_doc_id = max(checksum_data.values(), default=0)
    documents_read=max_existing_doc_id
    glb_doc_id = max_existing_doc_id + 1
else:
    # If it doesn't exist, initialize with an empty dictionary
    with open(checksum_file, "w") as file:
        json.dump({}, file)




def get_doc_id_from_checksum(checksum,url):
    global glb_doc_id  # Declare glb_doc_id as a global variable

    # If checksum is already present then it means that Document has already been processed
    if checksum in checksum_data:
        return 0
    else:
        # If checksum is not present, add it to the checksum file along with its associated doc_id
        glb_doc_id += 1
        checksum_data[checksum] = glb_doc_id
        # Store the URL in the urlfile_data corresponding to that DocID
        urlfile_data[glb_doc_id] = url  

        return glb_doc_id


print("Trying Forward Index")

forward_index_data = []
# Iterate through each JSON file in the Folder
for json_file in json_files:

    # Construct the full path to the JSON file
    json_file_path = os.path.join(folder_path, json_file)

    # Read the JSON data from the file
    with open(json_file_path, "r") as file:
        json_data = file.read()

    # Load the JSON data 
    data = json.loads(json_data)

    for i, article in enumerate(data, 1):

        # Retrieving the Doc url and perform hashing to check if this document 
        # has previously been processed or not
        document_title = article["url"]
        checksum = hashlib.sha256(document_title.encode("UTF-8")).hexdigest()
        doc_id = get_doc_id_from_checksum(checksum,document_title)

        # If the doc_id already exists then Continue to the next Document
        if doc_id == 0:
            print("DocID already exists")
            continue

        # If Doc_id is not already present then store the desired info 
        # of this doc in Forward index
        content = article["title"] + " " + article["content"]
        # Separate each word from the content
        tokens = [word_tokenize(content)]

        # Remove stop words and punctuation, and stem each token in the tokens
        stemmed_words = [
            stemmer.stem(token)
            for sentence_tokens in tokens
            for token in sentence_tokens
            if token.isalnum() and token.lower() not in stop_words
        ]

        # Store tokens in the dictionary data structure
        tokens_dict[i] = stemmed_words

        # Flatten the list of lists (tokens)
        flat_tokens = [token for sentence_tokens in tokens for token in sentence_tokens]

        # Calculate each token frequency in the Document using stemmed tokens
        token_frequency = {
            token: stemmed_words.count(token) for token in set(stemmed_words)
        }

        # Calculate token positions 
        # First we make the list of all the unique words that appear using the set()
        # Then we iterate through each of these unique words. For each unique word 
        # we look at the document and find all the positions where that word appeared
        # and write it for that word (List of all Positions in the document)
        token_positions = {
            token: [i + 1 for i, word in enumerate(stemmed_words) if word == token]
            for token in set(stemmed_words)
        }

        # Append the data in the forward Index Data Structure
        forward_index_data.append(
            {
                "di": doc_id,
                "st": tokens_dict[i],
                "tf": token_frequency,
                "tp": token_positions,
                "u": article["url"],
                "d": article["date"],
                "pu": article["published_utc"],
                "cu": article["collection_utc"],
            }
        )

# After all the files JSON have been processed and their Forward Index data structure is made
# we then write the updated checksum and the DocURL 
try:

    with open(checksum_file, "w") as file: 
        json.dump(checksum_data, file)
    with open(urlfile, "w") as url_file: 
        json.dump(urlfile_data, url_file)
    
except Exception as e:
    print(f"Error writing to the file: {e}")


# Now pass this Forward Index Data Structure in the Inverted Indexer function 
# to make its inverted index
print("Forward index Stored ")
inverted_indexer(forward_index_data)

