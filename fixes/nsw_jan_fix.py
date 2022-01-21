# %%
import pandas as pd 
# pd.set_option("display.max_rows", 100)

# testo = "-testo"
testo = ''
# chart_key = f"oz-datablogs-something_random{igloo}{testo}"

fillo = 'https://raw.githubusercontent.com/M3IT/COVID-19_Data/master/Data/COVID_AU_state.csv'
#%%

data = pd.read_csv(fillo)
# 'date', 'state', 'state_abbrev', 'confirmed', 'confirmed_cum', 
# 'deaths', 'deaths_cum', 'tests', 'tests_cum', 'positives', 
# 'positives_cum', 'recovered', 'recovered_cum', 'hosp', 'hosp_cum', 
# 'icu', 'icu_cum', 'vent', 'vent_cum', 'vaccines', 'vaccines_cum'
#%%

df = data.copy()
df = df[['date', 'state', 'hosp_cum','icu_cum']]

df = df.loc[(df['date'] > "2022-01-14") & (df['date'] < "2022-01-19")]

## For checking
# df = df.loc[(df['date'] > "2022-01-11") & (df['date'] < "2022-01-13")]
# df = df.loc[df['state'] == "New South Wales"]

df['hosp_cum'] = pd.to_numeric(df['hosp_cum']) - pd.to_numeric(df['icu_cum'])

df = df[['state','hosp_cum', 'icu_cum', 'date' ]]
df.columns = ['Jurisdiction','Not in ICU','ICU','Date']


national = df.copy()
national = national.groupby(by=['Date'])['Not in ICU','ICU'].sum().reset_index()
national['Jurisdiction'] = "Australia"

combo = df.append(national)
combo.drop_duplicates(subset=['Date', 'Jurisdiction'], keep='last', inplace=True)
combo.sort_values(by=['Date'], inplace=True, ascending=True)

p = combo

with open('fixes/hospo_15_18_jan.csv', 'w') as f:
    combo.to_csv(f, index=False, header=True)

# vchecker = 'gdp_per_capita'
# print(p.loc[p[vchecker].isna()])
print(p)
# print(p['Jurisdiction'].unique().tolist())
print(p.columns.tolist())
# %%
