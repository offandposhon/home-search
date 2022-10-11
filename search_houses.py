import requests
import json
import get_commute_mapbox
import time
import os
from dotenv import load_dotenv


## Set your basic search variables
# enter your search-area city, state here. 
# Ex: 'alexandria, va', 'rockville, md'
location_input = 'rockville, md'
property_type_input='SINGLE_FAMILY' # Also accepts 'TOWNHOUSE' and other types
home_type_input='Houses' # if property_type_input set to 'TOWNHOUSE', set this to 'Townhomes'
desired_walk_score= 53 #(1-100)
max_commute_time = 45 # (minutes)
price_min = '400000' # ($)
price_max = '760000' # ($)
beds_min = '3'
baths_min = '3'
contract_type = 'ForSale' # 'ForSale', 'ForRent'
minimum_square_feet = '1800'
minimum_school_rating = 5 #(1-10)
commute_end_address='740 15th St NW, Washington, D.C.' # Ex: 740 15 St NW, Washington, D.C.'


url = "https://zillow-com1.p.rapidapi.com/propertyExtendedSearch"
querystring = {"location":location_input,"status_type": contract_type,"home_type": home_type_input,"minPrice": price_min,"maxPrice": price_max,"bathsMin": baths_min,"bedsMin": beds_min,"sqftMin": minimum_square_feet}
load_dotenv()

RAPID_API_KEY = os.getenv('RAPID_API_KEY')

headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
}

all_house_ids = []
# find out how many pages of info there are
response = requests.request("GET", url, headers=headers, params=querystring)
output = json.loads(response.text)
total_pages = output['totalPages']
print(f"Pages of Zillow results to process: {total_pages}")
print('Processing..')
total_outputs = []
page_count = 1
while page_count <= total_pages:
    # sleep to avoid API timeouts from RapidAPI
    time.sleep(2)
    querystring = {"location":location_input,"status_type": contract_type,"home_type": home_type_input,"minPrice": price_min,"maxPrice": price_max,"bathsMin": baths_min,"bedsMin": beds_min,"sqftMin": minimum_square_feet}
    response = requests.request("GET", url, headers=headers, params=querystring)
    output = json.loads(response.text)
    for item in output['props']:
        total_outputs.append(item)
    page_count = page_count + 1


for item in total_outputs:
    if item['propertyType'] == property_type_input:
        all_house_ids.append(item['zpid'])


url = "https://zillow-com1.p.rapidapi.com/property"
headers = {
	"X-RapidAPI-Key": RAPID_API_KEY,
	"X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
}

qualified_listings = []
for id in all_house_ids:
    querystring = {"zpid":id}
    time.sleep(2)
    response = requests.request("GET", url, headers=headers, params=querystring)
    specific_search_result = json.loads(response.text)
    primary_school_rating = ''
    try:
        for school in specific_search_result['schools']:
            print()
    except Exception as e:
        print('SCHOOLS ERROR')
        print(specific_search_result)
        continue
    
    address_to_pass = specific_search_result['address']['streetAddress'] + ", " + specific_search_result['address']['city'] + ", " + specific_search_result['address']['state']
    print(address_to_pass)
    print('School ratings:')
    for school in specific_search_result['schools']:
        print(school['level'])
        print(school['rating'])
        if school['level'] == 'Primary' or school['level'] == 'Elementary':
            primary_school_rating = school['rating']
            if primary_school_rating:
                if primary_school_rating >= minimum_school_rating:
                    address_to_pass = specific_search_result['address']['streetAddress'] + ", " + specific_search_result['address']['city'] + ", " + specific_search_result['address']['state']
                    # commute_time = get_commute_time.get_commute_time(address_to_pass, commute_end_address)
                    commute_time = get_commute_mapbox.get_commute_time(address_to_pass, commute_end_address)
                    commute_time_min = commute_time / 60


                    if commute_time_min < max_commute_time:
                        walk_url = "https://zillow-com1.p.rapidapi.com/walkAndTransitScore"
                        querystring = {"zpid":id}
                        headers = {
                            "X-RapidAPI-Key": RAPID_API_KEY,
                            "X-RapidAPI-Host": "zillow-com1.p.rapidapi.com"
                        }

                        response = requests.request("GET", walk_url, headers=headers, params=querystring)
                        response_transit = json.loads(response.text)
                        walk_score = response_transit['walkScore']['walkscore']

                        if walk_score >= desired_walk_score:
                            print(f"COMMUTE TIME: {commute_time_min}")
                            print(f"WALK SCORE: {walk_score}")
                            # print(json.dumps(specific_search_result, indent=4))
                            qualified_listings.append("https://zillow.com" + specific_search_result['url'])


                
    if len(qualified_listings) > 0:
        print('Qualified listings found so far:')
        print(qualified_listings)
    else:
        print('No qualified listings found so far.. ')


if len(qualified_listings) > 0:
    print('Final Qualified listings:')
    print(qualified_listings)
else:
    print('No qualified listings found that meet your specified criteria')