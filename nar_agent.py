import requests
from bs4 import BeautifulSoup
import yaml
import time

def load_config():
    with open('config.yml', 'r') as f:
        return yaml.safe_load(f)

def check_relevance(text, config):
    text = text.lower()
    core_hits = [w for w in config['keywords']['core'] if w in text]
    broad_hits = [w for w in config['keywords']['broad'] if w in text]
    
    if core_hits: return f"CORE (найдено: {', '.join(core_hits[:2])})"
    if broad_hits: return f"STRATEGIC (контекст: {', '.join(broad_hits[:2])})"
    return None

def scan_deep(url, config):
    try:
        print(f"--- Изучаю источник: {url} ---")
        res = requests.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Собираем все ссылки на странице
        links = set()
        for a in soup.find_all('a', href=True):
            link = a['href']
            # Оставляем только полные ссылки и убираем мусор
            if link.startswith('http') and not any(b in link.lower() for b in config['blocklist']):
                links.add(link)
        
        found_count = 0
        for link in list(links)[:15]: # Проверяем первые 15 глубоких ссылок для теста
            try:
                sub_res = requests.get(link, timeout=10)
                sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
                reason = check_relevance(sub_soup.get_text(), config)
                
                if reason:
                    print(f"   [!] Найдено релевантное: {link}")
                    print(f"       Почему: {reason}")
                    found_count += 1
                time.sleep(1) # Пауза, чтобы не забанили
            except: continue
            
        if found_count == 0:
            print("   На этой глубине ничего конкретного не найдено.")
            
    except Exception as e:
        print(f"Ошибка при сканировании {url}: {e}")

if __name__ == "__main__":
    cfg = load_config()
    for source in cfg['sources']:
        scan_deep(source, cfg)
