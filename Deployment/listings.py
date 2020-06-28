import requests
import time
from datetime import datetime

class Listings():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def get_listings(self, radius=2000, result=10):
        coors = str(self.lat) + '%2C' + str(self.lon)
        time_now = int(time.time() * 1000)

        query = f"https://www.99.co/api/v2/web/search/listings?created_at={time_now}&"
        query += f"listing_type=sale&main_category=hdb&page_num=1&page_size={result}&property_segments=residential&"
        query += f"query_coords={coors}&query_limit=radius&query_type=google&"
        query += f"radius_max={radius}&rental_type=unit&sub_categories=hdb_2r%2Chdb_3r%2Chdb_4r%2Chdb_5r%2Chdb_executive"

        response = requests.get(query)
        try:
            payload = response.json()['data']['sections'][0]['listings']

            load_list = []
            for load in payload:
                load_dict = dict()
                postcode = int(load['postal_code'])
                load_dict['Postal Code'] = postcode
                load_dict['Address'] = load['address_name']
                load_dict['Price'] = load['attributes']['price_formatted']
                load_dict['Floor Area'] = load['attributes']['area_size_formatted'].split()[0]
                load_dict['Price per Sqft'] = load['attributes']['area_ppsf_formatted'].split()[0]
                if load['attributes']['completed_at']:
                    load_dict['Remaining Lease'] = 99 - datetime.fromtimestamp(time.time()).year + load['attributes']['completed_at']
                else:
                    load_dict['Remaining Lease'] = None
                api_route = f'https://developers.onemap.sg/commonapi/elastic/omsearch?searchVal={postcode}&returnGeom=Y&getAddrDetails=N'
                coor_response = requests.get(api_route).json()['results']
                if coor_response:
                    coors = coor_response[0]
                    load_dict['Latitude'] = float(coors['LATITUDE'])
                    load_dict['Longitude'] = float(coors['LONGITUDE'])
                    load_list.append(load_dict)
            return load_list

        except IndexError:
            return None
