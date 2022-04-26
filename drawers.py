from mpl_toolkits.basemap import Basemap
import numpy as np


def make_map(lon_0: float, lat_0: float, height: float) -> Basemap:
    """
    отрисовывает карту
    :param lon_0: долгота центральной точки
    :param lat_0: широта центральной точки
    :param height: высота спутника
    :return: карта
    """
    m = Basemap(projection='nsper', lon_0=lon_0, lat_0=lat_0, satellite_height=height * 1000., resolution='l')
    m.drawcoastlines()
    m.fillcontinents()
    return m


def draw_grid(m: Basemap):
    """
    отрисовывает сетку на карте
    :param m: карта
    """
    m.drawparallels(np.arange(-90, 90, 5))
    m.drawmeridians(np.arange(0, 360, 5))


def draw_coords(m: Basemap, track_lat: np.ndarray, track_lon: np.ndarray, color: str):
    """
    отрисовывает трек на карте
    :param m: карта
    :param track_lat: широты трека
    :param track_lon: долготы трека
    :param color: цвет
    """
    xpt, ypt = m(track_lon, track_lat)
    m.scatter(xpt, ypt, color=color)


def draw_point(m: Basemap, lat_lon: np.ndarray, color: str):
    """
    отрисовывает одну точку на карте
    :param m: карта
    :param lat_lon: [широта, долгота] точки
    :param color: цвет
    """
    xpt, ypt = m(lat_lon[1], lat_lon[0])
    m.scatter(xpt, ypt, color=color)
