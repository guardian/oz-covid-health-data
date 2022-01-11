import csv
import re
import pandas as pd

pattern = "\d+"

listo = []
with open('archive/nt_scraping/scraped.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        datto = row[0]
        texto = row[1]

        texto = texto.replace("COVID-19", "Covid")
        texto = texto.split(",")
        texto = [x for x in texto if "in hospital" in x]

        texto = "".join(texto)

        num = re.search('\d+', texto, re.IGNORECASE).group(0)

        data = [{'Date': datto, 'In hospital': num}]
        inter = pd.DataFrame.from_records(data)

        listo.append(inter)

fin = pd.concat(listo)

with open('archive/nt_hospitalisations', 'w') as f:
    fin.to_csv(f, index=False, header=True)




