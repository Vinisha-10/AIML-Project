import pickle
import streamlit as st
import requests

OMDB_API_KEY = "d497dd19" # This is the key you provided in your original fetch_poster

def fetch_poster(movie_title, omdb_api_key_param):

    url = f"http://www.omdbapi.com/?apikey={omdb_api_key_param}&t={movie_title}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get('Response') == 'True' and data.get('Poster') and data['Poster'] != 'N/A':
            return data['Poster'] 
        else:
            error_msg = data.get('Error', 'No poster/movie found in OMDb for this title.')
            
            return "https://via.placeholder.com/200x300?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        
        return "https://via.placeholder.com/200x300?text=Error+Fetching+Poster" 
    except ValueError:
        
        return "https://via.placeholder.com/200x300?text=Data+Error" 

def recommend(movie):
    recommended_movie_names = []
    recommended_movie_posters = []

    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error(f"Movie '{movie}' not found in the dataset. Please select a valid movie.")
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    for i in distances[1:6]:

        movie_title = movies.iloc[i[0]]['title']

        recommended_movie_names.append(movie_title)

        poster_url = fetch_poster(movie_title, OMDB_API_KEY)
        recommended_movie_posters.append(poster_url)

    return recommended_movie_names, recommended_movie_posters

st.header('Movie Recommender System')

try:
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))
    st.success("Movies DataFrame and Similarity Matrix loaded successfully!")
except FileNotFoundError:
    st.error("Error: 'movie_list.pkl' or 'similarity.pkl' not found.")
    st.info("Please ensure these files are in the same directory as your Streamlit app.")
    st.stop() 

if 'title' not in movies.columns:
    st.error("Error: 'movie_list.pkl' DataFrame does not contain a 'title' column.")
    st.info("The app requires a 'title' column to fetch movie posters from OMDb.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    if OMDB_API_KEY == "YOUR_OMDB_API_KEY_HERE" or not OMDB_API_KEY:
        st.warning("Please ensure your OMDb API key is correctly set in the code!")
        st.info("You provided 'd497dd19', so just make sure it's valid.")
    
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names: 
        cols = st.columns(5)
        for idx in range(min(len(recommended_movie_names), 5)):
            with cols[idx]:
                st.text(recommended_movie_names[idx])
                st.image(recommended_movie_posters[idx], width=150)
    else:
        st.info("No recommendations generated for the selected movie, or an error occurred.")