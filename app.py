import os
from flask import Flask, request, jsonify
from weather import Weather

app = Flask(__name__)

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
        'icon':weather.icon,
        'send_condition':weather.send_cond,
        'send_temp':weather.send_temp,
        'send_region':weather.send_region
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
