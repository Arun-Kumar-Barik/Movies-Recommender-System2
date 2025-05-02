import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Download similarity.pkl from Google Drive (direct link)
def download_file_from_url(url, filename):
    if not os.path.exists(filename):
        st.write(f"Downloading {filename}...")
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

similarity_url = "https://drive.google.com/uc?export=download&id=1LAicDLRTFjOsM1LcS2TYgVA6p9eo044c"
download_file_from_url(similarity_url, "similarity.pkl")

# Load movie data and similarity matrix
movies = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = pd.DataFrame(movies)

# Recommendation function
def recommend(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = [movies_list.iloc[i[0]].title for i in distances[1:6]]
    return recommended_movies

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie', movies_list['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.subheader("Top 5 Recommended Movies:")
    for i, name in enumerate(recommendations, 1):
        st.write(f"{i}. {name}")
