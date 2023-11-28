# Testing the inverted index to fetch the DocID which has the farthest position of that word 



# import json

# def farthest_position_for_word(word, inverted_index_file):
#     with open(inverted_index_file, 'r') as file:

#         inverted_index = json.load(file)

#     if word in inverted_index:
#         # Word found in the inverted index
#         word_info = inverted_index[word]['positions']

#         farthest_doc_id = None
#         farthest_position = -1  # Initialize to a value lower than any possible position

#         for doc_id, positions in word_info.items():
#             max_position = max(map(int, positions))
#             if max_position > farthest_position:
#                 farthest_doc_id = doc_id
#                 farthest_position = max_position

#         if farthest_doc_id is not None:
#             return farthest_doc_id, farthest_position
#         else:
#             # This should not happen if positions are properly stored
#             return None
#     else:
#         # Word not found
#         return None

# # Example usage
# word = "elit"
# inverted_index_file = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\codeSpace\\inverted_index_test_file.json"
# result = farthest_position_for_word(word, inverted_index_file)

# if result:
#     doc_id, farthest_position = result
#     print(f"Word: {word}")
#     print(f"Farthest Position for Document ID {doc_id}: {farthest_position}")
# else:
#     print(f"Word '{word}' not found in the inverted index.")




# Testing the inverted index to fetch the total docID's associated with that word 


import json

def get_all_doc_ids_for_word(word, inverted_index_file):
    with open(inverted_index_file, 'r') as file:
        inverted_index = json.load(file)

    if word in inverted_index:
        # Word found in the inverted index
        word_info = inverted_index[word]['documents']
        
        if word_info:
            doc_ids = list(word_info.keys())
            return doc_ids
        else:
            # No documents associated with the word
            return []
    else:
        # Word not found
        return []

# Example usage
word = "alleg"
inverted_index_file = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\codeSpace\\inverted_index_test_file.json"
doc_ids = get_all_doc_ids_for_word(word, inverted_index_file)

if doc_ids:
    print(f"Word: {word}")
    print(f"Total Document IDs associated with the word: {len(doc_ids)}")
    print(f"Document IDs: {doc_ids}")
else:
    print(f"Word '{word}' not found in the inverted index.")


