
'''
ZOKA = http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx\
?Output=W&Business_Name=zoka&Business_Address=&Longitude=&Latitude=&City=seattle\
&Zip_Code=98103&Inspection_Type=All&Inspection_Start=&Inspection_End=\
&Inspection_Closed_Business=A&Violation_Points=&Violation_Red_Points=\
&Violation_Descr=&Fuzzy_Search=N&Sort=B

http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Buisness_Name=ZOKA&Output=W&Violation_Red_Points=&Longitude=&Inspection_Closed_Business=A&Sort=B&Inspection_Type=All&Zip_Code=98103&Latitude=&Business_Address=&Violation_Descr=&Violation_Points=&Fuzzy_Search=N&Inspection_End=&City=Seattle&Inspection_Start=

'''
import requests

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'B'
}


def get_inspection_page(**kwargs):
    url = INSPECTION_DOMAIN + INSPECTION_PATH + '?'
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        print('key: {}'.format(key))
        if key in INSPECTION_PARAMS:
            params[key] = val

    url += 'Output' + '=' + params['Output'] + '&'
    url += 'Business_Name' + '=' + params['Business_Name'] + '&'
    url += 'Business_Address' + '=' + params['Business_Address'] + '&'
    url += 'Longitude' + '=' + params['Longitude'] + '&'
    url += 'Latitude' + '=' + params['Latitude'] + '&'
    url += 'City' + '=' + params['City'] + '&'
    url += 'Zip_Code' + '=' + params['Zip_Code'] + '&'
    url += 'Inspection_Type' + '=' + params['Inspection_Type'] + '&'
    url += 'Inspection_Start' + '=' + params['Inspection_Start'] + '&'
    url += 'Inspection_End' + '=' + params['Inspection_End'] + '&'
    url += 'Inspection_Closed_Business' + '=' + params['Inspection_Closed_Business'] + '&'
    url += 'Violation_Points' + '=' + params['Violation_Points'] + '&'
    url += 'Violation_Red_Points' + '=' + params['Violation_Red_Points'] + '&'
    url += 'Violation_Descr' + '=' + params['Violation_Descr'] + '&'
    url += 'Fuzzy_Search' + '=' + params['Fuzzy_Search'] + '&'
    url += 'Sort' + '=' + params['Sort'] + '&'
    url = url[:-1]
    print('url: {}'.format(url))

    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content, resp.encoding
