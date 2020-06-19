import csv
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from firecracker_time_series import firecracker_time_series

# 6 "Admin2" county (Montgomery)
# 7 "Province_State" (Alabama)
# 9 & 10, latitude and longitude
# 12 to end index series
#
# -1 for corresponding index

# approximate radius of earth in km
R = 6373.0

nr = 3261
nd = 132
cases = np.empty((nr, nd))
counties = []
states = []
geo_coords = np.empty((nr, 2))  # [latitude, longitude]

with open('data/time_series_covid19_confirmed_US.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            DATE_MDY = row[11:]
            line_count += 1
        else:
            counties.append(row[5])
            states.append(row[6])
            cases[line_count-1, :] = np.array([int(v) for v in list(row[11:])])
            geo_coords[line_count-1, :] = np.array([float(v) for v
                                                    in list(row[8:10])])
            line_count += 1
    print(f'Processed {line_count} cases.')

# need to convert the dates.
# month, day, year
# DATE_MDY

# County (and state) with very first case in US.
just_index = cases.sum(axis=0)
earliest_index_index = np.min(np.where(just_index))
first_place_index = np.min(np.where(cases[:, earliest_index_index]))
DO_STATE = states[first_place_index]
COUNTY_ONE = counties[first_place_index]

do_counties = [i for (i, s) in enumerate(states) if s == DO_STATE]
county_rows = np.array(do_counties)

# Subset
sub_cases = cases[county_rows[0:-2], :]
sub_geo = geo_coords[county_rows[0:-2], :]
sub_counties = np.array(counties)[county_rows[0:-2]]

SUB_COUNTY_ONE = np.where(sub_counties == COUNTY_ONE)[0][0]
geo_one = sub_geo[SUB_COUNTY_ONE, :]

delta = np.radians(sub_geo) - np.radians(geo_one)
a = (np.sin(delta[:, 0]/2)**2 + np.cos(geo_one[0]) * np.cos(sub_geo[:, 0]) *
     np.sin(delta[:, 1]/2)**2)
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
distance_km = R * c

do_n_counties = min(14, delta.shape[0])
near_to_far_ind = np.argsort(distance_km)
M = np.transpose(sub_cases[near_to_far_ind[0:do_n_counties-1], :])
C = sub_counties[near_to_far_ind[0:do_n_counties-1]]
D = distance_km[near_to_far_ind[0:do_n_counties-1]]

G = np.diff(M, axis=0)
index = np.arange(0, G.shape[0]) + 1

win_len = 7
win = signal.hann(win_len)

temp_win = np.zeros((win_len,))
temp_win[3] = 1
index_of_filt_G = signal.convolve(index, temp_win, mode='valid')

filt_G = np.zeros((index_of_filt_G.shape[0], do_n_counties))
for i in range(G.shape[1]):
    filt_G[:, i] = signal.convolve(G[:, i], win, mode='valid') / sum(win)

xlim_global = [min(index_of_filt_G), max(index_of_filt_G)]
y_range_type = "zero_to_max"
y_value_label = "Confirmed cases"

# --------------------------------------------------------------
# Make figure.
fig = firecracker_time_series(filt_G, time=index_of_filt_G,
                              y_value_label=y_value_label, events=None,
                              xlim_global=xlim_global, verticals=None,
                              y_range_type=y_range_type, y_scale="log")

# Label x axis.
xl_txt = "Day since first case in US"
fontdict = {'fontsize': 16}
labelpad = 5
plt.xlabel(xl_txt, fontdict=fontdict, labelpad=labelpad)

# Show and print.
plt.show()
# if fig is not None:
#     fig.savefig("test_scripts_S" + str(subject_id) + ".pdf",
#                 bbox_inches='tight')
# --------------------------------------------------------------
DO_STATE = "New York"
do_counties = [i for (i, s) in enumerate(states) if s == DO_STATE]
county_rows = np.array(do_counties)

# Subset
sub_cases = cases[county_rows[0:-2], :]
sub_geo = geo_coords[county_rows[0:-2], :]
sub_counties = np.array(counties)[county_rows[0:-2]]

day_one = np.where(sub_cases.sum(axis=0) > 0)[0].min()
first_county_loc = np.where(sub_cases[:, day_one])[0].min()
COUNTY_ONE = sub_counties[first_county_loc]

sub_cases = sub_cases[:, day_one:]

geo_one = sub_geo[first_county_loc, :]


delta = np.radians(sub_geo) - np.radians(geo_one)
a = (np.sin(delta[:, 0]/2)**2 + np.cos(geo_one[0]) * np.cos(sub_geo[:, 0]) *
     np.sin(delta[:, 1]/2)**2)
c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
distance_km = R * c

# First few
near_to_far_ind = np.argsort(distance_km)[0:14]

# Every 4th (14)
# near_to_far_ind = np.argsort(distance_km)[:-9:4]

do_n_counties = 14

M = np.transpose(sub_cases[near_to_far_ind, :])
C = sub_counties[near_to_far_ind]
D = distance_km[near_to_far_ind]

G = np.diff(M, axis=0)
index = np.arange(0, G.shape[0]) + 1

win_len = 7
win = signal.hann(win_len)

temp_win = np.zeros((win_len,))
temp_win[3] = 1
index_of_filt_G = signal.convolve(index, temp_win, mode='valid')

filt_G = np.zeros((index_of_filt_G.shape[0], do_n_counties))
for i in range(G.shape[1]):
    filt_G[:, i] = signal.convolve(G[:, i], win, mode='valid') / sum(win)

xlim_global = [min(index_of_filt_G), max(index_of_filt_G)]
y_range_type = "zero_to_max"
y_value_label = "Confirmed cases"

# Make figure.
fig = firecracker_time_series(filt_G, time=index_of_filt_G,
                              y_value_label=y_value_label, events=None,
                              xlim_global=xlim_global, verticals=None,
                              y_range_type=y_range_type, y_scale="log",
                              conditions=list(C))

# Label x axis.
xl_txt = "Day since first case in New York state"
fontdict = {'fontsize': 16}
labelpad = 5
plt.xlabel(xl_txt, fontdict=fontdict, labelpad=labelpad)

# Show and print.
plt.show()
# if fig is not None:
#     fig.savefig("test_scripts_S" + str(subject_id) + ".pdf",
#                 bbox_inches='tight')
