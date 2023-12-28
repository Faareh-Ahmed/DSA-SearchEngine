import json
import nltk
import os
from math import log

nltk.download("punkt")

def inverted_indexer(forwardindex):

    # Check if forwardindex Data structure is empty then simply return
    print("STARTING INVERTED INDEX")
    if not forwardindex:
        print("Already Made Inverted Index for this Documents")
        return
    
    # Path to the folder for inverted index files containing the Barreling
    output_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"
    os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

    # Initialize the inverted index dictionaries for each barrel
    # Load existing inverted index barrels if they exist
    # Barreling is done based on the first 3 characters of the word and 
    # for numeric characters starting from (0 to 9). Another Barrel is made that stores the
    # words containing the Special Characters

    barrels = {}
    for char1 in range(ord('a'), ord('z') + 1):
        for char2 in range(ord('a'), ord('z') + 1):
            for char3 in range(ord('a'), ord('z') + 1):
                char = str(chr(char1) + chr(char2)+ chr(char3))
                barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
                if os.path.exists(barrel_file):
                    with open(barrel_file, "r") as file:
                        barrels[char] = json.load(file)
                else:
                    barrels[char] = {}

    # Include combinations where the second character is from '0' to '9'
    for char1 in range(ord('a'), ord('z') + 1):
        for char2 in range(ord('0'), ord('9') + 1):
            char = str(chr(char1) + chr(char2))
            barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
            if os.path.exists(barrel_file):
                with open(barrel_file, "r") as file:
                    barrels[char] = json.load(file)
            else:
                barrels[char] = {}


    for char in range(10):
        barrel_file = os.path.join(output_folder, f"inverted_index_{char}.json")
        if os.path.exists(barrel_file):
            with open(barrel_file, "r") as file:
                barrels[str(char)] = json.load(file)
        else:
            barrels[str(char)]={}

    barrel_file_other = os.path.join(output_folder, "inverted_index_other.json")
    if os.path.exists(barrel_file_other):
        with open(barrel_file_other, "r") as file:
            barrels['other'] = json.load(file)
    else:
            barrels['other']={}



    data = forwardindex
    count=0

    # reading each entry of the Forward Index Data Structure

    for test_entry in data:
        count+=1
        print(count)

        # Retrieving the necessary data from the Forward index Data structure
        doc_id = test_entry["di"]
        stemmed_tokens = test_entry["st"]
        frequency = test_entry["tf"]

        for position, token in enumerate(stemmed_tokens, start=1):
            # Get the frequency and Position of the currect word
            frequency = test_entry["tf"][token]
            position = test_entry["tp"].get(token, [])

            # Calculate the rank of each word in the document and storing them in the Inverted Index
            # We have primarily referred the TF-IDF ranking algorithm and made changes according to our
            # current project scenario

            tf = frequency / len(stemmed_tokens)
            idf = log(len(stemmed_tokens) / (frequency + 1))  # Adding 1 to avoid division by zero
            rank = tf * idf

            # Selecting the appropriate Barrel for the Word
            # Get the first character of the token 
            first_char = str(token)[0].lower() if str(token) else None

            # Ensure first_char is not None (empty or not a string)
            if first_char is not None:
                # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
                if '0' <= first_char <= '9':
                    barrel = first_char

                elif 'a' <= first_char <= 'z':
                    if(len(token)<2):
                        second_char=first_char
                        third_char=first_char
                        char=str(first_char+second_char+third_char)
                        barrel=char
                    else:
                        second_char = str(token)[1].lower() if str(token) else None
                        if('0' <= second_char <= '9'):
                            char = str(first_char+second_char)
                            barrel=char
                        # Check if the second_char is not a lowercase letter or a digit
                        elif('a' <= second_char <= 'z'):
                            if(len(token)<3):
                                third_char=second_char
                                char=str(first_char+second_char+third_char)
                                barrel=char
                            else:
                                third_char = str(token)[2].lower() if str(token) else None
                                
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

            # Create the inverted index entry for the token if it is not present in the barrel
                if token not in barrels[barrel]:
                    barrels[barrel][token] ={}

                # Update the inverted index entry by adding the desired information about the word
                if doc_id not in barrels[barrel][token]:
                    word_details={
                        "f":frequency,
                        "p":position,
                        "r":rank
                    }
                    barrels[barrel][token][doc_id]=word_details

                    


    # Save inverted index barrels to separate files
    print("Starting Writing to FIle\n")
    for char, inverted_index in barrels.items():
        inverted_index_file = os.path.join(output_folder, f"inverted_index_{char}.json")
        with open(inverted_index_file, "w") as file:
            json.dump(inverted_index, file)

    print("Inverted Index barrels stored in files.")
