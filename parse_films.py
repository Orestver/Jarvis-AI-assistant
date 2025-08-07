

import requests
from bs4 import BeautifulSoup
import webbrowser

def search_and_open_film(query):
    search_url = "https://uakino.best/index.php?do=search"
    payload = {"subaction": "search", "story": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.post(search_url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("a", class_="movie-title")

    if not results:
        print("❌ Film not found.")
        return

    for result in results:
        film_url = result.get("href")
        film_name = result.text.strip()

        if "/franchise/" in film_url  or "/anime-series/" in film_url or "/news/" in film_url or "/anime-solo/" in film_name or "/animeukr/" in film_url:
            continue

        print(f"🎬 Found : {film_name}")
        print(f"🔗 Opening: {film_url}")
        webbrowser.open(film_url)
        return  



