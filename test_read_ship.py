import pandas as pd

track = pd.read_csv('recources/AI57coords.csv', sep=';')
print(track)

# for station in track[['lat(deg)', 'lon(deg)']]:
print(track['lat(deg)'].to_numpy())
print(track['lon(deg)'].to_numpy())


