from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re

service = Service('/usr/bin/chromedriver')

chrome_options = Options()
chrome_options.binary_location = '/usr/bin/chromium-browser'
chrome_options.add_argument("--headless")
chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0')
chrome_options.page_load_strategy = 'eager'

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://finance.yahoo.com/calendar/earnings/")

base_url = "https://finance.yahoo.com/calendar/earnings"
symbol = "AAPL"
size = 25

driver.execute_script("""
    var buttons = document.querySelectorAll('button');
    for(var btn of buttons) {
        if(btn.textContent.includes('Accept') || btn.textContent.includes('Alle akzeptieren')) {
            btn.click(); break;
        }
    }
""")

page_string = BeautifulSoup(driver.page_source, 'html.parser').find(class_="total")
number_of_pages = page_string.get_text(strip=True).split()[-1]
# print(number_of_pages)

for offset in range(0, int(number_of_pages)): 
    driver.get(base_url)
    time.sleep(2) 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', attrs={'href': re.compile(r'/quote/[A-Z]+/')})
    for l in links:
        href = l.get("href")
        if href and href.startswith("http"):
            pass
        else:
            print(href)
            # driver.get(base_url + href)

    time.sleep(2) 

driver.quit()