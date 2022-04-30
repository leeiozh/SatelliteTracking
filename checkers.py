import numpy as np


def check_nearest_data(sat: np.ndarray, sec: float) -> (int, float):
    """
    находит ближайшую по времени точку данных со спутника
    :param sat: данные со спутнка
    :param sec: время снятия измерений
    :return: индекс ближайшей по времени точки и ее разницу во времени
    """
    return np.argmin(abs(sat[0] - sec)), np.min(abs(sat[0] - sec))


def get_area_coords(sat: np.ndarray, fmin: (int, float), num: int) -> (np.ndarray, np.ndarray):
    """
    возвращает кусок траектории спутника в окрестности точки, ближайшей по времени с заданным окном по времени
    :param sat: данные со спутника
    :param fmin: (индекс ближайщей по времени точки, разница во времени)
    :param num: окно по данным
    :return: [широта спутника в указанном окне, долгота спутника в указанном окне]
    """
    start = max(0, fmin[0] - num)
    end = min(fmin[0] + num + 1, len(sat[1]))
    return sat[1][start:end], sat[2][start:end]


def is_near_sat(sat_area: np.ndarray, track: np.ndarray, deg: float, buoy: bool) -> bool:
    """
    проверяет, находится ли спутник в окрестности положения судна
    :param sat_area: кусок траектории спутника
    :param track: координаты судна
    :param deg: окно по координатам в градусах
    :return: попадает ли кусок траектории спутника в окно трека судна
    """
    if not buoy:  # обрабатывать все точки
        if track[1] < 0:  # перевод долготы трека в долготу спутника
            tmp_track = [track[0], track[1] + 360]
            if np.abs(np.linalg.norm(sat_area - tmp_track)) < deg:
                return True
            else:
                return False
        else:
            if np.abs(np.linalg.norm(sat_area - track[:2])) < deg:
                return True
            else:
                return False
    else:  # обрабатывать только точки с буями
        if track[1] * track[-1] < 0:  # перевод долготы трека в долготу спутника
            tmp_track = [track[0] * track[-1], track[1] * track[-1] + 360]
            if np.abs(np.linalg.norm(sat_area - tmp_track)) < deg:
                return True
            else:
                return False
        else:
            if np.abs(np.linalg.norm(sat_area - track[:2] * track[-1])) < deg:
                return True
            else:
                return False
