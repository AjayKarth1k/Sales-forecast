from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from flask import Flask, send_from_directory
import datetime

app = Flask(__name__, static_folder='webapp/dist/webapp')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if not file or (file.content_type != 'text/csv' and file.content_type != 'application/vnd.ms-excel' and file.content_type != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return jsonify({'message': 'Invalid file type.'}), 400

    # Process the uploaded file using Pandas
    df = pd.read_csv(file)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    df.head()

    df.columns = ["ds", "y"]

    df.head()

    # Change the date to datetime object
    df["ds"] = pd.to_datetime(df["ds"])
    df.head()

    df.tail(20)
    Numerix = int(request.form.get('selectedNumerix'))
    periodicity = request.form.get('selectedPeriodicity')
    DW = "D"
    if periodicity == "Daily":
        periodicity = "D"
    elif periodicity == "Weekly":
        periodicity = "D"
        DW = "W"
        Numerix = Numerix * 7
    elif periodicity == "Monthly":
        periodicity = "MS"
    elif periodicity == "Year":
        periodicity = "A"
    else:
        periodicity = "M"

    df.plot(x="ds", y="y", figsize=(10, 6))

    length = len(df)
    train_size = round((80 / 100) * length)

    train = df[: length - 12]
    test = df[length - 12 :]
    train.tail()

    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=Numerix + 1, freq=periodicity)
    forecast = m.predict(future)

    last_date = forecast["ds"].tail(1)
    print(len(df))

    fpp = forecast.tail(Numerix)
    print(fpp)

    print(len(fpp))

    if periodicity == "D" and DW == "D":
        ld = [1960, 12, 3]
        ld = datetime.datetime(ld[0], ld[1], ld[2])
        predDate = [ld]
        # Date prediction

        for i in range(1, Numerix):
            nd = ld + datetime.timedelta(days=i)
            predDate.append(nd)
        fpp = list(fpp)
        # fpp.insert(0, 432.0)
        fcp = pd.DataFrame(predDate, columns=["date"])

        fcp["future sales"] = fpp
        fcp = fcp.set_index(fcp["date"])
        fcp.drop(["date"], axis="columns", inplace=True)
        print(fcp)
        fcp.plot()

        # Render the image
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))
        plt.show()
        plt.close()

    if periodicity == "W" and DW == "W":
        ld = [1960, 12, 3]
        ld = datetime.datetime(ld[0], ld[1], ld[2])
        predDate = [ld]
        # Date prediction

        for i in range(1, Numerix * 7):
            nd = ld + datetime.timedelta(days=i)
            predDate.append(nd)
        fpp = list(fpp)
        # fpp.insert(0, 432.0)
        fcp = pd.DataFrame(predDate, columns=["date"])

        fcp["future sales"] = fpp
        fcp = fcp.set_index(fcp["date"])
        fcp.drop(["date"], axis="columns", inplace=True)
        print(fcp)
        fcp.plot()
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))
        plt.show()
        plt.close()

    print(len(train))

    if periodicity == "MS":
        print(fpp)
        # Date prediction

        fcp = fpp[["ds", "yhat"]].copy()

        fcp = fcp.set_index(fcp["ds"])
        fcp.drop(["ds"], axis="columns", inplace=True)
        print(fcp)
        fcp.plot()
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))
        plt.show()
        plt.close()

    if periodicity == "A":
        print(fpp)
        # Date prediction

        fcp = fpp[["ds", "yhat"]].copy()

        fcp = fcp.set_index(fcp["ds"])
        fcp.drop(["ds"], axis="columns", inplace=True)
        print(fcp)
        fcp.plot()
        plt.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))
        plt.show()
        plt.close()


    forecast.tail()

    fig = plot_plotly(m, forecast)
    fig

    fig.write_html("webapp/forecast.html")

    # Finding out the trend

    fig2 = m.plot_components(forecast)

    fig2.savefig(os.path.join(app.static_folder, 'assets', 'prediction.png'))

    # """EVALUATING THE MODEL

    # """

    # from statsmodels.tools.eval_measures import rmse

    # predictions = forecast.iloc[-12:]["yhat"]

    # print(test["y"])

    # print(
    #     "Root Mean Squared Error between actual and  predicted values: ",
    #     rmse(predictions, test["y"]),
    # )
    # print("Mean Value of Test Dataset:", test["y"].mean())

    # from prophet.diagnostics import cross_validation
    # from prophet.diagnostics import performance_metrics

    # df_cv = cross_validation(m, initial=len(train), period="180 days", horizon="365 days")
    # df_metrics = performance_metrics(df_cv)



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