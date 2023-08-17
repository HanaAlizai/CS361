# Author: Hana Alizai
# Date: 7/31/23
# Description: This is the Python implementation of the microservice for my partner's project
# using Flask for the RESTful API  and the requests library for making API calls to a weather provider
# (WeatherAPI).

# Implementation

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS for your app

# Weather API base URL
WEATHER_API_URL = 'http://api.weatherapi.com/v1/current.json'

@app.route('/weather', methods=['GET'])
@cross_origin()  # Add this decorator to enable CORS for this route
def get_weather():
    # Get latitude and longitude from query parameters
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude are required parameters.", "status_code": 400}), 400

    try:
        # Make API call to Weather API to fetch weather data
        params = {
            'key': '6d03fe4c17934db68ab24339230108',  # Weather API key
            'q': f'{latitude},{longitude}',
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()

        # Extract relevant weather information
        location = weather_data['location']['name']
        temperature = weather_data['current']['temp_c']
        weather_description = weather_data['current']['condition']['text']
        humidity = weather_data['current']['humidity']
        wind_speed = weather_data['current']['wind_kph']

        # Create the weather response object
        weather_response = {
            "location": location,
            "temperature": temperature,
            "weather_description": weather_description,
            "humidity": humidity,
            "wind_speed": wind_speed
        }

        return jsonify(weather_response), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error fetching weather data.", "status_code": 500}), 500
    except KeyError:
        return jsonify({"error": "Invalid response from weather API.", "status_code": 500}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

# Testing:
# Using web browser: http://localhost:5000/weather?latitude=37.7749&longitude=-122.4194
# Example of San Francisco ^
