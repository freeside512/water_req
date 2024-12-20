import os
from flask import Flask, request, jsonify
import joblib
from weather import Weather
import pandas as pd
app = Flask(__name__)


crop_model = joblib.load('data/crop_rec.joblib')
water_model = joblib.load('data/water_level_pl.joblib')


@app.route('/weather', methods=['POST'])
def get_weather():
    data = request.json
    longitude = data.get('longitude')
    latitude = data.get('latitude')

    if not longitude or not latitude:
        return jsonify({'error': 'Longitude and Latitude are required'}), 400

    weather = Weather(longitude=longitude, latitude=latitude)
    weather.temp_cond()

    return jsonify({
        'temperature': weather.temp,
        'condition': weather.condition,
        'icon': weather.icon,
        'send_condition': weather.send_cond,
        'send_temp': weather.send_temp,
        'send_region': weather.send_region
    })


@app.route('/predict_crop', methods=['POST'])
def predict_crop():
    data = request.json
    features = data.get('features')

    if not features:
        return jsonify({'error': 'Features are required'}), 400

    try:
        prediction = crop_model.predict([features])
        return jsonify({'crop_prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_water', methods=['POST'])
def predict_water():
    data = request.json
    features = pd.DataFrame(data)
    if not features:
        return jsonify({'error': 'Features are required'}), 400

    try:
        prediction = water_model.predict([features])
        return jsonify({'water_level_prediction': prediction[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
