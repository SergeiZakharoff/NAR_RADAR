import requests
from bs4 import BeautifulSoup
import yaml
import json
import os
from datetime import datetime

def load_config():
    with open('config.yml', 'r') as f:
        return yaml.safe_load(f)

def analyze_page(url, config):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        title = soup.title.string if soup.title else ""
        
        # Проверка на прямое попадание (Aging)
        is_core = any(w in text for w in config['keywords']['core'])
        # Проверка на широкую рамку (Social)
        is_broad = any(w in text for w in config['keywords']['broad'])
        
        if is_core: return "CORE: Прямое соответствие НАР"
        if is_broad: return "STRATEGIC: Широкая социальная рамка"
        return None
    except:
        return None

def run_scout():
    config = load_config()
    print(f"Запуск сканирования: {datetime.now()}")
    
    # В этом простом примере мы сканируем только главные страницы источников
    for url in config['sources']:
        res = analyze_page(url, config)
        if res:
            print(f"НАЙДЕНО: {url} | Тип: {res}")

if __name__ == "__main__":
    run_scout()
