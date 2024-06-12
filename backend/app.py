from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/weather')
def get_weather():
    api_key = '956045bef81d1bb66a2e8f5a4e1c0eba'
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'City not provided'}), 400

    try:
        # Fetch current weather
        current_weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}")
        current_weather_data.raise_for_status()

        # Fetch weather forecast for the next 7 days
        forecast_data = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=imperial&APPID={api_key}")
        forecast_data.raise_for_status()

        current_weather_info = current_weather_data.json()
        weather = current_weather_info['weather'][0]['main']
        temp = round(current_weather_info['main']['temp'])
        precipitation = current_weather_info['weather'][0].get('description', 'N/A')
        humidity = current_weather_info['main'].get('humidity', 'N/A')
        wind_speed = current_weather_info['wind'].get('speed', 'N/A')
        sunrise = current_weather_info['sys'].get('sunrise', 'N/A')
        sunset = current_weather_info['sys'].get('sunset', 'N/A')

        forecast_info = forecast_data.json()['list'][:7]  # Extract next 7 days forecast
        forecast = [{
            'date': day['dt_txt'],
            'weather': day['weather'][0]['main'],
            'temperature': round(day['main']['temp']),
            'precipitation': day['weather'][0].get('description', 'N/A'),
            'humidity': day['main'].get('humidity', 'N/A'),
            'wind_speed': day['wind'].get('speed', 'N/A')
        } for day in forecast_info]

        return jsonify({
            'city': city,
            'current_weather': {
                'weather': weather,
                'temperature': temp,
                'precipitation': precipitation,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'sunrise': sunrise,
                'sunset': sunset
            },
            'forecast': forecast
        })
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'An error occurred while fetching weather data'}), 500

if __name__ == '__main__':
    app.run(debug=True)