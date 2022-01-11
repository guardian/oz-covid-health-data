import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs

import datefinder

print("Running NT Health Scraper")

r = requests.get('https://coronavirus.nt.gov.au/current-status#covid-19-data')

soup = bs(r.text, 'html.parser')

sec = soup.find(class_='covid-card-stats mt-2 mb-5')
cards = sec.find_all(class_='au-card')

## Find updated date

stringo = ''
texto = soup.find_all("p")
texto = [x.text for x in texto]
for par in texto:
    if "Data updated" in par:
        stringo += par
        stringo += " "

datter = datefinder.find_dates(stringo)
datto = ''

for match in datter:
    datto = match

datto = datto.strftime('%Y-%m-%d')

### Grab the actual data

for card in cards:
    texto = card.find(class_='au-display-md').text.strip()

    if texto == 'in hospital':

        num = card.find(class_='au-display-xxxl').text.strip()

data = [{'Date': datto, 'In hospital': num}]
new = pd.DataFrame.from_records(data)

## Read in archive
archive = 'archive/nt_scraping/nt_hospitalisations_archive.csv'

old = pd.read_csv(archive)

combo = old.append(new)

combo = combo.drop_duplicates(subset=['Date'],keep='last')

## Dump it

combo = combo.sort_values(by='Date', ascending=True)

with open(archive, 'w') as f:
    combo.to_csv(f, index=False, header=True)


# combo['Date'] = pd.to_datetime(combo['Date'])
# combo['Date'] = combo['Date'] + pd.DateOffset(days=1)
# combo['Date'] = combo['Date'].dt.strftime("%Y-%m-%d")

### Output official 

hospo = pd.read_csv('output/hospitalisations.csv')

nt = hospo.loc[hospo['Jurisdiction'] == "NT"]

tog = pd.merge(combo, nt, on='Date', how='left')

tog = tog[['Date', 'In hospital', 'ICU']]

### Dump it

with open('output/nt_hospitalisations.csv', 'w') as f:
    tog.to_csv(f, index=False, header=True)

p = tog

# print(p)
# print(p.columns)
