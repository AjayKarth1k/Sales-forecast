import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
from prophet.plot import plot_plotly, plot_components_plotly
import plotly.graph_objs as go
import datetime
import os
from plotly.io import write_image

def run_prophet(file, numerix, periodicity):
    df = pd.read_csv(file)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.columns = ['ds', 'y']

    # Change the date to datetime object
    df['ds'] = pd.to_datetime(df['ds'])

    if periodicity == 'Daily':
        freq = 'D'
    elif periodicity == 'Weekly':
        freq = 'W'
        numerix *= 7
    elif periodicity == 'Monthly':
        freq = 'MS'
    elif periodicity == 'Year':
        freq = 'A'
    else:
        freq = 'M'

    length = len(df)
    train_size = round((80/100)*length)

    train = df[:train_size]
    test = df[train_size:]

    m = Prophet()
    m.fit(train)
    future = m.make_future_dataframe(periods=numerix, freq=freq)
    forecast = m.predict(future)[-numerix:]

    if freq == 'W':
        forecast = forecast.resample('W', on='ds').sum()
    if freq == 'M':
        forecast = forecast.resample('MS', on='ds').sum()
        # Plotting
    fig = plot_plotly(m, forecast)
    fig.update_layout(
        title='Forecast Plot',
        xaxis_title='Date',
        yaxis_title='Value'
    )

    fig_comp = plot_components_plotly(m, forecast)
    fig_comp.update_layout(
        title='Forecast Components Plot'
    )

    actual_data = go.Scatter(x=test['ds'], y=test['y'], name='Actual Data')
    forecast_data = go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast Data')

    fig_final = go.Figure()
    fig_final.add_trace(actual_data)
    fig_final.add_trace(forecast_data)
    fig_final.update_layout(
        title='Actual vs Forecast Plot',
        xaxis_title='Date',
        yaxis_title='Value'
    )
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    fig.write_image(os.path.join(assets_dir, 'forecast.png'))
    fig_comp.write_image(os.path.join(assets_dir, 'forecast_components.png'))
    fig_final.write_image(os.path.join(assets_dir, 'actual_vs_forecast.png'))

    return 'success'

