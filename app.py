from flask import Flask, render_template, request
import requests
from api_key import API_KEY  # Import API key from separate file

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    city_name = request.form['city']
    weather_data = get_weather_data(city_name, API_KEY)

    if weather_data:
        return render_template('index.html', city=city_name.capitalize(), desc=weather_data['desc'], 
                               temp=weather_data['temp'], feels_like=weather_data['feels_like'], 
                               humid=weather_data['humid'])
    else:
        return render_template('index.html', error='City not found! Please try again.')

def get_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)

    print(f"Requesting URL: {url}")  # Debugging
    print(f"Response Code: {response.status_code}")  # Debugging

    if response.status_code == 200:
        json_data = response.json()
        print("Weather Data:", json_data)  # Debugging
        return {
            'desc': json_data['weather'][0]['description'],
            'temp': json_data['main']['temp'],
            'feels_like': json_data['main']['feels_like'],
            'humid': json_data['main']['humidity']
        }
    else:
        print(f"Error fetching weather data: {response.text}")  # Debugging
        return None

if __name__ == '__main__':
    app.run(debug=True)
