import netCDF4 as nc
import numpy as np
import datetime
import pandas as pd


def getclosest_ij(lats, lons, latpt, lonpt):
    dist_sq = (lats - latpt) ** 2 + (lons - lonpt) ** 2
    minindex_flattened = dist_sq.argmin()
    return minindex_flattened


track = pd.read_csv('recources/AI57coords.csv', sep=';')
track_lat = track["lat(deg)"].to_numpy()
track_lon = track["lon(deg)"].to_numpy()
track_buoy_lat = track[track["buoy_station"] > 0.]["lat(deg)"].to_numpy()
track_buoy_lon = track[track["buoy_station"] > 0.]["lon(deg)"].to_numpy()

fn = '/home/leeiozh/ocean/CopernicusData/j3/global_vavh_l3_rt_j3_20210701T000000_20210701T030000_20210701T060429.nc'
ds = nc.Dataset(fn)

print(ds.dimensions.get('time').size)

secs = np.array(ds.variables['time'][:])
print(secs)

lat, lon = ds.variables['latitude'], ds.variables['longitude']

latvals = lat[:]
lonvals = lon[:]

# dict_keys(['time', 'latitude', 'longitude', 'VAVH', 'VAVH_UNFILTERED', 'WIND_SPEED'])
