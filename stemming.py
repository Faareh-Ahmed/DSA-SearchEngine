# import nltk
# from nltk.stem import SnowballStemmer
# from nltk.tokenize import word_tokenize

# # Download the punkt data (if not already downloaded)
# nltk.download('punkt')

# # Sample text
# text = "CORPORA , @ running good better best residents who had expected to ring in 2022 in their homes are instead starting off the new year trying to salvage what remains of them after a wind-whipped wildfire tore through the Denver suburbs"

# # Tokenize the text
# words = word_tokenize(text)

# # Initialize the PorterStemmer
# stemmer = SnowballStemmer(language='english')

# # Stem each word
# stemmed_words = [stemmer.stem(word) for word in words]
# print(stemmed_words)
# # Print the original and stemmed words
# # for original, stemmed in zip(words, stemmed_words):
# #     print(f"{original} => {stemmed}")


def check_duplicates(file_path):
    try:
        with open(file_path, 'r') as file:
            doc_ids = set()
            duplicates = set()
            for line_number, line in enumerate(file, start=1):
                doc_id = line.strip()
                if doc_id in doc_ids:
                    duplicates.add(doc_id)
                else:
                    doc_ids.add(doc_id)

            if duplicates:
                print("Duplicate docIDs found:")
                for doc_id in duplicates:
                    print(f"  {doc_id}")
            else:
                print("No duplicate docIDs found.")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
file_path = 'existing_doc_ids.txt'
check_duplicates(file_path)
