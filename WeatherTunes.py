import song as sm
import streamlit as st
from streamlit_player import st_player
from streamlit_elements import media

# Set the title of the Streamlit app
st.set_page_config(page_title="WeatherTunes", page_icon=":musical_note:")
st.title("WeatherTunes")

# Add some spacing and instructions
st.markdown("""
    <style>
        .stForm {padding: 2rem; border-radius: 8px; border: 1px solid #e0e0e0;}
        .stForm div {margin-bottom: 1rem;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("Select a weather condition to get a song recommendation based on it. Your track will be found on Spotify.")

with st.form('weather_based_song'):
    # Load the dataset and available weather conditions
    data, weather_conditions = sm.load_data()

    # Check if data loaded successfully
    if data is None or weather_conditions is None:
        st.error("Failed to load data. Please check the dataset path or file.")
    else:
        # Create a dropdown menu for selecting the weather condition
        selected_weather = st.selectbox("Select Weather Condition", weather_conditions)

        # Add a submit button to the form
        submit_button = st.form_submit_button("Get Recommendation")

        # Get a song recommendation based on the selected weather when the form is submitted
        if submit_button:
            recommended_song = sm.song(selected_weather, weather_conditions, data)

            if "error" in recommended_song:
                st.error(recommended_song["error"])
            else:
                # Display the track name and provide a link to the song on Spotify
                track_name = recommended_song["name"]
                spotify_url = recommended_song["url"]

                st.markdown(f"**Recommended Song:** {track_name}")
                st.markdown(f"[Listen to this song on Spotify]({spotify_url})")

                # Additional Media Player Example (optional)
                st_player(url=spotify_url)
