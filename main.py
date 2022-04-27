import readers
import checkers
import drawers
import matplotlib.pyplot as plt
import numpy as np

WIN_TIME = 3600  # окно по времени в секундах
WIN_ANGLE = 2  # окно по координате в градусах
ONLY_BUOY = False  # обрабатывать только точки, в которых производились изерения

plt.figure()

# чтение треков
track_ship = readers.read_track('recources/AI57coords.csv')
sat_names = ['j3', 'cfo', 's3a', 's3b', 'al', 'h2b']
sat_data = readers.read_sat_data(sat_names)

print("tracks uploaded successfully")

# отрисовка карты
map = drawers.make_map(lon_0=-22.5, lat_0=59, height=600)
drawers.draw_grid(map)
drawers.draw_coords(map, track_lat=track_ship[:, 1], track_lon=track_ship[:, 2], track_buoy=track_ship[:, 4],
                    color1='gray', color2='black')
colors = ['red', 'yellow', 'orange', 'green', 'blue', 'purple']

# отрисовка легенды
for l in range(len(sat_names)):
    xpt, ypt = map(sat_data[0][1][0], sat_data[0][0][0])
    map.scatter(xpt, ypt, color=colors[l], label=sat_names[l])
plt.legend(loc="upper right")

for t in range(len(track_ship[:, 3])):  # цикл по времени
    color_num = -1

    for sat_dat in sat_data:  # цикл по спутникам
        color_num += 1
        sat_near_ship = checkers.get_area_coords(sat_dat, checkers.check_nearest_data(sat_dat, track_ship[t, 3]),
                                                 WIN_TIME)

        for p in range(len(sat_near_ship[0])):  # цикл по точкам в куске траектории, находящемся в окне по времени
            lat_lon = np.array([sat_near_ship[0][p], sat_near_ship[1][p]])
            if checkers.is_near_sat(lat_lon, track_ship[t, 1:5], WIN_ANGLE, buoy=ONLY_BUOY):
                drawers.draw_point(map, lat_lon, colors[color_num])

plt.show()
