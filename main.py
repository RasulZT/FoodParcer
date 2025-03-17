import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://vpuzo.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Файл, куда будем сохранять рецепты
OUTPUT_FILE = "recipes_vpuzo.json"

def get_categories():
    url = f"{BASE_URL}/category"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("Ошибка при загрузке категорий")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    categories = []

    # Ищем ссылки на категории (по анализу HTML)
    for category in soup.select(".cat-menu a"):
        category_name = category.text.strip()
        category_link = category["href"]
        if category_link.startswith("/"):
            category_link = BASE_URL + category_link
        categories.append({"name": category_name, "link": category_link})

    return categories

