
"""
url = "https://quotes.toscrape.com"  # Тестовий сайт

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.find_all("span", class_="text")
authors = soup.find_all("small", class_="author")

for quote, author in zip(quotes, authors):
    print(f"{quote.text} — {author.text}")
"""

import requests
from bs4 import BeautifulSoup
import webbrowser

def search_and_open_film(query):
    search_url = "https://uakino.best/index.php?do=search"
    payload = {"subaction": "search", "story": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.post(search_url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Знаходимо всі результати
    results = soup.find_all("a", class_="movie-title")

    if not results:
        print("❌ Фільм не знайдено.")
        return

    for result in results:
        film_url = result.get("href")
        film_name = result.text.strip()

        # Ігноруємо франшизи та мультфільми
        if "/franchise/" in film_url  or "/anime-series/" in film_url or "/news/" in film_url or "/anime-solo/" in film_name or "/animeukr/" in film_url:
            continue

        print(f"🎬 Знайдено фільм: {film_name}")
        print(f"🔗 Відкриваю: {film_url}")
        webbrowser.open(film_url)
        return  # Відкриваємо тільки перший відповідний фільм

    print("❌ Не знайдено відповідного фільму без франшиз чи мультфільмів.")

