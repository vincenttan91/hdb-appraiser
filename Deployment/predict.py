import joblib
import pandas as pd

def predict(payload):
    model = joblib.load(open('./data/lasso.pkl', 'rb'))
    scaler = joblib.load(open('./data/scaler.pkl', 'rb'))
    cols = ['storey_range', 'floor_area_sqm', 'remaining_lease', 'sold_year',
            'sold_month', 'mrt_dist', 'near_bus_itc', 'near_mrt_itc', 'bus_u300m',
            'bus_dist', 'mall_u1km', 'mall_dist', 'pri_u1km', 'pri_u2km',
            'pri_aff_u1km', 'pri_aff_u2km', 'pri_elite_u1km', 'pri_elite_u2km',
            'sec_u1km', 'sec_u2km', 'sec_aff_u1km', 'sec_aff_u2km', 'town_BEDOK',
            'town_BISHAN', 'town_BUKIT BATOK', 'town_BUKIT MERAH',
            'town_BUKIT PANJANG', 'town_BUKIT TIMAH', 'town_CENTRAL AREA',
            'town_CHOA CHU KANG', 'town_CLEMENTI', 'town_GEYLANG', 'town_HOUGANG',
            'town_JURONG EAST', 'town_JURONG WEST', 'town_KALLANG/WHAMPOA',
            'town_MARINE PARADE', 'town_PASIR RIS', 'town_PUNGGOL',
            'town_QUEENSTOWN', 'town_SEMBAWANG', 'town_SENGKANG', 'town_SERANGOON',
            'town_TAMPINES', 'town_TOA PAYOH', 'town_WOODLANDS', 'town_YISHUN']

    # model = joblib.load(open('./data/final_model.pkl', 'rb'))
    # cols = ['storey_range', 'floor_area_sqm', 'remaining_lease', 'sold_year', 'mrt_dist', 'mall_dist', 'pri_u2km', 'pri_aff_u1km', 'sec_u2km',
    #         'sec_aff_u1km', 'town_ANG MO KIO', 'town_BEDOK', 'town_BISHAN', 'town_BUKIT BATOK', 'town_BUKIT MERAH', 'town_BUKIT PANJANG',
    #         'town_BUKIT TIMAH', 'town_CENTRAL AREA', 'town_CHOA CHU KANG', 'town_CLEMENTI', 'town_GEYLANG', 'town_HOUGANG', 'town_JURONG EAST',
    #         'town_JURONG WEST', 'town_KALLANG/WHAMPOA', 'town_MARINE PARADE', 'town_PASIR RIS', 'town_PUNGGOL', 'town_QUEENSTOWN', 'town_SEMBAWANG',
    #         'town_SENGKANG', 'town_SERANGOON', 'town_TAMPINES', 'town_TOA PAYOH', 'town_WOODLANDS', 'town_YISHUN']

    df = pd.DataFrame([payload])
    df.drop(['mrt_station'], axis=1, inplace=True)
    df = pd.get_dummies(df)
    for col in cols:
        if col not in df.columns:
            df[col] = 0
    feature = df[cols]
    feature = scaler.transform(feature)
    price = int(model.predict(feature)[0] // 1000 * 1000)
    return f'{price:,}'
