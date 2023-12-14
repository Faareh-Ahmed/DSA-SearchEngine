from flask import Flask, render_template, request, redirect, url_for
import json
import os
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from os import path
app = Flask(__name__)



# Initialize the SnowballStemmer
stemmer = SnowballStemmer(language="english")

# Get the set of English stop words
stop_words = set(stopwords.words("english"))

common_docs = {}
docurls = {}


# Function to search for a word in the inverted index
def search_inverted_index(query_word, common_docs, docurls):
    # Tokenizing the combined words
   
# Get the absolute path of the directory containing this script (app.py)
    # Path to the folder for inverted index files
    working = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\test_inverted_index_files"
    # Print the working directory

    print("HAHA")
    strpath=r"C:\Users\user\OneDrive\Desktop\3rd Semester\DSA\Project\nela-gt-2022.json\nela-gt-2022\codeSpace\DSA-SearchEngine"
    print("current Dir: %s" % strpath)
    print("abspath: %s" %path.abspath( strpath))

    inverted_index_folder = os.path.abspath((working))
    print("Working Directory of Inverted Index Files:", inverted_index_folder)

    # Path to the DocURL file 
    docurl_file_path = os.path.join(
        "..","..", "test_forward_index_files", "docURL.json"
    ) 

    tokens = [word_tokenize(query_word)]

    # Remove stop words and punctuation, and stem the remaining words 
    stemmed_words = [
        stemmer.stem(token)
        for sentence_tokens in tokens
        for token in sentence_tokens
        if token.isalnum() and token.lower() not in stop_words
    ]

    for word in stemmed_words:
        # Get the first character of the stemmed query word
        first_char = word[0].lower() if word else None

        if first_char is not None:
            # Check if the first_char is numeric and update the inverted index entry in the 'numeric' barrel
            if "0" <= first_char <= "9":
                barrel = first_char
            elif "a" <= first_char <= "z":
                if len(word) < 2:
                    second_char = first_char
                    char = str(first_char + second_char)
                    barrel = char
                else:
                    second_char = str(word)[1].lower() if str(word) else None
                    if ("0" <= second_char <= "9") or ("a" <= second_char <= "z"):
                        char = str(first_char + second_char)
                        barrel = char
                    else:
                        barrel = "other"
            else:
                barrel = "other"

        # Load the inverted index for the specific barrel
        inverted_index_file_path = os.path.join(
            inverted_index_folder, f"inverted_index_barrel_{barrel}.json"
        )

        print("Inverted Barrel: ",inverted_index_file_path)
        try:
            with open(inverted_index_file_path, "r") as file:
                inverted_index = json.load(file)
        except FileNotFoundError:
            print(f"Inverted index file for '{query_word}' not found.")
            return common_docs, docurls

        # Check if the stemmed query word is in the inverted index
        if word in inverted_index:
            documents = list(inverted_index[word].keys())

            for document in documents:
                if document not in common_docs:
                    common_docs[document] = inverted_index[word][document]["rank"]
                else:
                    common_docs[document] += inverted_index[word][document]["rank"]

    return common_docs, docurls


def search(query, common_docs, docurls):
    stemmed_words = [stemmer.stem(token.lower()) for token in word_tokenize(query) if token.isalnum() and token.lower() not in stop_words]

    for word in stemmed_words:
        common_docs, docurls = search_inverted_index(word, common_docs.copy(), docurls.copy())

    sorted_documents = sorted(common_docs.keys(), key=lambda doc_id: common_docs[doc_id], reverse=True)
    top_documents = sorted_documents[:10]

    return [{"document_id": doc_id, "url": docurls.get(str(doc_id), "")} for doc_id in top_documents]



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search_results():
    global common_docs, docurls
    query = request.form["query"]
    common_docs = {}  # Reset common_docs for each search
    results = search(query, common_docs, docurls)
    return render_template("results.html", query=query, results=results)


@app.route("/upload", methods=["POST"])
def upload_documents():
    if "files" not in request.files:
        return redirect(request.url)

    files = request.files.getlist("files")
    # Add logic to process and store uploaded documents if needed
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)