import requests

#AccessingAPI

def get_hist_info(zipcode:int, date:str, distance:int) -> dict:
    req_url = '''http://www.airnowapi.org/aq/observation/zipCode/historical/?format=application/json&zipCode=%s&date=%sT00-0000&distance=%s&API_KEY=NOTYOURAPIKEY'''
    return requests.get(req_url % (str(zipcode), str(date), str(distance)))
get_hist_info(98105, '2020-03-01', 10)

#Looping through API Requests
countme = 0
test_df = pd.DataFrame()
for zipc in zip_codes1:
    for date in dates_str:
        print(zipc, date, countme)
        x = get_hist_info(zipc, date)
        df = pd.DataFrame(x)
        test_df = pd.concat([test_df, df])
        countme += 1
        if countme >= 480:
            print('sleeping')
            print(datetime.datetime.now())
            time.sleep(3600)
            countme = 0
            
    test_df.to_csv('data/2020aqi2.tsv', sep='\t')


#Trimming Dataframes to relevant months

for year in range(1980, 2020):
    aqi_single_year = pd.read_csv(f'data/daily_aqi_metro/daily_aqi_by_cbsa_{year}.csv')
    aqi_single_year['Date'] = pd.to_datetime(aqi_single_year['Date'], format='%Y-%m-%d', errors='ignore')
    start_date = f'{year}-03-01'
    end_date = f'{year}-06-30'
    mask = (aqi_single_year['Date'] >= start_date) & (aqi_single_year['Date'] <= end_date)
    aqi_single_year = aqi_single_year.loc[mask]
    aqi_single_year.to_csv(f'data/daily_aqi_metro/daily_aqi_by_cbsa_{year}_cleaned.csv')


#Simple Datetime conversion function
def convert_datetime(df):
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='ignore')
    return df

#Concating Dataframes together

aggregate_cbsa_aqi_df = pd.DataFrame()
for year in range(1980, 2020):
    aqi_single_year = pd.read_csv(f'data/daily_aqi_metro/daily_aqi_by_cbsa_{year}_cleaned.csv', index_col=0)
    aggregate_cbsa_aqi_df = pd.concat([aggregate_cbsa_aqi_df, aqi_single_year])

# Making year month day columns

aggregate_cbsa_aqi_df['Year'] = aggregate_cbsa_aqi_df['Date'].apply(lambda x: x.year)
aggregate_cbsa_aqi_df['Month'] = aggregate_cbsa_aqi_df['Date'].apply(lambda x: x.month)
aggregate_cbsa_aqi_df['Day'] = aggregate_cbsa_aqi_df['Date'].apply(lambda x: x.day)

