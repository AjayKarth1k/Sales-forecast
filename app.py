from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='app/')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if not file or (file.content_type != 'text/csv' and file.content_type != 'application/vnd.ms-excel' and file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return jsonify({'message': 'Invalid file type.'}), 400
    
    # Data Extraction
    df = pd.read_csv(file) #Reads File from Angular
    Numerix = int(request.form.get('selectedNumerix')) #Numerix value
    periodicity = request.form.get('selectedPeriodicity') #Periodicity value

    # Data Cleaning
    df.dropna(inplace=True) #Removing null values
    df.reset_index(drop=True, inplace=True) #Setting ds as index and applied to dataset

    #Preprocessing Dataset
    df.columns = ["ds", "y"]
    df["ds"] = pd.to_datetime(df["ds"]) #Converting ds to datetime formate

    if periodicity == "Days":
        periodicity = "D"
    if periodicity == "Weeks":
        periodicity = "W"
    if periodicity == "Months":
        periodicity = "MS"
    if periodicity == "Years":
        periodicity = "A"

    #Prophet Prediction
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=Numerix, freq=periodicity)
    forecast = m.predict(future)
    fpp = forecast.tail(Numerix)  

    fcp = pd.DataFrame({'Date': fpp['ds'], 'Sales': fpp['yhat']})
    fcp = fcp.set_index("Date")
    fcp.to_csv(os.path.join(app.static_folder, 'assets', 'Predicted_result.csv'))
    from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

    # Calculate RMSE and MAPE
    actual = df['y'].tail(Numerix)
    predicted = fpp['yhat']
    rmse = mean_squared_error(actual, predicted, squared=False)
    mape = mean_absolute_percentage_error(actual, predicted)

    # Print RMSE and MAPE
    print("RMSE:", rmse)
    print("MAPE:", mape)

    
    fcp.plot(color="#18ce98")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'), dpi=300, bbox_inches='tight') 
    plt.show()
    plt.close()

    #To get Trend for the given Dataset
    fig2 = m.plot_components(forecast)
    for ax in fig2.axes:
        for line in ax.lines:
            line.set_color("#18ce98")
    fig2.savefig(os.path.join(app.static_folder, 'assets', 'Trends.png'), dpi=300, bbox_inches='tight')
    return jsonify({'message': 'File uploaded successfully.'}), 200

@app.route('/')
def serve():
    return send_from_directory('app', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('app', path)


if __name__ == '__main__':
    app.run(debug=True)