import readers
import checkers
import drawers
import matplotlib.pyplot as plt

plt.figure()

track_ship = readers.read_track('recources/AI57coords.csv')
sat_names = ['j3', 'cfo', 's3a', 's3b']
sat_data = readers.read_sat_data(sat_names)

# print(checkers.get_area_coords(sat_data[0], checkers.check_nearest_data(sat_data[0], track_ship[0, 3]), 10))

map = drawers.make_map(lon_0=-22.5, lat_0=59, height=1000)
drawers.draw_grid(map)
drawers.draw_coords(map, track_lat=track_ship[:, 1], track_lon=track_ship[:, 2], color='green')

colors = ['red', 'blue', 'purple', 'orange']

for i in range(len(track_ship[:, 3])):
    k = -1
    for sat_dat in sat_data:
        k += 1
        sat_near_ship = checkers.get_area_coords(sat_dat, checkers.check_nearest_data(sat_dat, track_ship[i, 3]), 20)
        # print(sat_near_ship)
        for i in range(len(sat_near_ship)):
            # print(lat_lon)
            # print(lat_lon)
            # if checkers.is_near_sat(sat_near_ship[i], track_ship[i, 1:3], 10000):
            #     print('llll')
            drawers.draw_point(map, sat_near_ship[i], colors[k])

plt.show()
