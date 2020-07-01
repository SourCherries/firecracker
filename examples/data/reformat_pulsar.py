import numpy as np
import csv

nf = 300  # time frames
ns = 80   # series, pulsar number

total_sec = 107
total_ms = total_sec * 1000
ms = np.linspace(0, total_ms, nf * ns)

pulsars = np.empty((ns, nf))
with open('pulsar.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        pulsars[line_count, :] = np.array([float(v) for v in list(row)])
        line_count += 1

pulsars = pulsars.reshape((-1, ))

np.savetxt('pulsar_readable.csv', np.c_[ms, pulsars], delimiter=",",
           fmt="%1.2f", header="milliseconds,radio_intensity")
