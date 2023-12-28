from flask import Flask, render_template, request
from flask_socketio import SocketIO
from querytest import search_inverted_index  # Import the function from the other file
import subprocess
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')

    # Call the search_inverted_index function with the user's query
    results = search_inverted_index(query)

    return render_template('index.html', results=results)


@app.route('/upload_page')
def upload_page():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    # upload_folder = "D:\\3rd Semester\\DSA\\newFiles"
    upload_folder = "C:\\Users\\user\\OneDrive\\Desktop\\3rd Semester\\DSA\\Project\\nela-gt-2022.json\\nela-gt-2022\\newAdd_files"
    os.makedirs(upload_folder, exist_ok=True)
    print("API CALLED TO UPLOAD")
    if 'document' in request.files:
        document = request.files['document']
        print("Folder Path")
        print(document)
        # Process the document as needed (save, analyze, etc.)
        # Example: document.save('uploads/' + document.filename)

        # Save the document
        print("Entered IF")
        document_path = os.path.join(upload_folder,document.filename)
        print("Path Entered")
        document.save(document_path)
        print("Doc Saved")


        # Emit a message to the client indicating the start of processing
        socketio.emit('processing_started', {'message': 'Processing started for document...'})

        # Call the function to process the document using forward_indexer.py
        print("Printing the DOC PATH")
        print(document_path)
        subprocess.run(["python", "forward_indexer.py", upload_folder])

        print("FORWARD INDEX DONE\nINVERTED INDEX DONE")
        # Call inverted_indexer.py
        # subprocess.run(["python", "inverted_indexer.py"])

        # Emit a message to the client indicating the completion of processing
        socketio.emit('processing_completed', {'message': 'Document processing completed.'})

        return f'Document "{document.filename}" uploaded successfully!'
        # Add code to delete the document after processing
    else:
        return 'No document provided.'


if __name__ == '__main__':
    socketio.run(app, debug=True)
