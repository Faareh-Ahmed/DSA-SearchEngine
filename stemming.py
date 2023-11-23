import nltk
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

# Download the punkt data (if not already downloaded)
nltk.download('punkt')

# Sample text
text = "CORPORA , @ running good better best residents who had expected to ring in 2022 in their homes are instead starting off the new year trying to salvage what remains of them after a wind-whipped wildfire tore through the Denver suburbs"

# Tokenize the text
words = word_tokenize(text)

# Initialize the PorterStemmer
stemmer = SnowballStemmer(language='english')

# Stem each word
stemmed_words = [stemmer.stem(word) for word in words]
print(stemmed_words)
# Print the original and stemmed words
# for original, stemmed in zip(words, stemmed_words):
#     print(f"{original} => {stemmed}")
