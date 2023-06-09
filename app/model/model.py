import pickle
from pathlib import Path
#import traceback
# import streamlit as st
import pandas as pd




__version__ = "1.0.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent


#TODO: GET THE SURVEY DATA

#load the books dataset model
books_genres_pkl = pickle.load(open(f"{BASE_DIR}/books_genres_df-{__version__}.pkl", "rb"))

books_genres_df = pd.DataFrame(books_genres_pkl)

#Load the survey dataset model:
genre_weights_pkl = pickle.load(open(f"{BASE_DIR}/genre_weights_df-{__version__}.pkl", "rb"))

genre_weights_df = pd.DataFrame(genre_weights_pkl)



#TODO: TEST THE MODELS
# print("Genre Weights Model: ",genre_weights_df.head())
# print("Books Genres Model: ",books_genres_pkl.head())



# A function to return the the top genres for a given emotion
def get_top_genres(emotion, top_genres_count):
    return genre_weights_df[emotion].sort_values(ascending=False).head(top_genres_count).index.tolist()


def recommend(emotion, books_count):
    # Get the genre weights for the given emotion
    genre_weights = genre_weights_df[emotion]
    
    # Sort the genre weights in descending order
    genre_weights = genre_weights.sort_values(ascending=False)
    
    # Get the top genres based on the weights
    top_genres = genre_weights.index.tolist()
    
    # Calculate the weight multiplier for each genre based on its position in the top_genres list
    weight_multiplier = [1 / (i+1) for i in range(len(top_genres))]
    
    # Calculate the weighted genre weights for each genre
    weighted_genre_weights = genre_weights * weight_multiplier
    
    # Sort the weighted genre weights in descending order
    weighted_genre_weights = weighted_genre_weights.sort_values(ascending=False)
    
    # Select the top genres based on the weighted genre weights
    top_genres_weighted = weighted_genre_weights.index.tolist()[:5]
    
    # Filter books dataframe based on top genres
    filtered_books = books_genres_df[books_genres_df['Genres'].apply(lambda genres: any(genre in genres for genre in top_genres_weighted))]
    
    # Get the desired number of books
    recommended_books = filtered_books['ISBN'].tolist()[:books_count]
    
    return recommended_books