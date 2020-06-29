from datetime import datetime
import time
import pandas as pd
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

    def malls(self):
        spm = pd.read_csv('./data/Mall.csv')
        dist_list = []
        total_list = []
        for coor in zip(spm['latitude'], spm['longitude']):
            distance = self.dist_cal(coor)
            total_list.append(distance)
        self.loc_dict['mall_dist'] = min(total_list)

    def primary_sc(self):
        pri = pd.read_csv('./data/Primary_School.csv')
        pri.loc[0:19, 'elite'] = 1
        under_2km = 0
        aff_1km = 0

        for idx, coor in enumerate(zip(pri['latitude'], pri['longitude'])):
            distance = self.dist_cal(coor)
            if distance <= 1000:
                if (pri.loc[idx, 'affiliation'] == 1) & (pri.loc[idx, 'elite'] == 1):
                    aff_1km += 1

            if distance <= 2000:
                under_2km += 1

        self.loc_dict['pri_u2km'] = under_2km
        self.loc_dict['pri_aff_u1km'] = aff_1km

    def secondary_sc(self):
        sec = pd.read_csv('./data/Secondary_School.csv')
        sec.loc[0:19, 'elite'] = 1
        under_2km = 0
        aff_1km = 0

        for idx, coor in enumerate(zip(sec['latitude'], sec['longitude'])):
            distance = self.dist_cal(coor)
            if distance <= 1000:
                if (sec.loc[idx, 'affiliation'] == 1) & (sec.loc[idx, 'elite'] == 1):
                    aff_1km += 1

            if distance <= 2000:
                under_2km += 1

        self.loc_dict['sec_u2km'] = under_2km
        self.loc_dict['sec_aff_u1km'] = aff_1km

    def planning_area(self):
        planning_area = pd.read_csv('./data/planning_area.csv')
        planning_area['geometry'] = planning_area['geometry'].apply(wkt.loads)
        planning_area = gpd.GeoDataFrame(planning_area, geometry='geometry')
        for boundary, town in zip(planning_area.geometry, planning_area.name):
            coor = Point(self.lon_1, self.lat_1)
            if coor.within(boundary):
                return town
        return 'unknown'

    def get_date(self):
        dt = datetime.fromtimestamp(time.time())
        self.loc_dict['sold_year'] = dt.year - 2016

    @property
    def all_attr(self):
        return self.loc_dict
