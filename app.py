
import gradio as gr
import requests
import plotly.express as px

# Hardcoded API key (use securely and consider environment variables for production)
API_KEY = 'b9d350d631c7212603d437d5e3e8965e'  # Replace with your actual API key

# Function to fetch environmental data from OpenWeatherMap
def fetch_city_data(location):
    try:
        # API call to get weather data
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(weather_url)

        if response.status_code == 200:
            weather_data = response.json()
            air_quality = get_air_quality_data(location)
            # Extract relevant data
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            # Simulate AQI (you can replace this with real AQI data fetching if available)
            aqi = air_quality if air_quality else 'Data Not Available'
            
            return {
                "location": location,
                "temperature": temperature,
                "humidity": humidity,
                "aqi": aqi
            }
        else:
            return {"error": "Could not fetch data for the specified location."}
    except Exception as e:
        return {"error": str(e)}

# Simulate air quality data
def get_air_quality_data(location):
    # This is a placeholder; replace with actual AQI fetching logic
    return 50  # Simulated AQI value

# Gradio interface function
def city_data_interface(location):
    data = fetch_city_data(location)
    
    if "error" in data:
        return data["error"]

    # Create a bar plot with the data
    fig = px.bar(
        x=['Temperature (°C)', 'Humidity (%)', 'Air Quality Index'],
        y=[data['temperature'], data['humidity'], data['aqi']],
        title=f"Environmental Data for {data['location']}",
        labels={'x': 'Metrics', 'y': 'Values'},
        color=['Temperature (°C)', 'Humidity (%)', 'Air Quality Index']
    )
    
    return fig

# Gradio Interface
interface = gr.Interface(
    fn=city_data_interface,
    inputs=[
        gr.Textbox(label="Enter a Location")  # Removed API Key input
    ],
    outputs=gr.Plot(label="Environmental Data Visualization"),
    title="CityMind AI Engine",
    description="Enter any city name to visualize its environmental data (AQI, Temperature, Humidity)."
)

# Launch the interface
interface.launch()

