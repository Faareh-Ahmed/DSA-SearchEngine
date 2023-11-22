import json
import nltk
nltk.download('punkt')
# ************************** Tokenizing the content of Document **********************

from nltk.tokenize import word_tokenize, sent_tokenize

json_file_path = 'C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\newsdata\\abcnews.json'

# Read the JSON data from the file
with open(json_file_path, 'r') as file:
    json_data = file.read()

# Parse the JSON data
data = json.loads(json_data)
# Initializing a dictionary to store tokens
tokens_dict = {}

# Extract and store content and tokens of the first 10 documents
for i, article in enumerate(data[:10], 1):
    content = article['content']

    # Tokenize the content
    sentences = sent_tokenize(content)
    tokens = [word_tokenize(sentence) for sentence in sentences]

    # Store tokens in the dictionary
    tokens_dict[i] = tokens

# Print the dictionary
print("\nTokens Dictionary:")
for doc_no, doc_tokens in tokens_dict.items():
    print(f"Document {doc_no}: {doc_tokens}")