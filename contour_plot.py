import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
from glob import glob

# from scipy.optimize import curve_fit

files_dir = r'FILEDIRECTORY/'
file_dir = glob(files_dir + '*.xy')

file_dir.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

file_dir.sort()  # for mac and linux system
number_files = len(file_dir)

df = []
i = 1
for f in file_dir:
    df.append(pd.read_csv(f, skiprows=[i for i in range(0, 23)], header=None, sep='\s+'))
    i = i + 1


twothetas = []
intensitys = []

for i in range(0, number_files):
    #twotheta = df[i].loc[:4100, 0].to_numpy()
    #intensity = df[i].loc[:4100, 1].to_numpy()
    twotheta = df[i].loc[:2963, 0].to_numpy()
    intensity = df[i].loc[:2963, 1].to_numpy()
    twothetas.append(twotheta)
    intensitys.append(intensity)

x = twothetas[15]
y = range(0, len(intensitys))

x_t, y_n = np.meshgrid(x, y)
z_i = np.array(intensitys, dtype=object)
# z_i is currently a 1D array of 1D arrays.
# We need to convert it to a 2D array that has the same shape as x_t and y_n.

# First, find the length of the longest 1D array.
max_length = 0
for i in range(0, len(z_i)):
    if len(z_i[i]) > max_length:
        max_length = len(z_i[i])

# Then, create a new 2D array that has the same shape as x_t and y_n.
z_i_new = np.zeros((len(z_i), max_length))
# Fill in the values from z_i.
for i in range(0, len(z_i)):
    for j in range(0, len(z_i[i])):
        z_i_new[i, j] = z_i[i][j]

# Finally, replace z_i with z_i_new.
z_i = z_i_new

z_i[z_i <= 0] = 0
z_i[z_i >= 20] = 18

fig = plt.figure(figsize=(10, 10))
gs = gridspec.GridSpec(1, 1)

ax0 = fig.add_subplot(gs[0])
ax0.tick_params(which='minor', length=2)

ax0.set_facecolor('white')

#ax0.contourf(x_t[36:], y_n[36:], z_i[36:], vmin=0, vmax=25, levels=50, cmap=cm.binary)
# cp = ax0.contourf(x_t[:37], y_n[:37], z_i[:37], vmin=0, vmax=9, levels=50, cmap=cm.binary)

cp = ax0.contourf(x_t, y_n, z_i, vmin=0, vmax=9, levels=50, cmap=cm.binary)
# ax0.axvline(x=7.3949, y color='red', linestyle='--')

ax0.annotate('PHASE1, HKL',xy=(7.45,2), c='r',fontsize=15, rotation=90)
ax0.annotate('PHASE1, HKL',xy=(8.6 ,2), c='r',fontsize=15, rotation=90)

ax0.annotate('PHASE2, HKL',xy=(12.3 ,2), c='r',fontsize=15, rotation=90)
ax0.annotate('PHASE2, HKL',xy=(14.4 ,2), c='r',fontsize=15, rotation=90)


ax0.set_xlabel('2theta')
ax0.set_ylabel('file no.')

fig.colorbar(cp)
plt.savefig('CONTOURPLOT.png')
plt.show()
