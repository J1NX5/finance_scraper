from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd

service = Service('/usr/bin/chromedriver')

chrome_options = Options()
chrome_options.binary_location = '/usr/bin/chromium-browser'
chrome_options.add_argument("--headless")
chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0')
chrome_options.page_load_strategy = 'eager'

driver = webdriver.Chrome(service=service, options=chrome_options)

base_url = "https://finance.yahoo.com/calendar/earnings"
fin_base_url = "https://finance.yahoo.com"

driver.get(base_url)

driver.execute_script("""
    var buttons = document.querySelectorAll('button');
    for(var btn of buttons) {
        if(btn.textContent.includes('Accept') || btn.textContent.includes('Alle akzeptieren')) {
            btn.click(); break;
        }
    }
""")

page_string = BeautifulSoup(driver.page_source, 'html.parser').find(class_="total")

if page_string is None:
    number_of_pages = "1"
else:
    number_of_pages = page_string.get_text(strip=True).split()[-1]

# in earning_data is the final result
earning_data = dict()
for offset in range(0, int(number_of_pages)): 
    driver.get(base_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    section = soup.find('section', class_='main yf-93c5lg')
    links = section.find_all('a', attrs={'href': re.compile(r'/quote/[A-Z]+/')})
    for l in links:
        # at this point we need to extract the symbol from the link
        href = l.get("href")

        # filter symbol
        parts = [p for p in href.split("/") if p]
        symbol = parts[-1]
        print(f'Symbol: {symbol}')

        if href and href.startswith("http"):
            pass
        else:
            # print(fin_base_url + href + "financials/")
            driver.get(fin_base_url + href + "financials/")
            soup_l2 = BeautifulSoup(driver.page_source, 'html.parser')
            # print(soup_l2.get_text(strip=True))
            driver.execute_script("""
                var buttons = document.querySelectorAll('button');
                for(var btn of buttons) {
                    if(btn.textContent.includes('Quarterly')){
                        btn.click(); break;
                    }
                }
            """)
            section_l2 = soup_l2.find('section', class_='finContainer yf-yuwun0')
            # print(section_l2)
            # column = section_l2.find_all(class_="column")
            row = section_l2.find_all(class_="row")
            data = []
            for r in row:
                column = r.select("div.column")
                values = [c.get_text(strip=True) for c in column]
                # earning_data[symbol] = [c.get_text(strip=True) for c in columns]
                data.append(values)
                # print(data)
            header = data[0]
            data = data[1:]
            df = pd.DataFrame(data, columns=header)
            #print(df[["TTM"]])  
            print(df.to_string()) 

        
    time.sleep(2) 

driver.quit()