import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://vpuzo.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}
DATA_FILE = "data.json"

def get_categories():
    url = BASE_URL  # Главная страница, где находятся категории
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("Ошибка при загрузке категорий")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    categories = []

    # Находим категории в div class="subnav-header"
    for category in soup.select(".subnav-header a"):
        print(f"Category: {category} \n")
        category_name = category.text.strip()
        category_link = category["href"]
        if category_link.startswith("/"):
            category_link = BASE_URL + category_link

        categories.append({"category": category_name, "category_link": category_link, "recipes": []})

    return categories

def update_data_json():
    categories = get_categories()

    if not categories:
        print("Категории не найдены.")
        return

    # Загружаем старый data.json
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []  # Если файла нет или он пустой, создаем пустой список

    # Обновляем data.json новыми категориями
    updated_data = []
    existing_categories = {entry["category"] for entry in data}

    for category in categories:
        if category["category"] not in existing_categories:
            updated_data.append(category)

    # Добавляем новые категории к старым
    data.extend(updated_data)

    # Записываем обновленный JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Файл {DATA_FILE} обновлен. Добавлено {len(updated_data)} новых категорий.")

if __name__ == "__main__":
    update_data_json()
