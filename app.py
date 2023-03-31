from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='webapp/dist/webapp')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if not file or (file.content_type != 'text/csv' and file.content_type != 'application/vnd.ms-excel' and file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return jsonify({'message': 'Invalid file type.'}), 400

    # Process the uploaded file using Pandas
    df = pd.read_csv(file)
    df = df[['Sales Person', 'Expenses']]

    # Generate the plot
    x = df['Sales Person']
    y = df['Expenses']
    value_x = 2.2;
    value_y = 2.5;
    M = request.form.get('selectedNumerix')
    N = request.form.get('selectedPeriodicity')
    plt.plot(x, y)
    plt.title(f'{M}, {N}')
    plt.savefig(os.path.join(app.static_folder, 'assets', 'data.png'))
    plt.close()

    return jsonify({'message': 'File uploaded successfully.'}), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
