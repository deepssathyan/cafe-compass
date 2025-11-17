# cafe-compass

# ☕ Cafe Compass • Streamlit App
![GitHub stars](https://img.shields.io/github/stars/deepssathyan/cafe-compass?style=social)


> Find the perfect café anywhere in the world — complete with filters, maps, images, and real-time data from Yelp.
<p align="center">
  <img src="https://i.pinimg.com/originals/0f/8e/10/0f8e10b4dc9707d222113df0aec0bf2f.gif" width="500"/>
</p>

---

## 🔍 Features

- 🌍 Search for cafés anywhere in the world by city
- 🎯 Filter by:
  - "Open Now" status
  - Minimum star rating
- 🗺️ Interactive map view (with Folium)
- 🧁 Beautiful side-by-side cards with:
  - Café photo
  - Address, rating, contact
  - Yelp link
- 🧠 Results persist on rerun using Streamlit session state

---

## ⚙️ Tech Stack

| Layer        | Tool                     |
|--------------|--------------------------|
| UI           | Streamlit                |
| Maps         | Folium + streamlit-folium|
| Backend      | Python                   |
| External API | Yelp Fusion API          |
| Utils        | requests, dotenv         |

---

## 🚀 Live Demo
> 🧪 If you're running locally:

---
## 🛣️ Roadmap: Cafe Compass 2.0

- [ ] 🧠 Mood-based café recommendations  
- [ ] 💬 AI-powered review summaries  
- [ ] 🎨 Theme switcher (dark / pastel)  
- [ ] 🏷️ Tags (vegan, quiet, study-friendly)  
- [ ] 💾 Save favorites to CSV  
- [ ] 📍 Distance from user location  
- [ ] 🔐 Optional login / personalization  

```bash
git clone https://github.com/your-username/cafe-compass.git
cd cafe-compass
pip install -r requirements.txt
streamlit run app.py    
