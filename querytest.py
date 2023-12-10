import json
import os
from nltk.stem import SnowballStemmer

# Path to the folder for inverted index files
inverted_index_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"

# Path to the DocURL file
docurl_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\docURL.json"  # Replace with the actual path

# Initialize the SnowballStemmer
stemmer = SnowballStemmer(language="english")

# Function to search for a word in the inverted index
def search_inverted_index(query_word):
    # Stem the query word
    stemmed_query_word = stemmer.stem(query_word)

    # Get the first character of the stemmed query word
    first_char = stemmed_query_word[0].lower() if stemmed_query_word else None

    # Ensure first_char is not None (empty or not a string)
    if first_char is not None:
        # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
        if '0' <= first_char <= '9':
            barrel = first_char
        elif 'a' <= first_char <= 'z':
            barrel = first_char
        else:
            barrel = 'other'

    # Load the inverted index for the specific barrel
    inverted_index_file_path = os.path.join(inverted_index_folder, f"inverted_index_{barrel}.json")
    print(f"Inverted Index for '{barrel}':")
    #load the DocURL file

    try:
        with open(inverted_index_file_path, "r") as file:
            inverted_index = json.load(file)
    except FileNotFoundError:
        print(f"Inverted index file for '{query_word}' not found.")
        return


     # Load the DocURL file
    try:
        with open(docurl_file_path, "r") as docurl_file:
            docurls = json.load(docurl_file)
    except FileNotFoundError:
        print("DocURL file not found.")
        docurls = {}  # Empty dictionary if file not found

    # Check if the stemmed query word is in the inverted index
    if stemmed_query_word in inverted_index:
        # Get the documents, positions, and frequency information for the word
        documents = inverted_index[stemmed_query_word]["documents"]
        positions = inverted_index[stemmed_query_word]["positions"]
        frequency = inverted_index[stemmed_query_word]["frequency"]

        # print(documents)
        # print(positions)
        # Output the results
        print(f"Stemmed Query Word: {stemmed_query_word}")
        print("Documents:")
        for doc_id in documents:
            print(f"  Document ID: {doc_id}")

            # if str(doc_id) in positions:
            #     print(f"    Positions: {positions[str(doc_id)]}")
            # else:
            #     print("    Positions: Not available")
            # if str(doc_id) in frequency:
            #     print(f"    Frequency: {frequency[str(doc_id)]}")
            # else:
            #     print("Frequency not available")
            
            if str(doc_id) in docurls:
                print(f"URL : {docurls[str(doc_id)]}")
            print("")


    else:
        print(f"Stemmed Query Word '{stemmed_query_word}' not found in the inverted index.")

# Example usage
query_word = input("Enter a word to search: ")
search_inverted_index(query_word)
