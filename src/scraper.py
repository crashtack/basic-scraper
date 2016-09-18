
'''
ZOKA = http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx\
?Output=W&Business_Name=zoka&Business_Address=&Longitude=&Latitude=&City=seattle\
&Zip_Code=98103&Inspection_Type=All&Inspection_Start=&Inspection_End=\
&Inspection_Closed_Business=A&Violation_Points=&Violation_Red_Points=\
&Violation_Descr=&Fuzzy_Search=N&Sort=B

http://info.kingcounty.gov/health/ehs/foodsafety/inspections/Results.aspx?Buisness_Name=ZOKA&Output=W&Violation_Red_Points=&Longitude=&Inspection_Closed_Business=A&Sort=B&Inspection_Type=All&Zip_Code=98103&Latitude=&Business_Address=&Violation_Descr=&Violation_Points=&Fuzzy_Search=N&Inspection_End=&City=Seattle&Inspection_Start=

'''
import requests
import os
from io import open
from bs4 import BeautifulSoup
import sys
import re


INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': 'seattle',
    'Zip_Code': '98103',
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
    # import pdb; pdb.set_trace()
    return resp.content, resp.encoding


def load_inspection_page(filename):
    '''read a utf-8 html file from disk'''
    DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(DIR, filename)
    # with open(path, 'rb') as fh:
    #     data = fh.read
    file_ = open(path, 'rb')
    data = file_.read()
    encoding = 'utf-8'
    return data, encoding


def parse_source(html, encoding='utf-8'):
    '''parse the loaded file'''
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return parsed


def extract_data_listings(parsed):
    '''does something'''
    return parsed.find_all(id=re.compile(r"PR[\d]+~"))


def has_two_tds(elem):
    ''' returns true if the element is a tr and has exactly 2 tds'''
    is_tr = elem.name == 'tr'
    td_children = elem.find_all('td', recursive=False)
    has_two = len(td_children) == 2
    return is_tr and has_two


def clean_data(td):
    '''clean out the extra white space'''
    data = td.string
    try:
        return data.strip('"\\r\\n" \n\r:-')
    except AttributeError:
        return u''


def extract_restaurant_metadata(elem):
    metadata_rows = elem.find('tbody').find_all(
        has_two_tds, recursive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, []).append(clean_data(val_cell))
    return rdata

if __name__ == "__main__":
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '8/1/2016',
        'Zip_Code': '98103'
    }
    # import pdb; pdb.set_trace()
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, endocing = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)

    for listing in listings[:5]:
        metadata = extract_restaurant_metadata(listing)
        print(metadata)
        print()
