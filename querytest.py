# import json
# import os
# from nltk.stem import SnowballStemmer
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import time

# # Path to the folder containing inverted index files in form of Barrels
# inverted_index_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"

# # Path to the DocURL file
# docurl_file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\docURL.json"  

# # Initializing the SnowballStemmer
# stemmer = SnowballStemmer(language="english")

# # nltk is a library to process natural language data for understandable by computer
# # We can use many methods like tokenizer and stemmer to clean the data and 
# # reduce it to its root form
# from nltk.tokenize import word_tokenize, sent_tokenize

# # Get the set of English stop words
# stop_words = set(stopwords.words("english"))

# common_docs={}
# rank=[]

#  # Load the DocURL file where URL are stored corresponding to each docID
# try:
#     with open(docurl_file_path, "r") as docurl_file:
#         docurls = json.load(docurl_file)
# except FileNotFoundError:
#     print("DocURL file not found.")
#     docurls = {}  # Empty dictionary if file not found


# # Function to search for a word in the inverted index
# def search_inverted_index(query_word):

#     start_time = time.time()

#     common_docs = {}
#     #tokenizing the Query that the user Entered in the search bar
#     tokens = [word_tokenize(query_word)]


#     # Remove stop words and punctuation, and stem each token in the tokens
#     stemmed_words = [
#         stemmer.stem(token)
#         for sentence_tokens in tokens
#         for token in sentence_tokens
#         if token.isalnum() and token.lower() not in stop_words
#     ]


#     # Now we will Loop through each of the words individually
#     for word in stemmed_words:

#         stemmed_query_word = stemmer.stem(query_word)
#         print(word)

#         # Selecting the correct barrel in which that word exists
#         # Get the first character of the stemmed query word
#         first_char = word[0].lower() if word else None
#         print(first_char)
#         # Ensure first_char is not None (empty or not a string)
#         if first_char is not None:
#             # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
#             if '0' <= first_char <= '9':
#                 barrel = first_char

#             elif 'a' <= first_char <= 'z':
#                 if(len(word)<2):
#                     second_char=first_char
#                     third_char=first_char
#                     char=str(first_char+second_char+third_char)
#                     barrel=char
#                 else:
#                     second_char = str(word)[1].lower() if str(word) else None
#                     if('0' <= second_char <= '9'):
#                         char = str(first_char+second_char)
#                         barrel=char
#                     # Check if the second_char is not a lowercase letter or a digit
#                     elif('a' <= second_char <= 'z'):
#                         if(len(word)<3):
#                             third_char=second_char
#                             char=str(first_char+second_char+third_char)
#                             barrel=char
#                         else:
#                             third_char = str(word)[2].lower() if str(word) else None
                            
#                             if('0' <= third_char <= '9'):
#                                 third_char=second_char
#                                 char=str(first_char+second_char+third_char)
#                                 barrel=char
#                             elif('a' <= third_char <= 'z'):
#                                 char=str(first_char+second_char+third_char)
#                                 barrel = char
#                             else:
#                                 barrel='other'
#                     else:
#                         barrel = 'other'
#             else:
#                 barrel = 'other'

#         # Getting the correct path for that specific Barrel
#         inverted_index_file_path = os.path.join(inverted_index_folder, f"inverted_index_{barrel}.json")
#         print(f"Inverted Index for '{barrel}':")

#         # Load the inverted index for that specific barrel
#         try:
#             with open(inverted_index_file_path, "r") as file:
#                 inverted_index = json.load(file)
#         except FileNotFoundError:
#             print(f"Inverted index file for '{query_word}' not found.")
#             return

#         print("File Barrel Loaded Successfully")
#         # # Load the DocURL file
#         try:
#             with open(docurl_file_path, "r") as docurl_file:
#                 docurls = json.load(docurl_file)
#         except FileNotFoundError:
#             print("DocURL file not found.")
#             docurls = {}  # Empty dictionary if file not found

#         # Check if the query word is in the inverted index
#         if word in inverted_index:
        
#             # Retrieve the List of docID where the word occured
#             documents=list(inverted_index[word].keys())

#             # Loop through each Document
#             for document in documents:
#                 # Check if that Document is already present in the common Documents
#                 # then update its rank by adding the current word rank
#                 # If that Document is not present in the common documents then
#                 # Add it into the common document with its rank 
#                 if document not in common_docs:
#                     common_docs[document]=inverted_index[word][document]["r"]
#                 else:
#                     common_docs[document]=common_docs[document]+inverted_index[word][document]["r"]

#              # If common_docs is empty, initialize it with the document IDs from the first word
#             if not common_docs:
#                 common_docs.update(documents)
#             else:
#                 # Intersect the current document_ids with common_document_ids
#                 common_docs = {doc_id: common_docs[doc_id] for doc_id in common_docs if doc_id in documents}


#             for doc_id in common_docs.keys():
#                 rank.append(common_docs[doc_id])

#         else:
#             print(f"Stemmed Query Word '{word}' not found in the inverted index.")
#     # Sort documents by rank
#     sorted_documents = sorted(rank, reverse=True)
#     # Sort documents by rank
#     sorted_documents = sorted(common_docs.keys(), key=lambda doc_id: common_docs[doc_id], reverse=True)
    
#      # Measure the end time
#     end_time = time.time()

#     # Calculate the elapsed time
#     elapsed_time = end_time - start_time

#     print("sorted Doc:\n",sorted_documents)

#     # Select the top 10 documents
#     top_documents = sorted_documents[:20]
#     print("Top document:\n",top_documents)

#     document_data = {}

#     # Output the results
#     print(f"Stemmed Query Word: {query_word}")
#     for doc_id in top_documents:
#         if str(doc_id) in docurls:
#             document_data[doc_id] = docurls[str(doc_id)]
    
#     print(f"Code took {elapsed_time} to Run the Query")

#     # Data will be used in backend.py
#     return document_data




















# New querytest.py

















import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import heapq
import sys
import time
from nltk.stem import SnowballStemmer


#function to load the lexicon for finding the word id corresponding to the searched word
def load_Lexicon():
    file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\lexicon.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None  

#function to load the document index file for finding the urls of documents corresponding to the searched word
def load_documentIndex():
    file_path = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_forward_index_files\\docURL.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

#function to load the file for finding the dates of documents published corresponding to the searched word
def load_document_date_file():
    file_path = "Forward_Index/docId_date_mapping.json"
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

#function to load the relevant barrel into ram for finding the document ids and data corresponding to the searched word
def load_inverted_index_barrel(path):
    try: 
        with open(path, "r") as file:
            return json.load(file)
    except (FileExistsError, FileNotFoundError):
        return None

'''
function for getting all the documents along with their ids and data
for those documents that contain the searched word
'''
def get_documents(word_id, word_data_in_barrel):
    if str(word_id) in word_data_in_barrel:
        word_data = word_data_in_barrel[str(word_id)]
        return word_data
    else:
        return {}



def search_inverted_index(query):

    #setting up the english stop words from the NLTK
    stop_words = set(stopwords.words("english"))

    #object for the lemmatizer class
    stemmer = SnowballStemmer(language="english")

    #object for loading the lexicon dictionary 
    lexicon_dictionary = load_Lexicon()

    #object for loading the file that contains the documents are their urls
    document_urls = load_documentIndex()

    #dictionary for storing the data of each barrel that needs to be loaded for getting the word data
    loaded_inverted_indices = {}

    #getting the searched input query from the user
    # query = input("Enter the query to search: ")

    #starting the timer to calculate the execution time
    start_time = time.time()

    #tokenizing the combined words
    query_tokenized = word_tokenize(query)

    #remove special characters, dots, etc.
    query_tokenized = [word for word in query_tokenized if re.match("^[a-zA-Z0-9_]*$", word)]

    #convert to lowercase
    query_tokenized = [word.lower() for word in query_tokenized]

    #remove stop words
    clean_query = [word for word in query_tokenized if word not in stop_words]

    #lemmatization
    clean_query = [stemmer.stem(word) for word in clean_query]

    document_score = {}
    document_data={}

    for word in clean_query:
        try: 
            word_id = lexicon_dictionary[word]
            print("Word ID: ",word_id)
        except:
            print(f'{word} is not present in any document!')
            continue
        
        #getting the relevant barrel id that contains the searched word
        barrel_id = word_id % 2000
        print("Barrel:\n",barrel_id)

        #check if the inverted index for this barrel is already loaded, then do not reload
        if barrel_id in loaded_inverted_indices:
            word_data_in_barrel = loaded_inverted_indices[barrel_id]
        else:
            #load the inverted index for this barrel
            word_data_in_barrel = load_inverted_index_barrel(f'C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files\\inverted_index.json_{barrel_id+1}.json')
            loaded_inverted_indices[barrel_id] = word_data_in_barrel

            print("Barrel:\n",word_data_in_barrel)
        #getting the information for all the documents that have a particular word searched
        documents = get_documents(word_id, word_data_in_barrel)
        print("Documents containg the word : ",documents)
        #dictionary that will store the documents along with their scores for ranking 
        # document_score = {}
        #scoring the documents based on the number of words they contain out of the number of searched words
        for document in documents.keys():

            '''
            if document appears first time, then give it a score one
            this means that the document so far has only one word in it out of the 
            total number of words searched
            '''
            if document not in document_score:
                document_score[document] = {"count": 1, "values": [documents[document]]}
            else:
                '''
                increasing the score of the documents by one everytime
                they appear again, this means they have more words in them
                that have been searched, so they will be scored higher
                '''
                document_score[document]["count"] += 1
                document_score[document]["values"].append(documents[document])

    #condition to check if no document appears, this means that the searched query has no relevant articles available
    if(len(document_score)== 0):
        print("The searched query is not present in any document!\nPlease search for other words..!!")
        return {}

    #getting the max scored document
    max_count_document = max(document_score.items(), key=lambda x: x[1]["count"])

    #getting the score of the max scored document
    max_count = max_count_document[1]["count"]
    print(max_count)

    #variable that keeps track of the number of documents that have been displayed
    documents_shown = 0

    #if the number of documents shown exceed 30 or no more documents are left, then stop
    while(documents_shown < 30 and max_count >=1):

        #a list that will store the documents of same score and then will be used for sorting
        priority_queue = []

        #loop to iterate over each document that has been retreived
        for doc in document_score.items():
            if doc[1]["count"] == max_count:
                getting_frequencies = doc[1]['values']
                frequency = 0

                '''
                summing up the frequencies of each document that has the same
                number of words out of the number of words searched, 
                this is being used for ranking
                '''
                for value in getting_frequencies:
                    frequency += value['fr']

                #pushing the document ids into heap based on the frequency in descending order
                heapq.heappush(priority_queue, (-frequency, doc[0]))

        #decreasing the count
        max_count -= 1

        #popping the document ids from the heap
        for _ in range(len(priority_queue)):
            if priority_queue:
                if(documents_shown >= 30):
                    break
                frequency, document_id = heapq.heappop(priority_queue)
                #accessing the document index to get the document urls and then displaying them on terminal
                document_data[document_id] = document_urls[document_id]
                # print(document_id, " ", -frequency, " ", document_url)
                documents_shown += 1

    #ending the program execution time
    end_time = time.time()

    #calculating the time taken
    execution_time = end_time - start_time

    #displaying the time taken by the code to run
    print(f"Code took {execution_time:.6f} seconds to run.")
    print(document_data)
    return document_data