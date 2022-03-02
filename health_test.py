import pandas as pd 

df = pd.read_csv('https://raw.githubusercontent.com/joshnicholas/oz-covid-data/main/output/hospitalisations.csv')

df = df.loc[df['Date'] == df['Date'].max()]

p = df

print(p)
print(p.columns)