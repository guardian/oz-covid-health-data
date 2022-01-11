import pandas as pd 
import requests
from bs4 import BeautifulSoup as bs

import datefinder

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

## Read in on

old = pd.read_csv('output/nt_hospitalisations')

combo = old.append(new)

combo = combo.drop_duplicates(subset=['Date'],keep='last')

## Dump it

combo = combo.sort_values(by='Date', ascending=True)

with open('output/nt_hospitalisations', 'w') as f:
    combo.to_csv(f, index=False, header=True)