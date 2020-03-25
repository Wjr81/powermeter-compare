import gpxpy
import pandas as pd
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import numpy as np

quarq_file = open('/home/vinh/quarq.gpx', 'r')
tacx_file = open('/home/vinh/tacx.gpx', 'r')

quarq = gpxpy.parse(quarq_file)
tacx = gpxpy.parse(tacx_file)

def gpx2list(gpx):
    gpx_list = []
    for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    time = dates.date2num(point.time)
                    power = int(point.extensions[0].text)
                    gpx_list.append([time, power])
    return gpx_list

df = pd.DataFrame(gpx2list(quarq), columns=['time', 'quarq']).set_index('time')
tacx_df = pd.DataFrame(gpx2list(tacx), columns=['time', 'tacx']).set_index('time')
df['tacx'] = tacx_df.tacx
del tacx_df
df['quarq_3s'] = df.quarq.rolling(3).mean()
df['tacx_3s'] = df.tacx.rolling(3).mean()
df['difff'] = df.quarq_3s - df.tacx_3s

diff_list = []
for x in np.arange(df.quarq.max()):
    difff = df[df.quarq==x].difff.mean()
    sem = df[df.quarq==x].difff.sem()
    diff_list.append([difff, sem])

df_diff = pd.DataFrame(diff_list, columns=['mean_diff', 'semm'])
df_diff['mean_diff_rolling'] = df_diff.mean_diff.rolling(30).mean()

plt.plot(df_diff.mean_diff_rolling)
plt.fill_between(df_diff.index.to_series(), df_diff.mean_diff + df_diff.semm, df_diff.mean_diff - df_diff.semm, alpha = 0.5)
plt.plot(df_diff.index.to_series(), np.zeros(len(df_diff)))