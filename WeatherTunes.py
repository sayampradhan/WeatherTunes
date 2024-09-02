import streamlit as st
import song as sm
from streamlit_geolocation import streamlit_geolocation
from weather_data import get_city, get_weather_data

# Set the title of the Streamlit app (must be the first Streamlit command)
st.set_page_config(page_title="WeatherTunes", page_icon=":musical_note:")
st.title("WeatherTunes")

# Get the user's location using streamlit_geolocation
location = streamlit_geolocation()

if location:
    lon = location.get('longitude')
    lat = location.get('latitude')

    if lon and lat:
        city = get_city(lat, lon)
        if city:
            st.write(f"Detected city: {city}")
            weather = get_weather_data(city)

            if weather:
                sky = weather
                st.write(f"Sky condition: {sky}")

                # Automatically generate a song recommendation based on the sky condition
                data, weather_conditions = sm.load_data()

                if data is None or weather_conditions is None:
                    st.error("Failed to load data. Please check the dataset path or file.")
                else:
                    if sky in weather_conditions:
                        recommended_song = sm.song(sky, weather_conditions, data)

                        if "error" in recommended_song:
                            st.error(recommended_song["error"])
                        else:
                            track_name = recommended_song["name"]
                            spotify_url = recommended_song["url"]

                            st.markdown(f"**Recommended Song:** {track_name}")
                            # st.markdown(, unsafe_allow_html=True)
                            st.markdown(f"<img src=\"https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Spotify_icon.svg/232px-Spotify_icon.svg.png\" width=20>   [Listen to this song on Spotify]({spotify_url})", unsafe_allow_html=True) 
                            # st.markdown()

                    else:
                        st.error(f"No song recommendations available for the sky condition: {sky}")

            else:
                st.error("Failed to retrieve weather data.")
        else:
            st.error("Failed to retrieve city name from coordinates.")
    else:
        st.error("Failed to get location data. Ensure location services are enabled.")
else:
    st.error(
        "Location could not be determined. Please ensure location services are enabled."
    )

footer_html = """
<div style='text-align: center;'>
  <p>Developed with ❤️ by Sayam</p>
  <p><a href='https://github.com/sayampradhan/WeatherTunes/tree/main' target='_blank'>View on GitHub</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
