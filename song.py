import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import pandas as pd

# Initialize Spotify API with client credentials
client_credentials_manager = SpotifyClientCredentials(
    client_id='fbe0872020b147bb9184bbeb34c0026e', client_secret='3c370a4df64f4a23ab343d6fabacf184')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def load_data(dataset_path="spotify_weather_data.csv"):
    """
    Load the dataset and return the dataframe along with unique weather types.

    Parameters:
    - dataset_path: Path to the CSV dataset.

    Returns:
    - df: DataFrame containing the dataset.
    - weathers: Array of unique weather conditions.
    """
    df = pd.read_csv(dataset_path)
    weathers = pd.unique(df['Weather'])
    return df, weathers


def get_weather(weathers):
    """
    Return the weather inputted by the user (or another function).

    Parameters:
    - weathers: Array of unique weather conditions.

    Returns:
    - weather: String representing the weather selected by the user.
    """
    weather = input(f"Enter the weather from the options {
                    ', '.join(weathers)}: ")
    return weather


def song(weather, weathers, df):
    """
    Return a random song for the given weather if it exists in the dataset.

    Parameters:
    - weather: String representing the weather condition.
    - weathers: Array of unique weather conditions.
    - df: DataFrame containing the dataset.

    Returns:
    - A dictionary with the song name and track ID, or an error message.
    """
    if weather not in weathers:
        return {"error": f"'{weather}' is not a valid weather type. Please choose from {', '.join(weathers)}."}
    else:
        filtered_df = df[df['Weather'] == weather]
        if filtered_df.empty:
            return {"error": f"No songs found for the weather '{weather}'."}
        else:
            random_song = filtered_df.sample(n=1).iloc[0]
            track_name = random_song['Track Name']
            results = sp.search(q=track_name, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                return {"name": track['name'], "id": track['id'], "url": track['external_urls']['spotify']}
            else:
                return {"error": f"Song '{track_name}' not found on Spotify."}


if __name__ == '__main__':
    df, weathers = load_data()
    weather = get_weather(weathers)
    result = song(weather, weathers, df)
    if "error" in result:
        print(result["error"])
    else:
        print(f"Random song for {weather}: {
              result['name']} (Spotify URL: {result['url']})")