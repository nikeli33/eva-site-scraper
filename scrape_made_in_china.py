import requests
from bs4 import BeautifulSoup
import time
import random
from pathlib import Path

# Список популярных User-Agent для имитации разных браузеров
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_2 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
]

def fetch_page(url, retries=3):
    """
    Загружает страницу с повторами и случайным User-Agent.
    """
    for attempt in range(retries):
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            elif response.status_code in [429, 503]:
                wait = 2 ** attempt
                print(f"[WARN] Код {response.status_code} — retry {attempt+1}/{retries} after {wait}s")
                time.sleep(wait)
            else:
                print(f"[ERROR] Неожиданный статус: {response.status_code}")
                break
        except requests.RequestException as e:
            print(f"[ERROR] Ошибка сети: {e}")
            time.sleep(2)
    return None

def scrape_made_in_china_companies(category_url, pages=5, delay=1.0):
    companies = set()
    for page in range(1, pages + 1):
        url = f"{category_url}?page={page}"
        print(f"Fetching: {url}")

        html = fetch_page(url)
        if not html:
            print(f"[FAIL] Не удалось загрузить страницу {page}")
            break

        soup = BeautifulSoup(html, 'html.parser')

        for item in soup.select('a.compnay-name span'):
            companies.add(item.get_text(strip=True))

        jitter = random.uniform(0.5, delay)
        time.sleep(delay + jitter)

    return companies

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    OUTPUT_PATH = BASE_DIR / "companies.txt"

    category = "https://www.made-in-china.com/Consumer-Electronics-Catalog/Mobile-Phone.html"
    print("Собираем компании...")
    company_names = scrape_made_in_china_companies(category, pages=10, delay=1.5)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for name in sorted(company_names):
            f.write(name + "\n")

    print(f"\n✅ Готово! Собрано компаний: {len(company_names)}")
    print(f"📄 Список сохранён в {OUTPUT_PATH.name}")
