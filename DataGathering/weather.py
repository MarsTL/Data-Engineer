import requests

API_KEY = "1db8d48ff01679de46c0a5d0e049aaf7"
lat = 45.5152
lon = -122.6784

#current weather function
def get_weather(API_KEY, lat, lon):
  #format string
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
  
  response = requests.get(url).json()

  city = response['name']
  country = response['sys']['country']

  description = response['weather'][0]['description']


  temp = response['main']['temp']
  #convert kelvin to F
  temp = (temp * 1.8) - 459.67

  feels_like = response['main']['feels_like']
  #convert kelvin to F
  feels_like = (feels_like * 1.8) - 459.67

  humidity = response['main']['humidity']


  return{
  'city': city,
  'country': country,
  'temp': round(temp,2),
  'feels_like': round(feels_like, 2),
  'humidity': humidity ,
  'description': description

  }

weather = get_weather(API_KEY, lat, lon)


#get nxt three days function
def get_3_day_weather(API_KEY, lat, lon):
  url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
  response = requests.get(url).json()

  rain_forecast = False
  for forecast in response['list']:
    description = forecast['weather'][0]['description']
    if 'rain' in description.lower():
        rain_forecast = True
        break
    
  if rain_forecast:
    print("🌧️ Rain is forecasted in Portland within the next 3 days!")
  else:
    print("☀️ No rain forecasted in Portland within the next 3 days.")

print("\n")
print(f"📍 Weather for {weather['city']}, {weather['country']}")
print("\n")
print("🌡️ Temp (°F):", weather['temp'])
print("😌 Feels Like (°F):", weather['feels_like'])
print("💧 Humidity (%):", weather['humidity'])
print("☁️ Weather Condition:", weather['description'])
print("\n")

three_days = get_3_day_weather(API_KEY, lat, lon)
