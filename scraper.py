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
chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0')
chrome_options.page_load_strategy = 'normal'

driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://finance.yahoo.com/calendar/earnings?offset=0&symbol=AAPL")

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
time.sleep(3)

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-ylk*='qte']"))
)

time.sleep(3)

for offset in range(0, 109, size): 
    url = f"{base_url}?offset={offset}&symbol={symbol}"
    driver.get(url)
    time.sleep(5) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', attrs={'href': re.compile(r'/quote/[A-Z]+/')})
    for l in links:
        print(l)


driver.quit()