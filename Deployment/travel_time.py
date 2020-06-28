def get_duration(lat_1, lon_1, lat_2, lon_2, token, route_type='pt'):
    import requests
    import json

    if route_type == 'pt':
        query = f"https://developers.onemap.sg/privateapi/routingsvc/route?start={lat_1},{lon_1}&end={lat_2},{lon_2}&routeType={route_type}&token={token}&date=2019-10-04&time=07:30:00&mode=TRANSIT&maxWalkDistance=500&numItineraries=1"

    else:
        query = f"https://developers.onemap.sg/privateapi/routingsvc/route?start={lat_1},{lon_1}&end={lat_2},{lon_2}&routeType={route_type}&token={token}"

    response = requests.get(query)
    jsons = json.loads(response.content)

    if route_type == 'pt':
        duration = round(jsons['plan']['itineraries'][0]['duration'] / 60, 2)
    else:
        duration = round(jsons['route_summary']['total_time'] / 60, 2)

    return duration
