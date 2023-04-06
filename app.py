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

app = Flask(__name__, static_folder='webapp/src')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if not file or (file.content_type != 'text/csv' and file.content_type != 'application/vnd.ms-excel' and file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return jsonify({'message': 'Invalid file type.'}), 400
    

    df = pd.read_csv(file)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.columns = ["ds", "y"]
    df["ds"] = pd.to_datetime(df["ds"])
    Numerix = int(request.form.get('selectedNumerix'))
    periodicity = request.form.get('selectedPeriodicity')
    if periodicity == "Days":
        periodicity = "D"
    if periodicity == "Weeks":
        periodicity = "W"
    if periodicity == "Months":
        periodicity = "MS"
    if periodicity == "Years":
        periodicity = "A"
    length = len(df)
    train_size = round((80 / 100) * length)
    train = df[: length - 12]
    test = df[length - 12 :]
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=Numerix, freq=periodicity)
    forecast = m.predict(future)
    fpp = forecast.tail(Numerix)
    fcp = pd.DataFrame({'Date': fpp['ds'], 'Sales': fpp['yhat']})
    fcp = fcp.set_index("Date")
    fcp.to_csv(os.path.join(app.static_folder, 'assets', 'Predicted_result.csv'))
    if(periodicity == 'D'):
        fcp.plot(color="#18ce98")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'), dpi=300, bbox_inches='tight') 
        plt.show()
        plt.close()
    elif(periodicity == 'W'):
        fcp.plot(color="#18ce98")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'), dpi=300, bbox_inches='tight') 
        plt.show()
        plt.close()
        print(len(train))
    elif periodicity == "MS":
        fcp.plot(color="#18ce98")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'), dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
    elif periodicity == "A":
        fcp.plot(color="#18ce98")
        plt.xlabel("Date")
        plt.ylabel("Sales")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'), dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
    fig2 = m.plot_components(forecast)
    for ax in fig2.axes:
        for line in ax.lines:
            line.set_color("#18ce98")
    fig2.savefig(os.path.join(app.static_folder, 'assets', 'Trends.png'), dpi=300, bbox_inches='tight')
    return jsonify({'message': 'File uploaded successfully.'}), 200

if __name__ == '__main__':
    app.run(debug=True)