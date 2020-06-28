from datetime import datetime
import time
import pandas as pd
import authenticate as auth
import travel_time as tt
from math import sin, cos, sqrt, atan2, radians
from shapely.geometry import Point
from shapely import wkt
import geopandas as gpd

class Geoinfo():
    def __init__(self, lat, lon):
        self.lat_1 = lat
        self.lon_1 = lon
        self.loc_dict = dict()
        self.mrt()
        self.bus()
        self.malls()
        self.primary_sc()
        self.secondary_sc()
        self.get_date()
        self.loc_dict['town'] = self.planning_area()

    def dist_cal(self, coor):
        R = 6373.0
        lat_2 = radians(coor[0])
        lon_2 = radians(coor[1])
        dlon = lon_2 - radians(self.lon_1)
        dlat = lat_2 - radians(self.lat_1)
        a = sin(dlat / 2)**2 + cos(self.lat_1) * cos(lat_2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = int(R * c * 1000)
        return distance

    def mrt(self):
        mrt = pd.read_csv('./data/MRT.csv')
        dist_list = []
        for coor in zip(mrt['Latitude'], mrt['Longitude']):
            distance = self.dist_cal(coor)
            dist_list.append(distance)
        self.loc_dict['mrt_dist'] = min(dist_list)

        if (mrt.loc[dist_list.index(self.loc_dict['mrt_dist']), 'Bus_Interchange'] == 1) & (min(dist_list) <= 500):
            self.loc_dict['near_bus_itc'] = 1
        else:
            self.loc_dict['near_bus_itc'] = 0

        if (mrt.loc[dist_list.index(self.loc_dict['mrt_dist']), 'MRT_Interchange'] == 1) & (min(dist_list) <= 500):
            self.loc_dict['near_mrt_itc'] = 1
        else:
            self.loc_dict['near_mrt_itc'] = 0

        self.loc_dict['mrt_station'] = mrt.loc[dist_list.index(self.loc_dict['mrt_dist']), 'Name']

    def bus(self):
        bus = pd.read_csv('./data/Bus_Stop.csv')
        dist_list = []
        bus_list = 0
        for coor in zip(bus['latitude'], bus['longitude']):
            distance = self.dist_cal(coor)
            dist_list.append(distance)
            if distance <= 300:
                bus_list += 1
        self.loc_dict['bus_u300m'] = bus_list
        self.loc_dict['bus_dist'] = min(dist_list)

    def malls(self):
        spm = pd.read_csv('./data/Mall.csv')
        dist_list = []
        total_list = []
        for coor in zip(spm['latitude'], spm['longitude']):
            distance = self.dist_cal(coor)
            total_list.append(distance)
            if distance <= 1000:
                dist_list.append(distance)
        self.loc_dict['mall_u1km'] = len(dist_list)
        self.loc_dict['mall_dist'] = min(total_list)

    def primary_sc(self):
        pri = pd.read_csv('./data/Primary_School.csv')
        pri.loc[0:19, 'elite'] = 1
        under_1km = 0
        under_2km = 0
        aff_1km = 0
        aff_2km = 0
        elite_1km = 0
        elite_2km = 0

        for idx, coor in enumerate(zip(pri['latitude'], pri['longitude'])):
            distance = self.dist_cal(coor)
            if distance <= 1000:
                under_1km += 1
                if (pri.loc[idx, 'affiliation'] == 1) & (pri.loc[idx, 'elite'] == 1):
                    aff_1km += 1
                if pri.loc[idx, 'elite'] == 1:
                    elite_1km += 1

            if distance <= 2000:
                under_2km += 1
                if (pri.loc[idx, 'affiliation'] == 1) & (pri.loc[idx, 'elite'] == 1):
                    aff_2km += 1
                if pri.loc[idx, 'elite'] == 1:
                    elite_2km += 1

        self.loc_dict['pri_u1km'] = under_1km
        self.loc_dict['pri_u2km'] = under_2km
        self.loc_dict['pri_aff_u1km'] = aff_1km
        self.loc_dict['pri_aff_u2km'] = aff_2km
        self.loc_dict['pri_elite_u1km'] = elite_1km
        self.loc_dict['pri_elite_u2km'] = elite_2km

    def secondary_sc(self):
        sec = pd.read_csv('./data/Secondary_School.csv')
        sec.loc[0:19, 'elite'] = 1
        under_1km = 0
        under_2km = 0
        aff_1km = 0
        aff_2km = 0
        elite_1km = 0
        elite_2km = 0

        for idx, coor in enumerate(zip(sec['latitude'], sec['longitude'])):
            distance = self.dist_cal(coor)
            if distance <= 1000:
                under_1km += 1
                if (sec.loc[idx, 'affiliation'] == 1) & (sec.loc[idx, 'elite'] == 1):
                    aff_1km += 1
                if sec.loc[idx, 'elite'] == 1:
                    elite_1km += 1

            if distance <= 2000:
                under_2km += 1
                if (sec.loc[idx, 'affiliation'] == 1) & (sec.loc[idx, 'elite'] == 1):
                    aff_2km += 1
                if sec.loc[idx, 'elite'] == 1:
                    elite_2km += 1

        self.loc_dict['sec_u1km'] = under_1km
        self.loc_dict['sec_u2km'] = under_2km
        self.loc_dict['sec_aff_u1km'] = aff_1km
        self.loc_dict['sec_aff_u2km'] = aff_2km
        self.loc_dict['sec_elite_u1km'] = elite_1km
        self.loc_dict['sec_elite_u2km'] = elite_2km

    def planning_area(self):
        planning_area = pd.read_csv('./data/planning_area.csv')
        planning_area['geometry'] = planning_area['geometry'].apply(wkt.loads)
        planning_area = gpd.GeoDataFrame(planning_area, geometry='geometry')
        for boundary, town in zip(planning_area.geometry, planning_area.name):
            coor = Point(self.lon_1, self.lat_1)
            if coor.within(boundary):
                return town
        return 'unknown'

    # def travel_time(self):
    #     token = auth.get_token('hdb.appraiser@gmail.com', 'singaporepwd')
    #     destination = [{'name': 'raffles_place', 'coor': [1.282542, 103.850954]},
    #                    {'name': 'one_north', 'coor': [1.299036, 103.786897]},
    #                    {'name': 'jurong_east', 'coor': [1.333577, 103.742292]},
    #                    {'name': 'orchard', 'coor': [1.304898, 103.832525]},
    #                    {'name': 'changi', 'coor': [1.35722, 103.987305]}]

    #     for place in destination:
    #         col_name = 'pt_time_' + place['name']
    #         lat_2 = place['coor'][0]
    #         lon_2 = place['coor'][1]
    #         self.loc_dict[col_name] = tt.get_duration(self.lat_1, self.lon_1, lat_2, lon_2, token)

        # for place in destination:
        #     for mode in ['pt', 'drive']:
        #         col_name = mode + '_' + place['name']
        #         lat_2 = place['coor'][0]
        #         lon_2 = place['coor'][1]
        #         self.loc_dict[col_name] = tt.get_duration(self.lat_1, self.lon_1, lat_2, lon_2, token, route_type=mode)

    def get_date(self):
        dt = datetime.fromtimestamp(time.time())
        self.loc_dict['sold_year'] = dt.year - 2016
        self.loc_dict['sold_month'] = dt.month

    @property
    def all_attr(self):
        return self.loc_dict
