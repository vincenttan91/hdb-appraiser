from flask import Flask, jsonify, request, render_template, url_for
from geoinfo import Geoinfo
from listings import Listings
import predict
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/getDetail', methods=['GET'])
def get_detail():
    address = request.args.get('address')
    api_route = f'https://developers.onemap.sg/commonapi/elastic/omsearch?searchVal={address}&returnGeom=Y&getAddrDetails=Y'
    response = requests.get(api_route).json()
    if response['results']:
        response = response['results'][0]
        latitude = float(response['LATITUDE'])
        longitude = float(response['LONGITUDE'])
        location = Geoinfo(latitude, longitude)
        payload = dict()
        payload['response'] = 'success'
        payload['attr'] = location.all_attr
        payload['attr']['latitude'] = latitude
        payload['attr']['longitude'] = longitude
        payload['attr']['storey_range'] = int(request.args.get('level'))
        payload['attr']['floor_area_sqm'] = int(request.args.get('area'))
        payload['attr']['remaining_lease'] = int(request.args.get('lease'))
        payload['price'] = predict.predict(payload['attr'])
        return payload
    else:
        return jsonify({'response': 'request failed',
                        'message': 'invalid address'})

@app.route('/getListings', methods=['GET'])
def get_listings():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    listing = Listings(latitude, longitude)
    payload = dict()
    payload['nearby'] = listing.get_listings()
    if payload['nearby']:
        payload['response'] = 'success'
    else:
        payload['response'] = 'invalid address'
    return payload

if __name__ == "__main__":
    app.run(debug=True)
