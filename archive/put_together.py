import pandas as pd 
import os 


names = ["recent_cases", "total_cases", "cases_age_sex",
 "deaths_age_sex", "tests", "hospitalisations", "ndis",
  "aged_care_resi", "aged_care_home"]

testo = names[0]
dicto = {"recent_cases": ['Jurisdiction', 'Active cases', 'Locally acquired last 24 hours',
                            'Overseas acquired last 24 hours',
                            "'Under investigation last 24 hours'", 'Locally acquired last 7 days',
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

for name in names:

    listo = []
    for file in os.listdir('data'):
        if name in file:

            cols = dicto[name]

            inter = pd.read_csv(f'data/{file}', parse_dates=['Date'])

            if (name == "recent_cases") | (name == "total_cases"):
            # if (name == testo):
                cols = inter.columns.tolist()
                cols = [x.replace("*", "").strip() if "*" in x else x for x in cols]
                cols = [x.replace("^", "").strip() if "^" in x else x for x in cols]
                cols = [x.replace("'", "").strip() if "'" in x else x for x in cols]
                cols = [x.replace("'", "").strip() if "'" in x else x for x in cols]

                # inter.rename(columns={"'Under investigation last 24 hours'":'Under investigation last 24 hours'}, inplace=True)

                inter.columns = cols
            
            inter[cols] = inter[cols]

            listo.append(inter)




    final = pd.concat(listo)
    final = final.sort_values(by='Date', ascending=True)

    if name == testo:


        print(name, final.columns)

    with open(f"output/{name}.csv", "w") as f:
        final.to_csv(f, index=False, header=True)

    print(final.shape)
    final.drop_duplicates(keep='last')
    print(final.shape)


