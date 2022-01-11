#%%
import requests
import dateparser
import pandas as pd
import time

from bs4 import BeautifulSoup as bs 
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Firefox(options=chrome_options)
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

#%%

listo = []

for page in range(1,7):

    start_url = f'https://coronavirus.nt.gov.au/updates?page={page}'

    print(f"Starting page{page}")
    driver.get(start_url)

    time.sleep(3)

    soup = bs(driver.page_source, 'html.parser')

    links = soup.find_all(class_='py-4')
    links = [x.a['href'] for x in links]

    print(f"There are {len(links)} links.")

    for link in links:
        r = requests.get(link)
        soup2 = bs(r.text, 'html.parser')

        datter = soup2.find(class_='publishedDate').text

        datto = dateparser.parse(datter)

        datto = datto.strftime('%Y-%m-%d')

        print(datto)

        stringo = ''
        texto = soup2.find_all("p")
        texto = [x.text for x in texto]

        # print(texto)

        for par in texto:
            if "in hospital" in par:
                stringo += par
                stringo += " "

        
        if len(stringo) > 1:
            print(stringo)

            data = [{'Date': datto, 'Text': stringo}]
            inter = pd.DataFrame.from_records(data)

            listo.append(inter)

            fin = pd.concat(listo)

            with open('archive/nt_scraping/scraped.csv', 'w') as f:
                fin.to_csv(f, index=False, header=True)




    # print(r.status_code)
    # print(links)
    # print(r.text)

# %%
