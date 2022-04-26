import numpy as np


def check_nearest_data(sat: np.ndarray, sec: float) -> (int, float):
    """
    находит ближайшую по времени точку данных со спутника
    :param sat: данные со спутнка
    :param sec: время снятия измерений
    :return: индекс ближайшей по времени точки и ее разницу во времени
    """
    return np.argmin(abs(sat[0] - sec)), np.min(abs(sat[0] - sec))


def get_area_coords(sat: np.ndarray, fmin: (int, float), num: int) -> np.ndarray:
    """
    возвращает кусок траектории спутника в окрестности точки, ближайшей по времени с заданным окном по времени
    :param sat: данные со спутника
    :param fmin: (индекс ближайщей по времени точки, разница во времени)
    :param num: окно по данным
    :return: [широта спутника в указанном окне, долгота спутника в указанном окне]
    """
    if fmin[0] - num > 0 and fmin[0] + num < len(sat[1]):
        return np.array([[sat[1][fmin[0] + i], sat[2][fmin[0] + i]] for i in range(-num, num + 1)])


def is_near_sat(sat_area: np.ndarray, track: np.ndarray, deg: float) -> bool:
    """
    проверяет, находится ли спутник в окрестности положения судна
    :param sat_area: кусок траектории спутника
    :param track: координаты судна
    :param deg: окно по координатам в градусах
    :return: попадает ли кусок траектории спутника в окно трека судна
    """
    if np.linalg.norm(sat_area - track) < deg:
        return True
    else:
        return False
