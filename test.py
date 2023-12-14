import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde, norm

l = {31.2: 1, 35.1: 4, 39.0: 13, 42.9: 33, 46.8: 115, 50.7: 271, 54.6: 363, 58.5: 381, 62.4: 379, 66.3: 370, 70.2: 256, 74.1: 47, 78.0: 2}
# convert the dictionary to a list
l_array = np.array( [k for k, v in l.items() for _ in range(v)])


s = sum(l.values())
bin_width = 3.9
bin_centers = list(l.keys())
heights = [v/s/bin_width for v in l.values()]
plt.bar(bin_centers, heights, width=bin_width*0.9, color='dodgerblue', label='histogram')
for c, h, v in zip(bin_centers, heights, l.values()):
    plt.text(c, h, v, ha='center', va='bottom')
plt.xticks(bin_centers)
mean = l_array.mean()
sdev = l_array.std()
for i in range(-3, 4):
    plt.axvline(mean+i*sdev, color='limegreen', ls='--', lw=2, label='mean + i*sdev' if i == 0 else None)

x = np.linspace(mean-4*sdev, mean+4*sdev, 500)
plt.plot(x, norm.pdf(x, mean, sdev), color='orange', lw=3, label='gaussian normal')
plt.autoscale(enable=True, axis='x', tight=True)
plt.legend()
plt.show()