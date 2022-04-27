import netCDF4 as nc
import numpy as np
import pandas as pd
import glob
import converters

TRACK_TYPE = np.ndarray(shape=(5,), dtype=float)


def read_track(file: str) -> TRACK_TYPE:
    """
    чтение данных о треке судна
    :param file: путь к файлу
    :return: данные из файла с переведенным временем
    """
    data = pd.read_csv(file, delimiter=";")
    data["time"] = data["time"].apply(converters.utc_to_sec)
    data["buoy_station"].fillna(0, inplace=True)
    data["buoy_station"] /= data["station"]
    return data.to_numpy()


def read_sat_data(names: list) -> np.ndarray:
    """
    чтенеи данных со спутника
    :param names: имена спутников (совпадают с именем папки)
    :return: массив массивов данных
    """
    res = np.ndarray(shape=(len(names), 4), dtype=np.ndarray)
    for i in range(len(names)):
        files = glob.glob('recources/' + names[i] + '/*.nc')
        files.sort()

        res[i, 0] = np.array(nc.Dataset(files[0]).variables['time'][:])
        res[i, 1] = np.array(nc.Dataset(files[0]).variables['latitude'][:])
        res[i, 2] = np.array(nc.Dataset(files[0]).variables['longitude'][:])
        res[i, 3] = np.array(nc.Dataset(files[0]).variables['VAVH'][:])

        for j in range(0, len(files)):
            ds = nc.Dataset(files[j])
            res[i, 0] = np.append(res[i, 0], np.array(ds.variables['time'][:]))
            res[i, 1] = np.append(res[i, 1], np.array(ds.variables['latitude'][:]))
            res[i, 2] = np.append(res[i, 2], np.array(ds.variables['longitude'][:]))
            res[i, 3] = np.append(res[i, 3], np.array(ds.variables['VAVH'][:]))
    return res
