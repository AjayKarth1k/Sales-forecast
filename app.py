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
    df.head()
    df.columns = ["ds", "y"]
    df.head()
    df["ds"] = pd.to_datetime(df["ds"])
    df.head()
    df.tail(20)
    Numerix = int(request.form.get('selectedNumerix'))
    periodicity = request.form.get('selectedPeriodicity')
    DW = "D"
    if periodicity == "Daily":
        periodicity = "D"
    if periodicity == "Weekly":
        periodicity = "D"
        DW = "W"
        Numerix = Numerix * 7
    if periodicity == "Monthly":
        periodicity = "MS"
    if periodicity == "Yearly":
        periodicity = "A"
    df.plot(x="ds", y="y", figsize=(10, 6))
    length = len(df)
    train_size = round((80 / 100) * length)
    train = df[: length - 12]
    test = df[length - 12 :]
    train.tail()
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=Numerix, freq=periodicity)
    forecast = m.predict(future)
    thecsv = pd.DataFrame({'Date': forecast['ds'], 'Sales': forecast['yhat']})
    thecsv.to_csv('Final_otput.csv', index=False)
    fpp = forecast.tail(Numerix)
    print(fpp)
    fcp = pd.DataFrame({'Date': fpp['ds'], 'Sales': fpp['yhat']})
    fcp = fcp.set_index("Date")
    print(fcp)
    fcp.to_csv(os.path.join(app.static_folder, 'assets', 'Predicted_result.csv'))
    if(periodicity == 'D' and DW=='D'):
        fcp.plot(color="#18ce98")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png')) 
        plt.show()
        plt.close()
    if(periodicity == 'D' and DW == 'W'):
        fcp.plot(color="#18ce98")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png')) 
        plt.show()
        plt.close()
    print(len(train))
    if periodicity == "MS":
        fcp.plot(color="#18ce98")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))
        plt.show()
        plt.close()
    if periodicity == "A":
        fcp.plot(color="#18ce98")
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))
        plt.show()
        plt.close()
    forecast.tail()
    fig2 = m.plot_components(forecast)
    for ax in fig2.axes:
        for line in ax.lines:
            line.set_color("#18ce98")
    fig2.savefig(os.path.join(app.static_folder, 'assets', 'Trends.png'))
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