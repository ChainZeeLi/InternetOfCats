from flask import Flask, send_from_directory
from flask import send_file



app = Flask(__name__)

UPLOAD_DIRECTORY = "../catpix"
"""
@app.route('/download', methods=['GET'])

def download():
	return send_from_directory(directory='.', filename='../catpix/cat1.jpg')
"""

@app.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)

