import numpy as np
import matplotlib.pyplot as plt
from firecracker import firecracker

import csv

# Load a long time series of radio intensities
total_samples = 24000
ms = np.empty((total_samples,))         # milliseconds
intensity = np.empty((total_samples,))  # radio intensity
with open('data/pulsar_readable.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    headers = next(csv_reader)
    line_count = 0
    for row in csv_reader:
        ms[line_count] = float(list(row)[0])
        intensity[line_count] = float(list(row)[1])
        line_count += 1

# Break this down into apparent periods (epochs)
ne = 80                         # number of epochs
nf = int(total_samples / ne)    # samples per epoch
epochs = intensity.reshape((ne, nf))
epochs = np.transpose(epochs)
ms_epoch = ms[0:nf]


# Firecracker figure.
xlim_global = [0, ms_epoch[-1]]
layers = True
fig = firecracker(epochs, time=ms_epoch, label_colorbar="Radio intensity",
                  xlim_global=xlim_global, y_range_type="min_to_max",
                  upsample=4, layers=layers)

# Label x axis.
xl_txt = "Time during pulse, milliseconds"
fontdict = {'fontsize': 16}
labelpad = 5
plt.xlabel(xl_txt, fontdict=fontdict, labelpad=labelpad)

# Show and print.
plt.show()
if layers:
    file_end = "-layers.png"
else:
    file_end = ".png"
if fig is not None:
    fig.savefig("fig-pulsar" + file_end,
                bbox_inches='tight')
