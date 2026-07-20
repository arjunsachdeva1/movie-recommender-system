# 🎬 CineMatch — AI Movie Recommendation Engine

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://movie-recommender-system.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Git LFS](https://img.shields.io/badge/Git_LFS-Enabled-FO5032?style=flat&logo=git&logoColor=white)](https://git-lfs.github.com/)

**CineMatch** is an end-to-end, machine-learning-powered movie recommendation system. By analyzing text vector embeddings and calculating cosine similarity metrics across thousands of titles, the app generates instant personalized recommendations complete with real-time posters, titles, and ratings via the TMDB REST API.

---

## ✨ Features

* 🧠 **Vector Similarity Engine:** Uses `CountVectorizer` and cosine similarity to match movies based on genres, plot keywords, cast, and crew.
* 🖼️ **Live TMDB Metadata & Posters:** Dynamically fetches high-resolution posters, user ratings, and details using asynchronous REST calls.
* 🔍 **Smart Fallback System:** Title-search fallback logic handles missing or invalid TMDB IDs smoothly without breaking the UI grid.
* ⚡ **Performance Caching:** Leverages `@st.cache_data` to minimize API latency and deliver sub-second recommendation loading.
* 🎨 **Glassmorphism UI:** Custom-styled dark mode interface with responsive multi-column layouts and dynamic card states.
* 📦 **Git LFS Architecture:** Tracks and deploys large binary model matrices ($>100\text{ MB}$) directly to Streamlit Community Cloud.

---

## 🛠️ Tech Stack & Architecture

| Domain | Tools & Technologies |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **Frontend UI** | Streamlit, HTML5, Custom CSS |
| **Machine Learning & NLP** | Scikit-Learn (`CountVectorizer`, Cosine Similarity), Pandas, NumPy |
| **Data Serialization** | Pickle (`.pkl`) |
| **External API** | TMDB REST API (`requests`) |
| **Version Control & Hosting** | Git, Git LFS, GitHub, Streamlit Community Cloud |

---

## 📁 Repository Structure

```text
├── app.py                   # Streamlit frontend & application logic
├── requirements.txt         # Production dependencies for cloud deployment
├── .gitattributes          # Git LFS tracking configuration for large datasets
├── movie_dict.pkl           # Processed movie metadata dictionary
├── similarity.pkl           # Cosine similarity matrix (Managed via Git LFS)
└── README.md                # Project documentation
