#%%

import pandas as pd 
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
import datetime 
import pytz
import time

print("Scraping Health Dept")

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
today = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
today = today.strftime('%Y-%m-%d')

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Firefox(options=chrome_options)


start_url = 'https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert/coronavirus-covid-19-case-numbers-and-statistics'


#%%
driver.get(start_url)
driver.implicitly_wait(15)
time.sleep(15)

#%%

tables = pd.read_html(driver.page_source.encode("utf-8"))

i = 0

## Need to wait while all the tables load
while len(tables) < 9:
    # driver.implicitly_wait(10)
    # print(f"Len {len(tables)}")
    time.sleep(2)
    tables = pd.read_html(driver.page_source.encode("utf-8"))
    i += 1

    if i > 600:
        print("Break")
        break

names = {0:"recent_cases", 1:"total_cases", 2:"cases_age_sex",
 3:"deaths_age_sex", 4:"tests", 5:"hospitalisations", 6:"ndis",
  7:"aged_care_resi", 8:"aged_care_home", 9:"oecd_mortality"}

dicto = {"recent_cases": ['Jurisdiction', 'Active cases', 'Locally acquired last 24 hours',
                            'Overseas acquired last 24 hours',
                            "Under investigation last 24 hours", 'Locally acquired last 7 days',
                            'Overseas acquired last 7 days', 'Under investigation last 7 days','Date'],
       "total_cases":   ['Jurisdiction', 'Overseas',
                        'Locally acquired - contact of confirmed case',
                        'Locally acquired - unknown contact',
                        'Locally acquired - interstate travel', 'Under investigation',
                        'Total cases', 'Total deaths', 'Date'],
        "cases_age_sex":    ['Age Group', 'Male', 'Female', 'Date'],
        "deaths_age_sex":   ['Age Group', 'Male', 'Female', 'Date'],
        "tests":    ['Jurisdiction', 'Tests in last 7 days',
                        'Tests in last 7 days per 100,000 population', 'Total tests',
                        'Total positive tests (%)', 'Date'],
        "hospitalisations": ['Jurisdiction', 'Not in ICU', 'ICU', 'Date'],
        "ndis"  :['State', 'Participant Active', 'Worker Active', 'Participant Recovered',
       'Worker Recovered', 'Participant Deaths', 'Worker Deaths', 'Date'],
"aged_care_resi" :['Jurisdiction', 'Active', 'Recovered', 'Deaths', 'Date'],
'aged_care_home': ['Jurisdiction', 'Active', 'Recovered', 'Deaths', 'Date']}

if len(tables) >= 9:
    try:


        i = 0
        for table in tables:
            # print(i)
            # print(table)
            # print(table.columns)
            table['Date'] = today
            title = f"{today}_{names[i]}"

            nammo = names[i]

            ## Dump individual file

            print(f"Dumping individual: {title}")

            with open(f"data/{title}.csv", "w") as f:
                table.to_csv(f, index=False, header=True)


            ## Ensure column names 
            cols = dicto[nammo]

            if (nammo == "recent_cases") | (nammo == "total_cases"):
                # if (name == testo):
                    # print(nammo, cols)
                    inter_cols = table.columns.tolist()
                    inter_cols = [x.replace("*", "").strip() if "*" in x else x for x in inter_cols]
                    inter_cols = [x.replace("^", "").strip() if "^" in x else x for x in inter_cols]
                    inter_cols = [x.replace("'", "").strip() if "'" in x else x for x in inter_cols]
                    inter_cols = [x.replace("'", "").strip() if "'" in x else x for x in inter_cols]
                    table.columns = inter_cols
                    # print(nammo, inter_cols)
                    # table.rename(columns={"'Under investigation last 24 hours'":'Under investigation last 24 hours'}, inplace=True)

            table[cols] = table[cols]

            ## Add data to the output files

            old = pd.read_csv(f'output/{names[i]}.csv')
            # print(names[i])
            # print(old.shape)
            combo = old.append(table)
            # print(combo.shape)
            combo = combo.drop_duplicates(keep='last')
            # print("Dropped", combo.shape)

            dropper = ['recent_cases', 'total_cases', 'tests', 'hospitalisations', 'aged_care_resi', 'aged_care_home']

            if names[i] in dropper:
                print(names[i])
                print(len(combo))
                combo = combo.drop_duplicates(subset=['Jurisdiction', 'Date'], keep='last')
                print(len(combo))

            print("Dumping output")



            with open(f'output/{names[i]}.csv', 'w') as f:
                combo.to_csv(f, index=False, header=True)


            i += 1

    except Exception as e:
        print(f"Error: {title}: {e}")
        # print(table.columns)
        

driver.close()