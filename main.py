import pandas as pd

covid_df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
#covid_df = pd.read_csv('us-counties.txt')
covid_df_live = pd.read_csv('https://github.com/nytimes/covid-19-data/raw/master/live/us-counties.csv')
covid_df = pd.concat([covid_df, covid_df_live])
pop_df = pd.read_excel('https://www.ers.usda.gov/webdocs/DataFiles/82701/RuralAtlasData23.xlsx', sheet_name='People', engine='openpyxl')
#pop_df = pd.read_excel('RuralAtlasData23.xlsx')

joined = covid_df.merge(pop_df, how='left', left_on='fips', right_on='FIPS')
joined = joined.sort_values(['fips', 'date'], ascending=[True, True]).reset_index(drop=True)
joined['cases_sum'] = joined['cases']
joined['cases'] -= joined.groupby('fips').shift().reset_index()['cases']# - joined['cases']
joined['cases_7day'] = joined.groupby('fips').rolling(7, min_periods=1)['cases'].sum().reset_index()['cases']
joined['cases_14day'] = joined.groupby('fips').rolling(14, min_periods=1)['cases'].sum().reset_index()['cases']
joined['active_case_estimate'] = joined['cases_14day'] / joined['TotalPopEst2018']

lac = joined.loc[joined['county'] == 'Los Angeles']
lac_current = lac.iloc[-1]
print(f"Recent Active Case percentage in LA County: {lac.iloc[-1]['active_case_estimate']:.4%}")
print(lac.iloc[-3:][['date', 'active_case_estimate']])

joined.to_csv('county_combined.csv')
