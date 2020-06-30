import numpy as np
import matplotlib.pyplot as plt
from firecracker import firecracker

import csv

nf = 300  # time frames
ns = 80   # series, pulsar number

total_sec = 107
series_ms = total_sec * 1000 / ns
ms = np.linspace(0, series_ms, nf)

pulsars = np.empty((nf, ns))
with open('data/pulsar.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        pulsars[:, line_count] = np.array([float(v) for v in list(row)])
        line_count += 1

# # Butterfly - spaghetti -  plot.
# plt.plot(pulsars)
# print([pulsars.min(), pulsars.max()])

# --------------------------------------------------------------
# Firecracker figure.
xlim_global = [0, series_ms]
layers = True
fig = firecracker(pulsars, time=ms, label_colorbar="Radio intensity",
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
