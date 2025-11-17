import os
import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_folium import st_folium
import folium

# Load environment variables
load_dotenv()

# Streamlit page settings
st.set_page_config(page_title="Cafe Compass", page_icon="☕", layout="wide")

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Gloria+Hallelujah&display=swap" rel="stylesheet">
    <h1 style='text-align: center;
               color: #BAB86C;
               font-family: "Gloria Hallelujah", cursive;
               font-size: 4em;
               margin-top: -20px;'>
        Cafe Compass
    </h1>
""", unsafe_allow_html=True)


# Hero-style GIF — same dimensions & layout as Cafe Corazón
st.markdown(
    """
    <div style="display: flex; justify-content: center; padding: 0;">
        <img src="https://i.pinimg.com/originals/0f/8e/10/0f8e10b4dc9707d222113df0aec0bf2f.gif" 
             style="width: 100%; max-width: 1280px; height: 500px; object-fit: cover; border-radius: 16px; margin-top: -10px;">
    </div>
    """,
    unsafe_allow_html=True
)



# Yelp API key
yelp_api_key = os.getenv("YELP_API_KEY")

# Function to call Yelp API
def search_cafes(location, limit=10, min_rating=0, open_now=False):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {yelp_api_key}"}
    params = {
        "term": "cafes",
        "location": location,
        "limit": limit,
        "sort_by": "best_match",
    }
    if open_now:
        params["open_now"] = True

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    businesses = data.get("businesses", [])
    return [b for b in businesses if b["rating"] >= min_rating]

# Sidebar filters
with st.sidebar:
    st.header("🔍 Search Filters")
    location = st.text_input("Enter a city or location", value="Seattle")
    num_results = st.selectbox("Number of cafés to show", options=[5, 10, 15, 20, 25], index=1)
    min_rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.5)
    open_now = st.checkbox("Only show cafes that are open now")
    search = st.button("Search Cafes")

# Perform search
if search and location:
    st.session_state.results = search_cafes(
        location=location,
        limit=num_results,
        min_rating=min_rating,
        open_now=open_now
    )

results = st.session_state.get("results", [])

# Map View
if results:
    first = results[0]
    lat = first["coordinates"]["latitude"]
    lon = first["coordinates"]["longitude"]
    cafe_map = folium.Map(location=[lat, lon], zoom_start=13)

    for cafe in results:
        name = cafe["name"]
        rating = cafe["rating"]
        address = ", ".join(cafe["location"]["display_address"])
        phone = cafe.get("display_phone", "N/A")
        lat = cafe["coordinates"]["latitude"]
        lon = cafe["coordinates"]["longitude"]

        popup = f"""
        <b>{name}</b><br>
        ⭐ Rating: {rating}<br>
        📍 {address}<br>
        📞 {phone}
        """
        folium.Marker(
            location=[lat, lon],
            popup=popup,
            tooltip=name,
            icon=folium.Icon(color="green", icon="coffee", prefix='fa')
        ).add_to(cafe_map)

    # Centered with rounded container
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(
            "<div style='border-radius: 20px; overflow: hidden;'>",
            unsafe_allow_html=True
        )
        st_folium(cafe_map, width=700, height=500)
        st.markdown("</div>", unsafe_allow_html=True)

# Cafe Cards
if results:
    st.subheader("📍 Cafe Results")
    for cafe in results:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(cafe["image_url"], width=100)
        with col2:
            st.markdown(f"### {cafe['name']}")
            st.markdown(f"⭐ **Rating**: {cafe['rating']} &nbsp;&nbsp;&nbsp; 📞 **Phone**: {cafe.get('display_phone', 'N/A')}")
            st.markdown(f"📍 {' ,'.join(cafe['location']['display_address'])}")
            st.markdown(f"🌐 [Yelp Page]({cafe['url']})")