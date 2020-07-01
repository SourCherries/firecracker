import numpy as np
import matplotlib.pyplot as plt
from firecracker import firecracker

# --------------------------------------------------------------
# Get data for single subject. Mean ERP across 14 labels_series.
subject_id = 7
number_series = 14

# Time scale.
ms_per_sample = 2
ms = np.arange(start=-1000, stop=1000+ms_per_sample, step=ms_per_sample)
number_frames = ms.size

M = np.fromfile("data/MERP_S" + str(subject_id) + ".bin")
M = M.reshape((-1, number_series), order='F')

# An event should be marked in the plot for each ERP:
#   Presentation of previous image, evoking an earlier brain response.
event_a_dur_ms = 250
event_a_ms = np.append(np.arange(0, 600+50, 50) * -1 - event_a_dur_ms, None)

# Condition labels (inter-stimulus-intervals)
ISI = [str(v)+" ms" for v in list(np.arange(0, 600+50, 50))]
ISI.append("N170")

# Ensure data as expected.
M.shape[0] == ms.shape[0]
M.shape[1] == number_series
event_a_ms.shape[0] == number_series

# Range of x axis in milliseconds.
#   Data range from -1000 to 1000 ms.
xlim_global = [-900, 600]


# --------------------------------------------------------------
# Make figure.
layers = True

fig = firecracker(M, time=ms, label_colorbar="Voltage",
                  times_markers=event_a_ms, xlim_global=xlim_global,
                  times_vert_lines=0, y_range_type="symmetric_around_zero",
                  labels_series=ISI, upsample=1, layers=layers)

# Label x axis.
xl_txt = "Time since event, milliseconds"
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
    fig.savefig("fig-erp" + file_end,
                bbox_inches='tight')
