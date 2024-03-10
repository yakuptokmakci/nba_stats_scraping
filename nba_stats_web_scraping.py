from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

options = Options()
##options.add_experimental_option("detach",True)     tarayıcı kapama
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

link = "https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"

def GetStats(link):
    stats = []
    driver.get(link)
    driver.maximize_window()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "stats_table")))

        table_rows = driver.find_elements(By.CLASS_NAME, "stats_table")[0].find_elements(By.TAG_NAME, "tr")
        
        # Tablo başlıklarını alalım
        table_headers = [header.text for header in table_rows[0].find_elements(By.TAG_NAME, "th")]

        # Her bir satırı işleyelim
        for row in table_rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            player_data = {}
            for i, cell in enumerate(cells):
                player_data[table_headers[i]] = cell.text
            stats.append(player_data)
    
    except Exception as e:
        print("Error Message:", e)
    
    return stats

def write_to_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

player_stats = GetStats(link)

desktop_path = r'C:\Users\yakup\OneDrive\Masaüstü\player_stats.json'

write_to_json(player_stats, desktop_path)

print("Veriler başarıyla 'player_stats.json' dosyasına yazıldı.")
