#
import os
import pickle
import streamlit as st
import pandas as pd
import requests

# Function to fetch movie poster
# def fetch_poster(movie_id):
#     # url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=90cfbb784b8f78febf99989ccfcbd340&language=en-US"
#     response = requests.get(url)
#     data = response.json()
#     poster_path = data.get('poster_path')
#     if poster_path:
#         full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#         return full_path
#     else:
#         return "https://via.placeholder.com/500x750?text=No+Image"

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        # recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names


# Streamlit UI
st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# If the loaded movie dict is a dict, convert to DataFrame
if isinstance(movies, dict):
    movies = pd.DataFrame(movies)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select a movie from the dropdown to get recommendations",
    movie_list
)

# Show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names= recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            # st.image(recommended_movie_posters[i])


def download_file_from_url(url, filename):
    if not os.path.exists(filename):
        print(f"Downloading {filename} from {url}...")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

similarity_url = "https://drive.google.com/uc?export=download&id=1LAicDLRTFjOsM1LcS2TYgVA6p9eo044c"
download_file_from_url(similarity_url, "similarity.pkl")
