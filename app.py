import streamlit as st
import pickle
import pandas as pd
import requests

# ---------------------------------------------------------
# Page Config
# ---------------------------------------------------------
st.set_page_config(
    page_title="CineMatch | AI Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Premium Ultra-Modern Custom CSS
# ---------------------------------------------------------
st.markdown("""
    <style>
    /* Global Page Styling */
    .stApp {
        background: linear-gradient(135deg, #0b0d17 0%, #111528 50%, #0d0f1d 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Title & Subtitle Container */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
    }
    
    .main-title {
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8f3d 50%, #e056fd 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        color: #8f9cae;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Dropdown Label & Styling */
    div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #ff4b4b !important;
        box-shadow: 0 0 15px rgba(255, 75, 75, 0.2);
    }

    /* Primary Recommend Button */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff6b6b 100%);
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 20px rgba(255, 75, 75, 0.4);
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(255, 75, 75, 0.7);
        background: linear-gradient(90deg, #ff6b6b 0%, #ff4b4b 100%);
    }

    /* Fixed Aspect Ratio Movie Poster Image Container */
    div[data-testid="stImage"] img {
        border-radius: 16px !important;
        aspect-ratio: 2 / 3 !important;
        object-fit: cover !important;
        width: 100% !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    div[data-testid="stImage"] img:hover {
        transform: scale(1.05) translateY(-8px) !important;
        box-shadow: 0 15px 35px rgba(255, 75, 75, 0.35) !important;
        border-color: rgba(255, 75, 75, 0.5) !important;
    }

    /* Movie Title Cards */
    .movie-card-title {
        color: #ffffff;
        font-weight: 700;
        font-size: 1rem;
        text-align: center;
        height: 2.8rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        margin-top: 0.8rem;
        margin-bottom: 0.3rem;
        line-height: 1.3;
    }

    /* Rating Tag */
    .movie-rating {
        background: rgba(255, 193, 7, 0.15);
        border: 1px solid rgba(255, 193, 7, 0.3);
        color: #ffc107;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        text-align: center;
        width: fit-content;
        margin: 0 auto;
    }

    /* Hide Streamlit Header & Footer for Clean UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 1. API Helper Function with Cache & Ratings
# ---------------------------------------------------------
@st.cache_data
def fetch_poster_and_rating(movie_id, title=None):
    fallback_poster = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=500&auto=format&fit=crop"
    api_key = "87dfe04d496c4397dfe32aac3a9b371c"
    
    try:
        # 1. Try fetching by movie_id first
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            vote_average = data.get('vote_average', 0.0)
            
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else fallback_poster
            rating_str = f"★ {round(vote_average, 1)}" if vote_average else "★ N/A"
            return poster_url, rating_str

        # 2. Backup: Search by Title if ID lookup failed (404)
        if title:
            search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={requests.utils.quote(title)}"
            search_res = requests.get(search_url, timeout=5)
            if search_res.status_code == 200:
                results = search_res.json().get('results', [])
                if results:
                    top_match = results[0]
                    poster_path = top_match.get('poster_path')
                    vote_average = top_match.get('vote_average', 0.0)
                    
                    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else fallback_poster
                    rating_str = f"★ {round(vote_average, 1)}" if vote_average else "★ N/A"
                    return poster_url, rating_str

        return fallback_poster, "★ N/A"
            
    except Exception:
        return fallback_poster, "★ N/A"
# ---------------------------------------------------------
# 2. Recommendation Logic Function
# ---------------------------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    
    for i in movies_list:
        movie_row = movies.iloc[i[0]]
        rec_title = movie_row['title']
        recommended_movies.append(rec_title)
        
        # Get ID safely
        if 'movie_id' in movie_row:
            movie_id = movie_row['movie_id']
        elif 'id' in movie_row:
            movie_id = movie_row['id']
        else:
            movie_id = movie_row.name 
            
        poster, rating = fetch_poster_and_rating(movie_id, title=rec_title)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)
        
    return recommended_movies, recommended_posters, recommended_ratings
# ---------------------------------------------------------
# 3. Load Datasets
# ---------------------------------------------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------------------------------------------
# 4. Streamlit UI Layout
# ---------------------------------------------------------
# Header Section
st.markdown("""
    <div class="main-header">
        <div class="main-title">CINEMATCH</div>
        <div class="main-subtitle">Discover your next favorite movie using AI recommendations</div>
    </div>
""", unsafe_allow_html=True)

# Selection Row
col_search, col_btn = st.columns([3, 1])

with col_search:
    selected_movie_name = st.selectbox(
        'Select or search a movie',
        movies['title'].values,
        label_visibility="collapsed"
    )

with col_btn:
    button_clicked = st.button('Get Recommendations 🚀')

# Display Section
if button_clicked:
    names, posters, ratings = recommend(selected_movie_name)
    
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.image(posters[i], use_container_width=True)
            st.markdown(f'<div class="movie-card-title">{names[i]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="movie-rating">{ratings[i]}</div>', unsafe_allow_html=True)