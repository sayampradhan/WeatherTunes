import streamlit as st
import song as sm
from streamlit_player import st_player
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

                            # Custom Spotify-like banner
                            st.markdown(
                                f"""
                                <div style="background-color:#1DB954;padding:15px;border-radius:10px;">
                                    <h3 style="color:white;text-align:center;">🎵 Listen to this song on Spotify 🎵</h3>
                                    <a href="{spotify_url}" style="display:block;text-align:center;color:white;text-decoration:none;font-weight:bold;">
                                        {track_name}
                                    </a>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # Additional Media Player Example (optional)
                            st_player(url=spotify_url)
                    else:
                        st.error(f"No song recommendations available for the sky condition: {sky}")

            else:
                st.error("Failed to retrieve weather data.")
        else:
            st.error("Failed to retrieve city name from coordinates.")
    else:
        st.error("Failed to get location data. Ensure location services are enabled.")
else:
    st.error("Location could not be determined. Please ensure location services are enabled.")
