import os
import argparse
import numpy as np
import xarray as xr
import cmocean

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors
import matplotlib
matplotlib.use('Agg')

def make_plot(data,lon,lat,infos,output):
    # args
    title, cmap, norm, tfs = infos
    data = tfs(data)
    # figure
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.EqualEarth())
    ax.add_feature(cfeature.LAND, zorder=100, edgecolor='k')
    # color map
    pcm = ax.pcolormesh(lon, lat, data, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(pcm, ax=ax, orientation='vertical', pad=0.05, shrink=0.5)
    plt.title(title)
    # write fig
    plt.savefig(output, bbox_inches='tight')
    plt.close()


def main(filepath_ref, filepath, var_name, fig_name, infos, freq):

    # read files
    try:
        ds = xr.open_dataset(filepath)
        ds_ref = xr.open_dataset(filepath_ref)
    except:
        return

    # coordinates
    lon = ds.nav_lon.values
    lat = ds.nav_lat.values

    # get fields
    var_ref = getattr(ds_ref,var_name).values[-1]
    var = getattr(ds,var_name).values[-1]
    diff_var = var - var_ref

    # plot
    plotpath = fig_name + '_diff_' + config +'_' + freq + '.png'
    make_plot(diff_var,lon,lat,infos,plotpath)



if __name__=="__main__":

    # Config name
    # -----------
    try:
        namelist = nml.read('namelist_cfg')
        config = namelist['namrun']['cn_exp']
    except:
        config = 'eORCA025.L75_subgridDensity.S22'


    # BSF difference
    infos = [ 'Barotropic Stream Function : eORCA025.L75.S22 - eORCA025.L75 (m3/s)' , cmocean.cm.balance , colors.Normalize(vmin=-2.e7, vmax=2.e7), lambda x: x ]
    main( filepath_ref='eORCA025.L75-GB.INF-MEAN/5d/1966-1970/eORCA025.L75-GB.INF_y1966-1970.5d_PSI.nc' , filepath='eORCA025.L75-SubgridDensity.S22-MEAN/5d/1966-1970/eORCA025.L75-SubgridDensity.S22_y1966-1970.5d_PSI.nc' , var_name='sobarstf', fig_name='BSF', infos=infos , freq='5d' )

    # SST difference
    infos = [ 'SST : eORCA025.L75.S22 - eORCA025.L75 (ºC)' , cmocean.cm.balance , colors.Normalize(vmin=-1.5, vmax=1.5), lambda x: x ]
    main( filepath_ref='eORCA025.L75-GB.INF-MEAN/1d/1966-1970/eORCA025.L75-GB.INF_y1966-1970.1d_gridTsurf.nc' , filepath='eORCA025.L75-SubgridDensity.S22-MEAN/1d/1966-1970/eORCA025.L75-SubgridDensity.S22_y1966-1970.1d_gridTsurf.nc' , var_name='sosstsst', fig_name='SST', infos=infos , freq='1d' )


    # SSH difference
    infos = [ 'SSH : eORCA025.L75.S22 - eORCA025.L75 (m)' , cmocean.cm.balance , colors.Normalize(vmin=-0.3, vmax=0.3), lambda x: x ]
    main( filepath_ref='eORCA025.L75-GB.INF-MEAN/1d/1966-1970/eORCA025.L75-GB.INF_y1966-1970.1d_gridTsurf.nc' , filepath='eORCA025.L75-SubgridDensity.S22-MEAN/1d/1966-1970/eORCA025.L75-SubgridDensity.S22_y1966-1970.1d_gridTsurf.nc' , var_name='sossheig', fig_name='SSH', infos=infos , freq='1d' )

    # Non-Solar Heat Flux difference
    infos = [ 'Net Heat Flux : eORCA025.L75.S22 - eORCA025.L75 (W/m2)' , cmocean.cm.balance , colors.Normalize(vmin=-50.0, vmax=50.0), lambda x: x ]
    main( filepath_ref='eORCA025.L75-GB.INF-MEAN/1d/1966-1970/eORCA025.L75-GB.INF_y1966-1970.1d_flxT.nc' , filepath='eORCA025.L75-SubgridDensity.S22-MEAN/1d/1966-1970/eORCA025.L75-SubgridDensity.S22_y1966-1970.1d_flxT.nc' , var_name='sohefldo', fig_name='QT', infos=infos , freq='1d' )
