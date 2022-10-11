from tracemalloc import start
import requests
from datetime import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()
import urllib

def get_commute_time(starting_location, ending_location):
    MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY')
    
    # geocode your start and end points
    # starting
    enc_starting_location = urllib.parse.quote_plus(starting_location)
    starting_geocode_url="https://api.mapbox.com/geocoding/v5/mapbox.places/"+str(enc_starting_location)+".json?limit=1&proximity=ip&types=address&access_token="+MAPBOX_API_KEY
    try:
        res = requests.request("GET", url=starting_geocode_url)
        res = json.loads(res.text)
        starting_coordinate_1 = res['features'][0]['geometry']['coordinates'][0]
        starting_coordinate_2 = res['features'][0]['geometry']['coordinates'][1]
        start_cood=str(starting_coordinate_1)+','+str(starting_coordinate_2)
    except Exception as e:
        print("Error getting starting coordinates:")
        print(e)

    # ending location
    enc_ending_location = urllib.parse.quote_plus(ending_location)
    ending_geocode_url="https://api.mapbox.com/geocoding/v5/mapbox.places/"+enc_ending_location+".json?limit=1&proximity=ip&types=address&access_token="+MAPBOX_API_KEY
    try:
        res = requests.request("GET", url=ending_geocode_url)
        res = json.loads(res.text)
        ending_coordinate_1 = res['features'][0]['geometry']['coordinates'][0]
        ending_coordinate_2 = res['features'][0]['geometry']['coordinates'][1]
        end_cood=str(ending_coordinate_1)+','+str(ending_coordinate_2)
    except Exception as e:
        print("Error getting ending coordinates:")
        print(e)


    encoded_coords = urllib.parse.quote_plus( start_cood+";"+end_cood )
    url="https://api.mapbox.com/directions/v5/mapbox/driving/"+encoded_coords+"?alternatives=true&geometries=geojson&language=en&overview=simplified&steps=true&access_token="+MAPBOX_API_KEY
    try:                                        
        response = requests.request("GET", url)
        mapbox_search_result = json.loads(response.text)
        if mapbox_search_result['routes'][0]:
            commute_time_min = mapbox_search_result['routes'][0]['duration']
        else:
            raise Exception('No routes found')
    except Exception as e:
        print("Error calculating commute time!!!!!! :")
        print(e)
        commute_time_min = 999999999999
        return commute_time_min
        
    # print(commute_time_min)
    return commute_time_min