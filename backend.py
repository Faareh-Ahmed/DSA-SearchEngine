from flask import Flask, render_template, request
from querytest import search_inverted_index  # Import the function from the other file

app = Flask(__name__)

# Path to the folder for inverted index files
inverted_index_folder = "D:\\3rd Semester\\DSA\\inv"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    # Call the search_inverted_index function with the user's query
    results = search_inverted_index(query)

    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
