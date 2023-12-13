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
    print(stemmed_query_word)

    # Get the first character of the stemmed query word
    first_char = stemmed_query_word[0].lower() if stemmed_query_word else None
    print(first_char)
   # Ensure first_char is not None (empty or not a string)
    # Ensure first_char is not None (empty or not a string)
    if first_char is not None:
        # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
        if '0' <= first_char <= '9':
            barrel = first_char

        elif 'a' <= first_char <= 'z':
            # print(token)
            if(len(stemmed_query_word)<2):
                second_char=first_char
                char=str(first_char+second_char)
                barrel=char
            else:
                second_char = str(stemmed_query_word)[1].lower() if str(stemmed_query_word) else None
                # Check if the second_char is not a lowercase letter or a digit
                if('0' <= second_char <= '9') or ('a' <= second_char <= 'z'):
                    char=str(first_char+second_char)
                    barrel = char
                else:
                    barrel = 'other'
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

    print("File Barrel Loaded Successfully")
     # Load the DocURL file
    try:
        with open(docurl_file_path, "r") as docurl_file:
            docurls = json.load(docurl_file)
    except FileNotFoundError:
        print("DocURL file not found.")
        docurls = {}  # Empty dictionary if file not found

    # Check if the stemmed query word is in the inverted index
    if stemmed_query_word in inverted_index:
     

        documents=list(inverted_index[stemmed_query_word].keys())

        # print(documents)
        print("ooo\n")
        rank=[]
        for doc_id in documents:
            # print(doc_id)
            rank.append(inverted_index[stemmed_query_word][ doc_id ]["rank"])
        # print(rank)

        # Sort documents by rank
        sorted_documents = sorted(documents, key=lambda doc_id: inverted_index[stemmed_query_word][doc_id]["rank"], reverse=True)

        # Select the top 10 documents
        top_documents = sorted_documents[:10]

        # Output the results
        print(f"Stemmed Query Word: {stemmed_query_word}")
        print("Top 10 Documents:")
        for doc_id in top_documents:
            # print(f"  Document ID: {doc_id}")

            if str(doc_id) in docurls:
                print(f"  URL : {docurls[str(doc_id)]}")
            print("")



    else:
        print(f"Stemmed Query Word '{stemmed_query_word}' not found in the inverted index.")

# Example usage
query_word = input("Enter a word to search: ")
search_inverted_index(query_word)
