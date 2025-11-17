import streamlit as st
from yelp_api import search_cafes
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Cafe Compass", page_icon="☕")

# 🔁 Persist results across reruns
if "results" not in st.session_state:
    st.session_state.results = []

st.title("☕ Cafe Compass")
st.subheader("Find your perfect coffee spot anywhere in the world 🌍")

# --- Input Form ---
with st.form("location_form"):
    location = st.text_input("📍 Enter a location (e.g. Kansas City, Tokyo, Paris):", "")
    limit = st.slider("☕ Number of cafés to search:", 5, 30, 10)
    open_now = st.checkbox("🕒 Only show cafés open now?")
    min_rating = st.slider("⭐ Minimum rating:", 1.0, 5.0, 3.5, 0.5)
    submit = st.form_submit_button("🔍 Search Cafés")

# --- Search logic on submit ---
if submit and location:
    with st.spinner("Finding cozy cafés..."):
        st.session_state.results = search_cafes(
            location,
            limit=limit,
            open_now=open_now
        )

# --- If results exist, apply rating filter and display ---
if st.session_state.results:
    results = st.session_state.results

    # ⭐ Filter by rating
    results = [cafe for cafe in results if cafe.get("rating", 0) >= min_rating]

    if not results:
        st.warning(f"No cafés match your filters in {location}. Try adjusting rating or filters.")
    else:
        st.success(f"Found {len(results)} cafés in {location} matching your filters!")

        # 🟢 Open Now Label
        if open_now:
            st.info("🟢 Only showing cafés that are currently open now.")

        # --- MAP AT TOP ---
        st.subheader("🗺️ Map View")

        first_cafe = results[0]
        lat = first_cafe["coordinates"]["latitude"]
        lon = first_cafe["coordinates"]["longitude"]
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

        st_folium(cafe_map, width=700, height=500)

        # --- Café Cards BELOW ---
        for cafe in results:
            st.markdown("----")
            col1, col2 = st.columns([1, 2])

            with col1:
                image_url = cafe.get("image_url")
                if image_url:
                    st.image(image_url, width=250)
                else:
                    st.write("🖼️ No image available")

            with col2:
                st.markdown(f"### ☕ {cafe['name']}")
                st.write(f"📍 **Address:** {', '.join(cafe['location']['display_address'])}")
                st.write(f"⭐ **Rating:** {cafe['rating']} | 📞 **Phone:** {cafe.get('phone', 'N/A')}")
                st.markdown(f"[🔗 View on Yelp]({cafe['url']})")