def get_hist_info(zipcode:int, date:str, distance:int) -> dict:
    req_url = '''http://www.airnowapi.org/aq/observation/zipCode/historical/?format=application/json&zipCode=%s&date=%sT00-0000&distance=%s&API_KEY=9AF5ED39-FAA2-4BBD-AD3D-E90F7178E17F'''
    return requests.get(req_url % (str(zipcode), str(date), str(distance)))
get_hist_info(98105, '2020-03-01', 10)
