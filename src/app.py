# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, send_from_directory, jsonify
import utils
import train_models as tm
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
#
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                           'favicon.ico',mimetype='image/vnd.microsoft.icon')


def perform_training(stock_name, df, models_list):
    all_colors = {'SVR_linear': '#FF9EDD',
                  'SVR_poly': '#FFFD7F',
                  'SVR_rbf': '#FFA646',
                  'linear_regression': '#CC2A1E',
                  'random_forests': '#8F0099',
                  'KNN': '#CCAB43',
                  'elastic_net': '#CFAC43',
                  'DT': '#85CC43',
                  'LSTM_model': '#CC7674'}

    print(df.head())
    dates, prices, ml_models_outputs, prediction_date, test_price = tm.train_predict_plot(stock_name, df, models_list)
    origdates = dates
    if len(dates) > 20:
        dates = dates[-20:]
        prices = prices[-20:]

    all_data = []
    all_data.append((prices, 'false', 'Data', '#000000'))
    for model_output in ml_models_outputs:
        if len(origdates) > 20:
            all_data.append(
                (((ml_models_outputs[model_output])[0])[-20:], "true", model_output, all_colors[model_output]))
        else:
            all_data.append(
                (((ml_models_outputs[model_output])[0]), "true", model_output, all_colors[model_output]))

    all_prediction_data = []
    all_test_evaluations = []
    all_prediction_data.append(("Original", test_price))
    for model_output in ml_models_outputs:
        all_prediction_data.append((model_output, (ml_models_outputs[model_output])[1]))
        all_test_evaluations.append((model_output, (ml_models_outputs[model_output])[2]))

    return all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data, all_test_evaluations

all_files = utils.read_all_stock_files('individual_stocks_5yr')
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# '‘/’ URL is bound with hello_world() function.
def landing_function():
    # all_files = utils.read_all_stock_files('individual_stocks_5yr')
    # df = all_files['A']
    # # df = pd.read_csv('GOOG_30_days.csv')
    # all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data = perform_training('A', df, ['SVR_linear'])
    stock_files = list(all_files.keys())

    return render_template('index.html',show_results="false", stocklen=len(stock_files), stock_files=stock_files, len2=len([]),
                           all_prediction_data=[],
                           prediction_date="", dates=[], all_data=[], len=len([]))

@app.route('/process', methods=['POST'])
def process():

    stock_file_name = request.form['stockfile']
    ml_algoritms = request.form.getlist('mlalgos')

    # all_files = utils.read_all_stock_files('individual_stocks_5yr')
    df = all_files[str(stock_file_name)]
    # df = pd.read_csv('GOOG_30_days.csv')
    all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data, all_test_evaluations = perform_training(str(stock_file_name), df, ml_algoritms)
    stock_files = list(all_files.keys())

    return render_template('index.html',all_test_evaluations=all_test_evaluations, show_results="true", stocklen=len(stock_files), stock_files=stock_files,
                           len2=len(all_prediction_data),
                           all_prediction_data=all_prediction_data,
                           prediction_date=prediction_date, dates=dates, all_data=all_data, len=len(all_data))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # This is a placeholder for the prediction logic
        # We'll implement the actual prediction model later
        data = request.get_json()
        stock_symbol = data.get('symbol', '')
        
        # For now, return a dummy prediction
        prediction = {
            'symbol': stock_symbol,
            'predicted_price': 100.0,
            'confidence': 0.85,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
