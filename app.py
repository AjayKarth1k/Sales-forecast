from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import matplotlib
import os
import matplotlib.pyplot as plt
import subprocess
matplotlib.use('Agg')

app = Flask(__name__, static_folder='webapp/dist/webapp')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if not file or (file.content_type != 'text/csv' and file.content_type != 'application/vnd.ms-excel' and file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return jsonify({'message': 'Invalid file type.'}), 400


    # Get the user input
    M = request.form.get('selectedNumerix')
    N = request.form.get('selectedPeriodicity')

    # Call the machine learning code with the input
    cmd = f'python machine.py --file {file.filename} --numerix {M} --periodicity {N}'
    subprocess.call(cmd, shell=True)

    return jsonify({'message': 'File uploaded and processed successfully.'}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
