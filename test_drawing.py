from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

fig = plt.figure()
track = pd.read_csv('recources/AI57coords.csv', sep=';')
track_lat = track["lat(deg)"].to_numpy()
track_lon = track["lon(deg)"].to_numpy()
track_buoy_lat = track[track["buoy_station"] > 0.]["lat(deg)"].to_numpy()
track_buoy_lon = track[track["buoy_station"] > 0.]["lon(deg)"].to_numpy()

m = Basemap(projection='nsper', lon_0=-22.5, lat_0=59, satellite_height=600 * 1000., resolution='l')

xpt, ypt = m(track_lon, track_lat)
m.scatter(xpt, ypt, color='red')

xpt, ypt = m(track_buoy_lon, track_buoy_lat)
m.scatter(xpt, ypt, color='green')

m.drawcoastlines()
m.fillcontinents()

m.drawparallels(np.arange(track_lat.min() - 10, track_lat.max() + 10, 5))  # , labels=[1, 1, 0, 1])
m.drawmeridians(np.arange(track_lon.min() - 10, track_lon.max() + 10, 5))  # , labels=[1, 1, 0, 1])

plt.show()
