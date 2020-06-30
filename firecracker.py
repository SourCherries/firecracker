""" This module contains a single function, firecracker, that produces a figure
of multiple time series that are stacked horizontally. A color gradient is
applied to each series so that one can use both the height of the y axis and
color in order to visually compare the shape and relative magnitude of the
different series."""

# External dependencies
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import interpolate


# Main and only function
def firecracker(M, time, label_colorbar, labels_series=None,
                times_markers=None, times_vert_lines=[], xlim_global=None,
                y_range_type="min_to_max", y_scale="linear", layers=False,
                upsample=1):
    """

    Make a 'firecracker' time series:
    a colorful figure of multiple time series.

    Time series are stacked horizontally.
    A color gradient is applied to each series so that an observer can use both
    the height of the y axis and color in order to visually compare the shape
    and relative magnitude of the different series.

    Parameters
    ----------
    M : numpy.ndarray
        2d matrix of time-series data: Time x series
    time : numpy.ndarray
        1d time values
    label_colorbar : str
        label for y-axis values. displayed on colorbar, not on y axis.
    labels_series : list
        list of strings to label each series
    times_markers : list
        list of times to mark a specific event in each series
    times_vert_lines : scalar or list
        x-axis value(s) for vertical line(s) spanning all series
    xlim_global : list
        x-axis limits (for all series)
    y_range_type : str
        method for setting y-axis range
            "min_to_max", "symmetric_around_zero", "zero_to_max"
    y_scale : str
        type of y axis: "linear" or "log"
    layers : bool
        from top to bottom, series are 'occluded' by subsequent series.
    upsample : int
        interpolate to increase number of samples: upsample x original number.


    Returns
    -------
    matplotlib.figure.Figure
        Figure object that can be further modified.

    """
    # Shape of data and check consistency.
    number_frames, number_series = M.shape
    checks = []
    checks.append(int(time.shape[0] == number_frames))
    if labels_series is not None:
        checks.append(int(len(labels_series) == number_series))
    if times_markers is not None:
        checks.append(int(len(times_markers) == number_series))
    if not np.prod(checks):
        print("Some input dimensions do not match up.")
        return None

    if (isinstance(times_vert_lines, float) or
            isinstance(times_vert_lines, int)):
        times_vert_lines = [times_vert_lines]

    assert isinstance(upsample, int), 'upsample should be int'

    # Linear interpolate to obtain greater sample of points.
    #   This module uses point-drawing to display color gradient.
    #   In some cases, large derivative causes points to be seen,
    #   instead of a smooth line. In that case, let's interpolate
    #   to give impression of line instead of points.
    if upsample > 1:
        inter_fun = interpolate.interp1d(time, M, axis=0)
        number_frames_fine = number_frames * upsample
        time = np.linspace(time.min(), time.max(), number_frames_fine)
        M = inter_fun(time)
        number_frames = number_frames_fine

    # If y axis is log scale, then color gradient should also be log scale.
    if y_scale is "log":
        eps = np.finfo(float).eps
        CM = np.log10(M - M.min() + eps)
    else:
        CM = M

    # Display parameters.
    FontSize = 12
    plt.rcParams.update({'font.size': FontSize})
    f_height_inches = 7  # Window position and size.
    mult_y = 1.3  # Scalar to stretch y axis range
    mult_c = 1.0  # Scalar to stretch color range

    # Common scales for color gradients and y axes.
    if y_range_type is "symmetric_around_zero":
        maxAbsY = round(np.abs(M).max() * mult_y)
        ylim_global = [-maxAbsY, maxAbsY]

        cmap = 'coolwarm'
        event_color = "#31a354"
        maxAbsC = round(np.abs(M).max() * mult_c)
        clim_global = [-maxAbsC, maxAbsC]
    elif y_range_type is "min_to_max":
        maxv = M.max()
        minv = M.min()
        new_range = (maxv - minv) * mult_y
        midv = (maxv-minv)/2 + minv
        ylim_global = [midv - new_range/2, midv + new_range/2]

        maxv = CM.max()
        minv = CM.min()
        new_range = (maxv - minv) * mult_c
        midv = (maxv-minv)/2 + minv

        clim_global = [midv - new_range/2, midv + new_range/2]
        cmap = 'inferno'
        event_color = "#31a354"

        if layers:
            cmap = 'viridis_r'  # viridis_r for layers.

    elif y_range_type is "zero_to_max":
        ylim_global = [0, M.max()*mult_y]

        clim_global = [0, CM.max()*mult_c]
        cmap = 'inferno'
        event_color = "#31a354"
    else:
        print("Invalid value for y_range_type.")
        return None

    # Adjust marker size.
    nms = 256 / number_series  # 84
    nms = max(int(np.log2(nms)), 1)
    dms = mpl.rcParams['lines.markersize']
    mpl.rcParams['lines.markersize'] = nms

    args = {}
    args['number_series'] = number_series
    args['time'] = time
    args['M'] = M
    args['CM'] = CM
    args['cmap'] = cmap
    args['clim_global'] = clim_global
    args['y_scale'] = y_scale
    args['xlim_global'] = xlim_global
    args['ylim_global'] = ylim_global
    args['times_markers'] = times_markers
    args['event_color'] = event_color
    args['labels_series'] = labels_series
    args['times_vert_lines'] = times_vert_lines

    if layers:
        fig, sp, axs = _layers(args)
        # final_axis = axs
    else:
        fig, sp, axs = _vanilla(args)
        # final_axis = axs[-1]

    # Colorbar.
    fig.colorbar(sp, ax=axs, shrink=0.6, label=label_colorbar)

    # Sizing of figure and display.
    aspect_ratio = 1.76
    if number_series > 25:
        aspect_ratio = 1.2
    w_height_inches = f_height_inches * aspect_ratio
    fig.set_size_inches((w_height_inches, f_height_inches))

    # Restore default marker size.
    mpl.rcParams['lines.markersize'] = dms
    return fig


# Helper functions: _vanilla() and _layers()
def _vanilla(args):
    number_series = args['number_series']
    time = args['time']
    M = args['M']
    CM = args['CM']
    cmap = args['cmap']
    clim_global = args['clim_global']
    y_scale = args['y_scale']
    xlim_global = args['xlim_global']
    ylim_global = args['ylim_global']
    times_markers = args['times_markers']
    event_color = args['event_color']
    labels_series = args['labels_series']
    times_vert_lines = args['times_vert_lines']

    # Initial plot to determine appropriate x ticks based
    #   on Matplotlib defaults.
    fig, axs = plt.subplots(number_series, 1, sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0)
    axs[0].scatter(time, M[:, 0], s=None, c=CM[:, 0], cmap=cmap,
                   vmin=clim_global[0], vmax=clim_global[1])
    axs[0].set_yscale(y_scale)
    axs[0].set_xlim(xlim_global[0], xlim_global[1])
    x_ticks = axs[0].get_xticks()
    plt.close(fig)

    # Plot each time series.
    #   Ensure appropriate ranges.
    #   Set spines to be invisible except for bottom spine for bottom series.
    fig, axs = plt.subplots(number_series, 1, sharex=False, sharey=False)
    fig.subplots_adjust(hspace=0)
    for i in range(number_series):
        sp = axs[i].scatter(time, M[:, i], s=None, c=CM[:, i], cmap=cmap,
                            vmin=clim_global[0], vmax=clim_global[1])
        axs[i].set_yscale(y_scale)
        if times_markers is not None:
            mid_val = M[:, i].mean()
            if times_markers[i] is not None:
                e1 = axs[i].plot(times_markers[i], mid_val, '|', ms=14, mew=3,
                                 color=event_color)
            else:
                mid_pnt = int(len(time)/2)
                e1 = axs[i].plot(time[mid_pnt], mid_val, '|', ms=14, mew=3,
                                 color=event_color)
                eh = e1[0]
                eh.set_visible(False)

        axs[i].set_xlim(xlim_global[0], xlim_global[1])
        axs[i].spines['left'].set_visible(False)
        axs[i].spines['right'].set_visible(False)
        axs[i].spines['bottom'].set_visible(False)
        axs[i].spines['top'].set_visible(False)
        axs[i].set_xticks([])
        axs[i].set_yticks([])
        if labels_series is not None:
            if labels_series[i] is not None:
                axs[i].set_ylabel(labels_series[i], rotation=0, labelpad=35)

    axs[-1].spines['bottom'].set_visible(True)
    axs[-1].set_xticks(x_ticks)

    # Ensure y-axis ranges are uniform and stretched out enough to fit data.
    for ax in axs:
        ax.set_ylim(ylim_global)
        ax.set_xlim(xlim_global)

    # Vertical line spanning sub plots.
    for xv in times_vert_lines:
        xarange = xlim_global[1] - xlim_global[0]
        txp = (xv - xlim_global[0]) / xarange
        ax.plot([txp, txp], [0, number_series], 'k--',
                transform=ax.transAxes,
                clip_on=False, ms=14, mew=3)

    return fig, sp, axs


def _layers(args):
    number_series = args['number_series']
    time = args['time']
    M = args['M']
    CM = args['CM']
    cmap = args['cmap']
    clim_global = args['clim_global']
    xlim_global = args['xlim_global']
    times_markers = args['times_markers']
    event_color = args['event_color']
    labels_series = args['labels_series']
    times_vert_lines = args['times_vert_lines']

    if labels_series is not None:
        xr = xlim_global[1] - xlim_global[0]
        xt = xlim_global[0] - 0.22 * xr

    bottom_y = M.min()
    y_spacing = 5
    y_shifts = np.linspace(0, number_series*y_spacing, number_series)
    y_shifts = y_shifts[::-1]
    fig, axs = plt.subplots(1, 1)
    fig.set_size_inches(7, 10)
    for i, ys in enumerate(y_shifts):
        axs.fill_between(time, M[:, i] + ys, bottom_y, color="w")
        sp = axs.scatter(time, M[:, i] + ys, s=None,
                         c=CM[:, i], cmap=cmap,
                         vmin=clim_global[0], vmax=clim_global[1])
        if labels_series is not None:
            if labels_series[i] is not None:
                axs.text(xt, ys, s=labels_series[i])

    axs.spines['left'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.spines['top'].set_visible(False)
    axs.set_yticks([])

    if times_markers is not None:
        for i, ys in enumerate(y_shifts):
            mid_val = M[:, i].mean()
            if times_markers[i] is not None:
                e1 = axs.plot(times_markers[i], mid_val + ys, '|',
                              ms=14, mew=3, color=event_color)
            else:
                mid_pnt = int(len(time)/2)
                e1 = axs.plot(time[mid_pnt], mid_val + ys, '|',
                              ms=14, mew=3, color=event_color)
                eh = e1[0]
                eh.set_visible(False)

    # Vertical line spanning sub plots.
    for xv in times_vert_lines:
        axs.plot([xv, xv], sp.axes.get_ylim(), 'k--', ms=14, mew=3)

    return fig, sp, axs
