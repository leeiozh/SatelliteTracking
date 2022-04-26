import datetime as dt


def utc_to_sec(utc: str) -> float:
    """
    конвертер из utc в секунды с J2000
    :param utc: время в utc
    :return: время в секундах с J2000
    """
    return (dt.datetime(int(utc[6:10]), int(utc[3:5]), int(utc[:2]), int(utc[11:13]), int(utc[14:16]), int(utc[17:19]))
            - dt.datetime(2000, 1, 1, 0, 0, 0)).total_seconds()


def sec_to_utc(sec: float) -> dt.datetime:
    """
    конвертер из секунд с J2000 в utc
    :param sec: время в секундах с J2000
    :return:  время в utc
    """
    return dt.datetime(2000, 1, 1, 0, 0, 0) + dt.timedelta(seconds=sec)
