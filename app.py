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
        'condition': weather.condition
    })

if __name__ == '__main__':
    app.run(debug=True)
