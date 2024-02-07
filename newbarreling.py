# import json
# import os


# # Function to load the forward index file
# def load_forward_index():
#     forward_index_path = 'C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\forwardindex.json'
#     try:
#         with open(forward_index_path, 'r') as f:
#             data = json.load(f)
#             print("Forward Index Loaded")
#             return data
#     except FileNotFoundError:
#         print("No file for forward index exists..!!")

# # Function to save each barrel data in the corresponding barrel file
# def save_inverted_index_file(index,path):
#    # Write inverted index to a JSON file
#     with open(path, 'w') as json_file:
#         json.dump(index, json_file)

# # Function that calls each barrel file one by one and then saves them
# def save_all_inverted_index_files(inverted_indices, inverted_index_file_paths):
#     for index, path in zip(inverted_indices, inverted_index_file_paths):
#         save_inverted_index_file(index, path)

# # Function to load the inverted index file if already exists, else creates a dictionary for inverted index
# def load_inverted_index(path):
#     try:
#         with open(path, 'r') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return {}

# # Function to create the structure to be inserted into the inverted index file
# def create_inverted_index(forward_index, inverted_indices, number_of_inverted_index_barrels,inverted_index_file_paths):
#     count=0
#     for doc_id, document in forward_index.items():
#         if count==20000:
#             print("20K reached")
#             save_all_inverted_index_files(inverted_indices, inverted_index_file_paths)
#             count=0

#         words = document.get("words", [])
#         doc_id = str(doc_id)

#         for word in words:
#             word_id = str(word.get("word_id"))
#             int_word_id = int(word_id)
#             word_id = str(word_id)

#             frequency = word.get("fr")
#             positions = word.get("ps")

#             barrel = int_word_id % number_of_inverted_index_barrels

#             if word_id is not None:
#                 # if "word_ID" not in inverted_indices[barrel]:
#                 #     inverted_indices[barrel]["word_ID"] = {}
#                 if word_id not in inverted_indices[barrel]:
#                     inverted_indices[barrel][word_id] = {}
#                 if doc_id not in inverted_indices[barrel][word_id]:
#                     word_info = {"fr": frequency, "ps": positions}
#                     inverted_indices[barrel][word_id][doc_id] = word_info
#         count+=1

# # Main function to load the forward index and then generate the inverted index
# def generate_inverted_index():
#     number_of_inverted_index_barrels = 2000
#     print("Started Loading Barrels")
#     inverted_index_file_paths = [
#         f'C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files\\inverted_index.json_{i}.json' for i in range(1, number_of_inverted_index_barrels + 1)
#     ]
#     inverted_indices = [load_inverted_index(path) for path in inverted_index_file_paths]
#     print("Barrels Loaded")
#     # json_forward_index_dir = "./Forward_Index/Forward_index_files"
#     # json_forward_index_files = [file for file in os.listdir(json_forward_index_dir) if file.endswith(".json")]

#     # for file_path in json_forward_index_files:
#     forward_index = load_forward_index()
#     create_inverted_index(forward_index, inverted_indices, number_of_inverted_index_barrels,inverted_index_file_paths)

#     save_all_inverted_index_files(inverted_indices, inverted_index_file_paths)

# # Call the main function to generate the inverted index
# generate_inverted_index()
