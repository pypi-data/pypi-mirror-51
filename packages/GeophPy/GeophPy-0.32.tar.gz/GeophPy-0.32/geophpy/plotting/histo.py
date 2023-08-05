# -*- coding: utf-8 -*-
'''
    geophpy.plotting.histo
    ----------------------

    Histogram Plot Management.

    :copyright: Copyright 2014-2019 Lionel Darras, Philippe Marty, Quentin Vitale and contributors, see AUTHORS.
    :license: GNU GPL v3.

'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import geophpy.plotting.plot as plot1D

from mpl_toolkits.axes_grid1 import make_axes_locatable

#def plot(dataset, fig=None, filename=None, zmin=None, zmax=None, cmapname=None, creversed=False, cmapdisplay=True, coloredhisto=True, dpi=None, transparent=False, valfilt=True):
def plot(dataset, **kwargs):
    ''' Plot the dataset histogram.

    cf. :meth:`~geophpy.dataset.DataSet.histo_plot`

    '''

    # Retrieving options #######################################################
    # Plot options
    fig = kwargs.get('fig', None)
    zmin = kwargs.get('zmin', None)
    zmax = kwargs.get('zmax', None)
    cmapname = kwargs.get('cmapname', None)
    creversed = kwargs.get('creversed', False)
    cmapdisplay = kwargs.get('cmapdisplay', True)
    coloredhisto = kwargs.get('coloredhisto', True)
    valfilt = kwargs.get('valfilt', False)
    colorbar = None

    # Saving options
    filename = kwargs.get('filename', None)
    dpi = kwargs.get('dpi', None)
    transparent = kwargs.get('transparent', False)

    # Reversed colormap ########################################################
    if creversed:
        cmapname = cmapname + '_r'  # adds '_r' at the colormap name to use the reversed colormap

    cmap = plt.get_cmap(cmapname)  # gets the colormap


    # Figure initialization
    fig, ax = plot1D._init_figure(fig=fig)  # clear an existing figure and add an empty ax


    # First display ############################################################
    #if fig is None:
    #    fig = plt.figure()
    #else:
    #    fig.clf()

    # Ignoring NaNs ############################################################
    # Dataset values
    if valfilt or dataset.data.z_image is None:
        nanidx = np.isnan( dataset.data.values.T[0] )  # index of nan
        Z = dataset.data.values.T[2][~nanidx]

    # Dataset zimage
    else:
        nanidx = np.isnan( dataset.data.z_image )  # index of nan
        Z = dataset.data.z_image[~nanidx]

    # Creating histogram #######################################################
    # Data range
    nbins = 100
    if zmin is None:
        zmin = Z.min()
    if zmax is None:
        zmax = Z.max()

    # Histogram
    #n, bins, patches = plt.hist(Z.flatten(), bins=nbins, range=(zmin, zmax), facecolor='black', alpha=1)
    #hst = plt.gca()
    n, bins, patches = ax.hist(Z.flatten(), bins=nbins, range=(zmin, zmax), facecolor='black', alpha=1)
    
    # Colored histogram ########################################################
    if cmapname is None and coloredhisto is True:
        cmapname = dataset.info.cmapname

    if coloredhisto:
        # Normalizing from 0 to 1 for cmap display
        bin_centers = 0.5 * (bins[:-1] + bins[1:])
        color = bin_centers - min(bin_centers)
        color /= max(color)

        # Setting individual patch color
        for clr, patch in zip(color, patches):
            patch.set_facecolor(cmap(clr))
            patch.set_edgecolor('None')

    #  Colorbar display ########################################################
    if  cmapname is None and cmapdisplay is True:
        cmapname = dataset.info.cmapname

    if cmapdisplay:
        # Creating a Mappable for colorbar
        ## As the histogram is not a 'Mappable', we have to use ScalarMappable
        ## to build the colorbar
        norm = mpl.colors.Normalize(vmin=zmin, vmax=zmax)
        #sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm._A = []

        # Colorbar creation
        #cb = plt.colorbar(sm, orientation='horizontal', pad=0.05)
        #cb.ax.xaxis.set_ticks_position('top')  # ticks on top
        #cb.ax.xaxis.set_tick_params(direction='out')  # ticks outside

        #see cax after
        cb = fig.colorbar(sm, ax=ax, orientation='horizontal', pad=0.075)
        cb.ax.xaxis.set_ticks_position('top')  # ticks on top
        cb.ax.xaxis.set_tick_params(direction='out')  # ticks outside

        ### Seems ok now
        # Histogram ticks in relative axes coordinates (0, 1)
        ## Colorbar ticks position need to be in axes oordinates (0, 1).
        ## Histogram ticks (zmin, zmax) are converted using mpl.transforms
        ## (work with log scale). An additional dummy y-coordinate is added
        ## to work with mpl.transforms.
        #hist_ticks_data = np.vstack((hst.get_xticks(), np.zeros_like(hst.get_xticks()))).T  # (x,0)-like data coordinates
        #hist_ticks_data = np.vstack((ax.get_xticks(), np.zeros_like(ax.get_xticks()))).T  # (x,0)-like data coordinates
        #hist_ticks = cb.ax.transAxes.inverted().transform(cb.ax.transData.transform(hist_ticks_data))[:,0]  # color bar axes coordinates

        # Colorbar ticks same as histogram ticks
        #tick_locator = mpl.ticker.FixedLocator(hist_ticks)
        #cb.locator = tick_locator
        cb.update_ticks()
        cb.ax.xaxis.set_ticklabels([])  # no ticks label displayed
        colorbar = cb

    fig.tight_layout()

    # Curve display
#    plt.xlim(bins.min(), bins.max())
    ax.set_xlim(bins.min(), bins.max())

    # Saving figure to file
    if filename is not None:
##       plt.savefig(filename, dpi=dpi, transparent=transparent)
##        plt.savefig(filename, dpi=dpi, transparent=transparent, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.savefig(filename, dpi=dpi, transparent=transparent, edgecolor='none')
       
    return fig, colorbar


def getlimits(self, valfilt=False):
    ''' Get limits values of histogram.'''

    if valfilt or self.data.z_image is None:
        Z = self.data.values.T[2]
    else:
        Z = self.data.z_image

    return np.nanmin(Z.flatten()), np.nanmax(Z.flatten())

##
##def getlimits(self):
##    '''getting limits values of histogram.'''
##    Z = self.data.z_image
##    array = np.reshape(np.array(Z), (1, -1))
##
##    return np.nanmin(array), np.nanmax(array)
