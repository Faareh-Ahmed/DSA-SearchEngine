import json
import os
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import time

# Path to the folder containing inverted index files in form of Barrels
inverted_index_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"

# Path to the DocURL file
docurl_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\docURL.json"  

# Initializing the SnowballStemmer
stemmer = SnowballStemmer(language="english")

# nltk is a library to process natural language data for understandable by computer
# We can use many methods like tokenizer and stemmer to clean the data and 
# reduce it to its root form
from nltk.tokenize import word_tokenize, sent_tokenize

# Get the set of English stop words
stop_words = set(stopwords.words("english"))

common_docs={}
rank=[]

 # Load the DocURL file where URL are stored corresponding to each docID
try:
    with open(docurl_file_path, "r") as docurl_file:
        docurls = json.load(docurl_file)
except FileNotFoundError:
    print("DocURL file not found.")
    docurls = {}  # Empty dictionary if file not found


# Function to search for a word in the inverted index
def search_inverted_index(query_word):

    start_time = time.time()

    common_docs = {}
    #tokenizing the Query that the user Entered in the search bar
    tokens = [word_tokenize(query_word)]


    # Remove stop words and punctuation, and stem each token in the tokens
    stemmed_words = [
        stemmer.stem(token)
        for sentence_tokens in tokens
        for token in sentence_tokens
        if token.isalnum() and token.lower() not in stop_words
    ]


    # Now we will Loop through each of the words individually
    for word in stemmed_words:

        stemmed_query_word = stemmer.stem(query_word)
        print(word)

        # Selecting the correct barrel in which that word exists
        # Get the first character of the stemmed query word
        first_char = word[0].lower() if word else None
        print(first_char)
        # Ensure first_char is not None (empty or not a string)
        if first_char is not None:
            # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
            if '0' <= first_char <= '9':
                barrel = first_char

            elif 'a' <= first_char <= 'z':
                if(len(word)<2):
                    second_char=first_char
                    third_char=first_char
                    char=str(first_char+second_char+third_char)
                    barrel=char
                else:
                    second_char = str(word)[1].lower() if str(word) else None
                    if('0' <= second_char <= '9'):
                        char = str(first_char+second_char)
                        barrel=char
                    # Check if the second_char is not a lowercase letter or a digit
                    elif('a' <= second_char <= 'z'):
                        if(len(word)<3):
                            third_char=second_char
                            char=str(first_char+second_char+third_char)
                            barrel=char
                        else:
                            third_char = str(word)[2].lower() if str(word) else None
                            
                            if('0' <= third_char <= '9'):
                                third_char=second_char
                                char=str(first_char+second_char+third_char)
                                barrel=char
                            elif('a' <= third_char <= 'z'):
                                char=str(first_char+second_char+third_char)
                                barrel = char
                            else:
                                barrel='other'
                    else:
                        barrel = 'other'
            else:
                barrel = 'other'

        # Getting the correct path for that specific Barrel
        inverted_index_file_path = os.path.join(inverted_index_folder, f"inverted_index_{barrel}.json")
        print(f"Inverted Index for '{barrel}':")

        # Load the inverted index for that specific barrel
        try:
            with open(inverted_index_file_path, "r") as file:
                inverted_index = json.load(file)
        except FileNotFoundError:
            print(f"Inverted index file for '{query_word}' not found.")
            return

        print("File Barrel Loaded Successfully")
        # # Load the DocURL file
        try:
            with open(docurl_file_path, "r") as docurl_file:
                docurls = json.load(docurl_file)
        except FileNotFoundError:
            print("DocURL file not found.")
            docurls = {}  # Empty dictionary if file not found

        # Check if the query word is in the inverted index
        if word in inverted_index:
        
            # Retrieve the List of docID where the word occured
            documents=list(inverted_index[word].keys())

            # Loop through each Document
            for document in documents:
                # Check if that Document is already present in the common Documents
                # then update its rank by adding the current word rank
                # If that Document is not present in the common documents then
                # Add it into the common document with its rank 
                if document not in common_docs:
                    common_docs[document]=inverted_index[word][document]["r"]
                else:
                    common_docs[document]=common_docs[document]+inverted_index[word][document]["r"]

             # If common_docs is empty, initialize it with the document IDs from the first word
            if not common_docs:
                common_docs.update(documents)
            else:
                # Intersect the current document_ids with common_document_ids
                common_docs = {doc_id: common_docs[doc_id] for doc_id in common_docs if doc_id in documents}


            for doc_id in common_docs.keys():
                rank.append(common_docs[doc_id])

        else:
            print(f"Stemmed Query Word '{word}' not found in the inverted index.")
    # Sort documents by rank
    sorted_documents = sorted(rank, reverse=True)
    # Sort documents by rank
    sorted_documents = sorted(common_docs.keys(), key=lambda doc_id: common_docs[doc_id], reverse=True)
    
     # Measure the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    print("sorted Doc:\n",sorted_documents)

    # Select the top 10 documents
    top_documents = sorted_documents[:20]
    print("Top document:\n",top_documents)

    document_data = {}

    # Output the results
    print(f"Stemmed Query Word: {query_word}")
    for doc_id in top_documents:
        if str(doc_id) in docurls:
            document_data[doc_id] = docurls[str(doc_id)]
    
    print(f"Code took {elapsed_time} to Run the Query")

    # Data will be used in backend.py
    return document_data

