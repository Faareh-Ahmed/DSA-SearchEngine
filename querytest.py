import json
import os
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Path to the folder for inverted index files
inverted_index_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"

# Path to the DocURL file
docurl_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\docURL.json"  # Replace with the actual path

# Initialize the SnowballStemmer
stemmer = SnowballStemmer(language="english")

# nltk is a library to process natural language data for understandable by computer
from nltk.tokenize import word_tokenize, sent_tokenize

# Get the set of English stop words
stop_words = set(stopwords.words("english"))

common_docs={}
rank=[]

 # Load the DocURL file
try:
    with open(docurl_file_path, "r") as docurl_file:
        docurls = json.load(docurl_file)
except FileNotFoundError:
    print("DocURL file not found.")
    docurls = {}  # Empty dictionary if file not found


# Function to search for a word in the inverted index
def search_inverted_index(query_word):

        #tokenizing the combined words
    tokens = [word_tokenize(query_word)]


# Remove stop words and punctuation, and stem the remaining words
    stemmed_words = [
        stemmer.stem(token)
        for sentence_tokens in tokens
        for token in sentence_tokens
        if token.isalnum() and token.lower() not in stop_words
    ]


    # flat_tokens = [token for sentence_tokens in tokens for token in sentence_tokens]

    # # Remove special characters, dots, etc.
    # query_tokenized = [word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

    # # Convert to lowercase
    # query_tokenized = [word.lower() for word in query_tokenized]

    # # Remove stop words
    # clean_query = [word for word in query_tokenized if word not in stop_words]

    # # Lemmatization
    # clean_query = [lemmatizer.lemmatize(word) for word in clean_query]


    for word in stemmed_words:

        # stemmed_query_word = stemmer.stem(query_word)
        print(word)

        # Get the first character of the stemmed query word
        first_char = word[0].lower() if word else None
        print(first_char)
    # Ensure first_char is not None (empty or not a string)
        # Ensure first_char is not None (empty or not a string)
        if first_char is not None:
            # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
            if '0' <= first_char <= '9':
                barrel = first_char

            elif 'a' <= first_char <= 'z':
                # print(token)
                if(len(word)<2):
                    second_char=first_char
                    char=str(first_char+second_char)
                    barrel=char
                else:
                    second_char = str(word)[1].lower() if str(word) else None
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
        # # Load the DocURL file
        # try:
        #     with open(docurl_file_path, "r") as docurl_file:
        #         docurls = json.load(docurl_file)
        # except FileNotFoundError:
        #     print("DocURL file not found.")
        #     docurls = {}  # Empty dictionary if file not found

        # Check if the stemmed query word is in the inverted index
        if word in inverted_index:
        

            documents=list(inverted_index[word].keys())
            # print(documents)

            for document in documents:
                if document not in common_docs:
                    common_docs[document]=inverted_index[word][document]["rank"]
                else:
                    common_docs[document]=common_docs[document]+inverted_index[word][document]["rank"]

             # If common_docs is empty, initialize it with the document IDs from the first word
            # if not common_docs:
            #     common_docs.update(documents)
            # else:
            #     # Intersect the current document_ids with common_document_ids
            #     common_docs.intersection_update(documents)

            # print(documents)
            # print("Common DOc:\n",common_docs)

            print("ooo\n")
            for doc_id in common_docs.keys():
                # print(doc_id)
                rank.append(common_docs[doc_id])
            # print(rank)

        else:
            print(f"Stemmed Query Word '{word}' not found in the inverted index.")
    # Sort documents by rank
    # sorted_documents = sorted(rank, reverse=True)
    # Sort documents by rank
    sorted_documents = sorted(common_docs.keys(), key=lambda doc_id: common_docs[doc_id], reverse=True)
    
    # print("sorted Doc:\n",sorted_documents)

    # Select the top 10 documents
    top_documents = sorted_documents[:10]
    print("Top document:\n",top_documents)

    # Output the results
    print(f"Stemmed Query Word: {query_word}")
    print("Top 10 Documents:")
    for doc_id in top_documents:
        # print(f"  Document ID: {doc_id}")

        if str(doc_id) in docurls:
            print(f"  URL : {docurls[str(doc_id)]}")
        print("")




# Example usage
query_word = input("Enter a word to search: ")
search_inverted_index(query_word)
