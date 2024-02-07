# import json

# def save_inverted_index_file(inverted_index):
#     # Write inverted index to a JSON file
#     with open('C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files\\inverted_index.json', 'w') as json_file:
#         json.dump(inverted_index, json_file)

# # Function to load the forward index file
# def load_forward_index():
#     forward_index_path = 'C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\forwardindex.json'
#     try:
#         with open(forward_index_path, 'r') as f:
#             data = json.load(f)
#             return data
#     except FileNotFoundError:
#         print("No file for forward index exists..!!")


# # Function to load the inverted index file if already exists, else creates a dictionary for inverted index
# def load_inverted_index():
#     file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files\\inverted_index.json"
#     try:
#         with open(file_path, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}

# # This function creates the structure to be inserted into the inverted index file
# def create_inverted_index(forward_index):
#     inverted_index = load_inverted_index()

#     # Iterating through each document in the forward index
#     for doc_id, document in forward_index.items():
#         words = document.get("words", [])
#         doc_id = str(doc_id)

#         # Getting the information for each word present in a particular document
#         for word in words:
            
#             word_id = str(word.get("word_id"))
#             frequency = word.get("fr")
#             positions = word.get("ps")

#             # If the inverted index file is empty, initialize it with a key named word_ID
#             # if "word_ID" not in inverted_index:
#             #     inverted_index["word_ID"] = {}

#             # If word is not present in the inverted index, create its key
#             if word_id not in inverted_index:
#                 inverted_index[word_id] = {}

#             # If a document id for a given word is not present, add the details for the word in the document
#             if doc_id not in inverted_index[word_id]:
#                 word_info = {
#                     "fr": frequency,
#                     "ps": positions
#                 }

#                 # Add the details of the word for that document in the inverted index of the word
#                 inverted_index[word_id][doc_id] = word_info

#     # Save the updated inverted index dictionary in a json file
#     save_inverted_index_file(inverted_index)

#     print("Inverted index generated and saved as 'inverted_index.json'")

# # Main function to load the forward index and then generate the inverted index
# forward_index = load_forward_index()
# create_inverted_index(forward_index)
