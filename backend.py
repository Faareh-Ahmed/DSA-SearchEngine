from flask import Flask, render_template, request
from querytest import search_inverted_index  # Import the function from the other file
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    # Call the search_inverted_index function with the user's query
    results = search_inverted_index(query)

    return render_template('index.html', results=results)

# upload_folder = "D:\\3rd Semester\\DSA\\newFiles"
upload_folder = "C:\\Users\\hbrsa\\OneDrive\\Desktop"
os.makedirs(upload_folder, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload():
    if 'document' in request.files:
        document = request.files['document']
        # Process the document as needed (save, analyze, etc.)
        # Example: document.save('uploads/' + document.filename)

        # Save the document
        document_path = os.path.join(upload_folder)
        document.save(document_path)

        # Call the function to process the document using forward_indexer.py
        subprocess.run(["python", "forward_indexer.py", document_path])

        # Call inverted_indexer.py
        subprocess.run(["python", "inverted_indexer.py"])


        return f'Document "{document.filename}" uploaded successfully!'
    else:
        return 'No document provided.'


if __name__ == '__main__':
    app.run(debug=True)