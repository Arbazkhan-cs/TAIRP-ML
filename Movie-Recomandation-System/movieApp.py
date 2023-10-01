# Using StreamLit for the app
import streamlit as st
import pickle
import pandas as pd
import requests

# loading the Movie Dictionary
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# Adding Title
st.title("Movie Recommender System")


# function for recommendation
similarities = pickle.load(open("similarities.pkl", "rb"))


def recommend(movie):
    movie_idx = movies[movies["title"] == movie].index[0]
    distance = similarities[movie_idx]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_path = []
    for i in movies_list:
        # fetch poster from api
        recommend_movies_path.append(fetch_poster(movies.iloc[i[0]].id))
        # fetch titles
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movies_path


# Function For Fetching Posters
def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US")
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


# Adding select box
select_movie_name = st.selectbox(
    'Select Movie Name:',
    movies["title"].values
)

# Adding a recommendation Button
if st.button('Recommend'):
    name, posters = recommend(select_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])

    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])
