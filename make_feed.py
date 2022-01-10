import pandas as pd 
from modules.syncData import syncData

# test = pd.read_json('https://covidlive.com.au/covid-live.json')
# print(test.columns.tolist())

# 'REPORT_DATE', 'LAST_UPDATED_DATE', 'CODE', 'NAME', 'CASE_CNT',
# 'TEST_CNT', 'DEATH_CNT', 'RECOV_CNT', 'MED_ICU_CNT', 'MED_VENT_CNT',
# 'MED_HOSP_CNT', 'SRC_OVERSEAS_CNT', 'SRC_INTERSTATE_CNT', 'SRC_CONTACT_CNT',
# 'SRC_UNKNOWN_CNT', 'SRC_INVES_CNT', 'PREV_CASE_CNT', 'PREV_TEST_CNT',
# 'PREV_DEATH_CNT', 'PREV_RECOV_CNT', 'PREV_MED_ICU_CNT', 'PREV_MED_VENT_CNT', 
# 'PREV_MED_HOSP_CNT', 'PREV_SRC_OVERSEAS_CNT', 'PREV_SRC_INTERSTATE_CNT', 
# 'PREV_SRC_CONTACT_CNT', 'PREV_SRC_UNKNOWN_CNT', 'PREV_SRC_INVES_CNT', 'PROB_CASE_CNT',
# 'PREV_PROB_CASE_CNT', 'ACTIVE_CNT', 'PREV_ACTIVE_CNT', 'NEW_CASE_CNT',
# 'PREV_NEW_CASE_CNT', 'VACC_DIST_CNT', 'PREV_VACC_DIST_CNT', 'VACC_DOSE_CNT',
# 'PREV_VACC_DOSE_CNT', 'VACC_PEOPLE_CNT', 'PREV_VACC_PEOPLE_CNT', 'VACC_AGED_CARE_CNT',
# 'PREV_VACC_AGED_CARE_CNT', 'VACC_GP_CNT', 'PREV_VACC_GP_CNT', 'VACC_FIRST_DOSE_CNT',
# 'PREV_VACC_FIRST_DOSE_CNT', 'VACC_FIRST_DOSE_CNT_12_15', 'PREV_VACC_FIRST_DOSE_CNT_12_15',
# 'VACC_PEOPLE_CNT_12_15', 'PREV_VACC_PEOPLE_CNT_12_15', 'VACC_BOOSTER_CNT', 'PREV_VACC_BOOSTER_CNT'

codes = {"AUS":"Australia", "NSW":"NSW", "QLD":"Queensland", 
"VIC": "Victoria", "TAS": "Tasmania", "ACT": "ACT", "SA": "South Australia", "WA": "WA", "NT":"NT"}

## Read in recent cases to get actives
recent = pd.read_csv('output/recent_cases.csv')
# 'Jurisdiction', 'Active cases',
# 'Locally acquired last 24 hours', 'Overseas acquired last 24 hours', 
# 'Under investigation last 24 hours', 'Locally acquired last 7 days', 
# 'Overseas acquired last 7 days', 'Under investigation last 7 days', 'Date'

recent = recent[['Date','Jurisdiction', 'Active cases']]


### Read in total cases to get cumulatives

total = pd.read_csv('output/total_cases.csv')

# 'Jurisdiction', 'Overseas', 'Locally acquired - contact of confirmed case', 
# 'Locally acquired - unknown contact', 'Locally acquired - interstate travel', 
# 'Under investigation', 'Total cases', 'Total deaths', 'Date'

total = total[['Date', 'Jurisdiction', 'Total cases', 'Total deaths']]

### Read in total tests

tests = pd.read_csv('output/tests.csv')
# 'Jurisdiction', 'Tests in last 7 days', 'Tests in last 7 days per 100,000 population', 
# 'Total tests', 'Total positive tests (%)', 'Date'

tests = tests[['Date', 'Jurisdiction', 'Total tests']]


### Read in hospo

hospo = pd.read_csv('output/hospitalisations.csv')
# 'Jurisdiction', 'Not in ICU', 'ICU', 'Date'
hospo['In hospital'] = hospo['Not in ICU'] + hospo['ICU']


hospo = hospo[['Date', 'Jurisdiction', 'In hospital', 'ICU']]

### Start Combining


combo = pd.merge(recent, total, on=['Date', 'Jurisdiction'], how='left')
combo = pd.merge(combo, tests, on=['Date', 'Jurisdiction'], how='left')
combo = pd.merge(combo, hospo, on=['Date', 'Jurisdiction'], how='left')

combo = combo[['Date', 'Jurisdiction', 'Active cases', 'Total cases', 'Total deaths', 'Total tests', 'In hospital', 'ICU']]

combo.columns = ['REPORT_DATE', 'CODE', 'ACTIVE_CNT', 'CASE_CNT', 'DEATH_CNT', 'TEST_CNT', 'MED_HOSP_CNT', 'MED_ICU_CNT']

combo.loc[combo['CODE'] == "Australia", 'CODE'] = 'AUS'
combo['NAME'] = combo.apply(lambda row: codes[row.CODE], axis = 1)

oz = combo.loc[combo['CODE'] == "AUS"].copy()
latest_cases = oz.iloc[-1]['CASE_CNT']
second_latest_cases = oz.iloc[-2]['CASE_CNT']

# second_latest_cases = inter2.iloc[-2]['Total cases']
# if latest_cases == second_latest_cases:
#     inter2 = inter2.iloc[:-1].copy()

listo = []

for juri in combo['CODE'].unique().tolist():
    inter = combo.loc[combo['CODE'] == juri].copy()

    ### TEST TO MAKE SURE ITS NEW DATA


    if latest_cases == second_latest_cases:
        inter = inter.iloc[:-1]


    ## ADD PREV COLUMNS
    inter['PREV_ACTIVE_CNT'] = inter['ACTIVE_CNT'].shift(1)
    inter['PREV_CASE_CNT'] = inter['CASE_CNT'].shift(1)
    inter['PREV_DEATH_CNT'] = inter['DEATH_CNT'].shift(1)

    inter['PREV_TEST_CNT'] = inter['TEST_CNT'].shift(1)
    inter['PREV_MED_HOSP_CNT'] = inter['MED_HOSP_CNT'].shift(1)
    inter['PREV_MED_ICU_CNT'] = inter['MED_ICU_CNT'].shift(1)
    
    inter['NEW_CASE_CNT'] = inter['CASE_CNT'].diff(1)
    inter['PREV_NEW_CASE_CNT'] = inter['NEW_CASE_CNT'].shift(1)


    listo.append(inter)

combo = pd.concat(listo)


combo['LAST_UPDATED_DATE'] = combo['REPORT_DATE']


testo = combo.loc[combo['CODE'] == "NSW"]

# testo = testo[['REPORT_DATE', 'CODE', 'CASE_CNT','PREV_CASE_CNT', 'NEW_CASE_CNT']]




### Read in prev Anthony data

ant = pd.read_csv('archive/Anthony_feed.csv')
ant = ant[['REPORT_DATE', 'LAST_UPDATED_DATE', 'NAME', 'CODE', 'ACTIVE_CNT', 'CASE_CNT', 'DEATH_CNT', 'TEST_CNT', 'MED_HOSP_CNT', 'MED_ICU_CNT', 'PREV_ACTIVE_CNT', 'PREV_CASE_CNT', 'PREV_DEATH_CNT', 'PREV_TEST_CNT', 'PREV_MED_HOSP_CNT', 'PREV_MED_ICU_CNT', 'NEW_CASE_CNT', 'PREV_NEW_CASE_CNT']]

ant = ant.loc[ant['REPORT_DATE'] < "2021-10-06"]

tog = combo.append(ant)

tog['REPORT_DATE'] = pd.to_datetime(tog['REPORT_DATE'])
tog['REPORT_DATE'] = tog['REPORT_DATE'].dt.strftime("%Y-%m-%d")

tog['LAST_UPDATED_DATE'] = pd.to_datetime(tog['LAST_UPDATED_DATE'])
tog['LAST_UPDATED_DATE'] = tog['LAST_UPDATED_DATE'].dt.strftime("%Y-%m-%d")

tog = tog.sort_values(by='REPORT_DATE', ascending=True)



p = testo


print(p)
# print(p.tail(20))
print(p.columns.tolist())

tog.fillna('', inplace=True)

# print(combo.to_dict('records'))

syncData(tog.to_dict(orient='records'),'2022/01/oz-covid-health-data', f"cases")