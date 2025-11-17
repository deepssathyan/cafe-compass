import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YELP_API_KEY")
API_URL = "https://api.yelp.com/v3/businesses/search"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}

def search_cafes(location, term="cafe", limit=10, open_now=False):
    params = {
        "term": term,
        "location": location,
        "categories": "cafes,coffee",
        "limit": limit,
        "sort_by": "rating"
    }

    if open_now:
        params["open_now"] = True

    response = requests.get(API_URL, headers=HEADERS, params=params)

    if response.status_code != 200:
        return {"error": response.json()}

    return response.json()["businesses"]