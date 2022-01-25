#%%
import requests
import pandas as pd
import numpy as np
import datetime
pd.set_option("display.max_rows", 100)


# %%
# Read in Anthony's data
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get('https://covidlive.com.au/covid-live.json', headers=headers)

data = r.json()
df = pd.read_json(r.text)
df = df.sort_values(by='REPORT_DATE', ascending=True)

df = df[['REPORT_DATE', 'CODE', 'ACTIVE_CNT', 'CASE_CNT', 'DEATH_CNT', 'TEST_CNT', 'MED_HOSP_CNT', 'MED_ICU_CNT', 'NAME', 'PREV_ACTIVE_CNT', 'PREV_CASE_CNT', 'PREV_DEATH_CNT', 'PREV_TEST_CNT', 'PREV_MED_HOSP_CNT', 'PREV_MED_ICU_CNT', 'NEW_CASE_CNT', 
'PREV_NEW_CASE_CNT', 'LAST_UPDATED_DATE']]

df = df.loc[(df['REPORT_DATE'] >= "2022-01-15") & (df['REPORT_DATE'] <= "2022-01-18")]

print(df)
print(df.columns)

with open('fixes/covid_live_jan_15_18.csv', 'w') as f:
    df.to_csv(f, index=False, header=True)

# cols needed: 'REPORT_DATE', 'CODE', 'ACTIVE_CNT', 'CASE_CNT', 'DEATH_CNT', 'TEST_CNT', 'MED_HOSP_CNT', 'MED_ICU_CNT', 'NAME', 'PREV_ACTIVE_CNT', 'PREV_CASE_CNT', 'PREV_DEATH_CNT', 'PREV_TEST_CNT', 'PREV_MED_HOSP_CNT', 'PREV_MED_ICU_CNT', 'NEW_CASE_CNT', 
# 'PREV_NEW_CASE_CNT', 'LAST_UPDATED_DATE'