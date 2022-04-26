import netCDF4 as nc
import datetime as dt
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

TRACK_TYPE = np.ndarray(shape=(5,), dtype=float)
SAT_TYPE = nc.Dataset


def utc_to_sec(utc: str) -> float:
    return (dt.datetime(int(utc[6:10]), int(utc[3:5]), int(utc[:2]), int(utc[11:13]), int(utc[14:16]), int(utc[17:19]))
            - dt.datetime(2000, 1, 1, 0, 0, 0)).total_seconds()


def sec_to_utc(sec: float) -> dt.datetime:
    return dt.datetime(2000, 1, 1, 0, 0, 0) + dt.timedelta(seconds=sec)


def read_track(file: str) -> TRACK_TYPE:
    data = pd.read_csv(file, delimiter=";")
    data["time"] = data["time"].apply(utc_to_sec)
    data["buoy_station"].fillna(0, inplace=True)
    data["buoy_station"] /= data["station"]
    return data.to_numpy()


def read_sat_data(names: list) -> np.ndarray:
    res = np.ndarray(shape=(len(names),), dtype=list)
    for i in range(len(names)):
        files = glob.glob(names[i] + '/*.nc')
        files.sort()
        res[i] = [nc.Dataset(files[i]) for i in range(len(files))]
    return res


def check_nearest_data(sat: np.ndarray, sec: float) -> (int, int):
    data_len = np.array([sat[i].dimensions.get('time').size for i in range(len(sat))])
    min_in_data = np.zeros(shape=(int(np.sum(data_len)),))
    curr_num = 0
    for i in range(len(sat)):
        min_in_data[curr_num: curr_num + data_len[i]] = abs(np.array(sat[i].variables['time'][:]) - sec)
        curr_num += data_len[i]
    return np.argmin(min_in_data), np.min(min_in_data)


def get_coords(sat: list, fmin: (int, int), num: int) -> list:
    data_len = np.array([sat[i].dimensions.get('time').size for i in range(len(sat))])
    ind = 1
    while data_len[ind - 1] < fmin[0] < np.sum(data_len):
        ind += 1
        data_len[ind] += data_len[ind - 1]
    return [[sat[ind].variables['latitude'][fmin[0] - data_len[ind - 2] + i],
             sat[ind].variables['longitude'][fmin[0] - data_len[ind - 2] + i]] for i in range(-num, num)]


# def draw_map(lon_0: float, lat_0: float, height: float):
#     m = Basemap(projection='nsper', lon_0=lon_0, lat_0=lat_0, satellite_height=height * 1000., resolution='l')
#
#     m.scatter(xpt, ypt, color='red')
#
#     xpt, ypt = m(track_buoy_lon, track_buoy_lat)
#     m.scatter(xpt, ypt, color='green')
#
#     m.drawcoastlines()
#     m.fillcontinents()
#
#     m.drawparallels(np.arange(track_lat.min() - 10, track_lat.max() + 10, 5))  # , labels=[1, 1, 0, 1])
#     m.drawmeridians(np.arange(track_lon.min() - 10, track_lon.max() + 10, 5))  # , labels=[1, 1, 0, 1])
#
#     plt.show()


# def draw_coords(latlon: list, color: str):


track_ship = read_track('recources/AI57coords.csv')
sat_names = ['j3', 'cfo']
sat_data = read_sat_data(sat_names)

print(get_coords(sat_data[0], check_nearest_data(sat_data[0], track_ship[0, 3]), 10))
