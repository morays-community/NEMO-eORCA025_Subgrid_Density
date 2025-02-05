# modules

# utils
import os
import sys
import re
import argparse
import random

import numpy as np
import netCDF4 as nc
import cmocean

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as colors

to_plot = dict()
infos = dict()
# ============================================================
#                         Plots Infos
# ============================================================
infos[ 'sosstsst' ] = [ 'SST (degC)', cmocean.cm.thermal , colors.Normalize(vmin=-2, vmax=35), lambda x: x ]
infos[ 'sosaline' ] = [ 'Salinity (psu)' , cmocean.cm.haline , colors.Normalize(vmin=28, vmax=38), lambda x: x ]
infos[ 'sossheig' ] = [ 'SSH (m)' , cmocean.cm.deep , colors.Normalize(vmin=-2, vmax=2), lambda x: x ]
infos[ 'soextrho' ] = [ '-\u0394\u03c1 (kg/m³)' , cmocean.cm.ice_r , colors.LogNorm(vmin=0.000005, vmax=0.05), lambda x: abs(x) ]
infos[ 'vozocrtx' ] = [ 'u (m/s)' , cmocean.cm.diff , colors.Normalize(vmin=-1.0, vmax=1.0), lambda x: x ]
infos[ 'vomecrty' ] = [ 'v (m/s)' , cmocean.cm.diff , colors.Normalize(vmin=-0.5, vmax=0.5), lambda x: x ]
infos[ 'vovecrtz' ] = [ 'w (m/s)' , cmocean.cm.diff , colors.Normalize(vmin=-0.0000005, vmax=0.0000005), lambda x: x]
infos[ 'sohefldo' ] = [ 'Heat Flux (W/m2)' , cmocean.cm.balance , colors.Normalize(vmin=-150., vmax=150.), lambda x: x ]
infos[ 'sosfldow' ] = [ 'Salt Flux (g/m2/s)' , cmocean.cm.amp , colors.Normalize(vmin=0.0, vmax=0.002), lambda x: x ]
infos[ 'sowaflup' ] = [ 'Fresh Water Flux (kg/m2/s)' , cmocean.cm.tarn , colors.Normalize(vmin=-0.001, vmax=0.001), lambda x: x ]
infos[ 'voeke' ] = [ 'EKE (cm2/s2)' , cmocean.cm.amp , colors.LogNorm(vmin=1., vmax=5000.), lambda x: x*1000. ]
infos[ 'vomke' ] = [ 'MKE (cm2/s2)' , cmocean.cm.amp , colors.LogNorm(vmin=1., vmax=5000.), lambda x: x*1000. ]
infos[ 'votke' ] = [ 'TKE (cm2/s2)' , cmocean.cm.amp , colors.LogNorm(vmin=1., vmax=5000.), lambda x: x*1000. ]
infos[ 'vomevt' ] = [ 'T.v (degC.m/s)' , cmocean.cm.balance , colors.Normalize(vmin=-18.0, vmax=18.0), lambda x: x ]
infos[ 'vomevs' ] = [ 'S.v (psu.m/s)' , cmocean.cm.delta , colors.Normalize(vmin=-18.0, vmax=18.0), lambda x: x ]
infos[ 'vozout' ] = [ 'T.u (degC.m/s)' , cmocean.cm.balance , colors.Normalize(vmin=-35.0, vmax=35.0), lambda x: x ]
infos[ 'vozous' ] = [ 'S.u (degC.m/s)' , cmocean.cm.delta , colors.Normalize(vmin=-35.0, vmax=35.0), lambda x: x ]
infos[ 'votemper' ] = [ 'Temperature (degC)' , cmocean.cm.thermal , colors.Normalize(vmin=-2, vmax=35), lambda x: x ]
infos[ 'vosaline' ] = [ 'Salinity (psu)' , cmocean.cm.haline , colors.Normalize(vmin=28, vmax=38), lambda x: x ]
infos[ 'voextrho' ] = [ '-\u0394\u03c1 (kg/m³)' , cmocean.cm.ice_r , colors.LogNorm(vmin=0.000005, vmax=0.05), lambda x: abs(x) ]
# ============================================================
#                       2D Fields to plot
# ============================================================
to_plot[ 'gridTsurf' ] = ['soextrho','sosstsst','sosaline','sossheig'] # sst, sss, drho
to_plot[ 'gridUsurf' ] = ['vozocrtx']                       # u-current
to_plot[ 'gridVsurf' ] = ['vomecrty']                       # v-current
to_plot[ 'flxT' ] = ['sohefldo','sosfldow','sowaflup']      # heat, salt, water fluxes
# ============================================================
#                       3D Fields to plot
# ============================================================
#to_plot[ 'gridT' ] = ['votemper','vosaline','voextrho']     # T, S, drho
#to_plot[ 'gridU' ] = ['vozocrtx']                           # u-current
#to_plot[ 'gridV' ] = ['vomecrty']                           # v-current
#to_plot[ 'gridW' ] = ['vovecrtz']                           # w-current
#to_plot[ 'EKE' ] = ['voeke','vomke','votke']                # eke, mke, tke
#to_plot[ 'VT' ]  = ['vomevt','vomevs','vozout','vozous']    # vt, vs, ut, us
# ============================================================


def main(respath,plotpath,confcase,freq,year,month,day):
    global to_plot
    global infos

    # go in year dir
    print(f'\n====== {freq} ======')
    os.chdir(respath)
    if year is None:
        years = os.listdir(os.getcwd())
        year = random.choice(years)
    year_path = respath + '/' + year
    os.chdir(year_path)

    # get month and day
    if month is None:
        month = random.randint(1,12)
    if day is None:
        day = random.randint(1,31)

    month = "{:02d}".format(int(month))
    day = "{:02d}".format(int(day))
    print(f'\n--> Snapshot of y{year} m{month} d{day}')

    # get files
    file_base = year_path + '/' + confcase + '_y' + str(year) + 'm' + str(month) + 'd' + str(day) + '.' + str(freq)
    for file in to_plot.keys():
        grid_file = file_base + '_' + file + '.nc'

        # get mesh and data if file exists
        if os.path.isfile(grid_file):
            ds=nc.Dataset(grid_file)
            lon = ds.variables['nav_lon']
            lat = ds.variables['nav_lat']
            try:
                dpt = ds.variables['deptht']
            except Exception as e0:
                try:
                    dpt = ds.variables['depthu']
                except Exception as e1:
                    try:
                        dpt = ds.variables['depthv']
                    except Exception as e2:
                        try:
                            dpt = ds.variables['depthw']
                        except Exception as e3:
                            dpt = None

            # loop on fields
            for fld in to_plot[file]:
                print(f'Plotting {fld}')
                data = ds.variables[fld][-1].data
                # check data
                if data is None:
                    data = np.zeros(lon.shape())
                if dpt is not None:
                    print(f'Depth not handled for 3D fields yet, plotting only surface')
                    data = data[0,:,:]
                        
                # plot
                output = plotpath + '/' + confcase + '_y' + year + 'm' + month + 'd' + day + '.' + freq + '_' + file + '_' + fld  + '.png'
                make_plot(data,lon,lat,infos[fld],output)
        else:
            print(f'File {grid_file} not found, ignored')


def make_plot(data,lon,lat,infos,output):
    # args
    title, cmap, norm, tfs = infos
    data = tfs(data)
    # figure
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.EqualEarth())
    ax.add_feature(cfeature.LAND, zorder=100, edgecolor='k')
    # colo map
    pcm = ax.pcolormesh(lon, lat, data, cmap=cmap, norm=norm, transform=ccrs.PlateCarree())
    cbar = plt.colorbar(pcm, ax=ax, orientation='vertical', pad=0.05, shrink=0.5)
    plt.title(title)
    # write fig
    plt.savefig(output, bbox_inches='tight')
    plt.close()


if __name__=="__main__":

    # args
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='confcase', type=str, default='noconf')
    parser.add_argument('-l', dest='loc', type=str, default='DDIR')
    parser.add_argument('-f', dest='freq', type=str, default='1d')
    parser.add_argument('-y', dest='year', type=str, default=None)
    parser.add_argument('-m', dest='month', type=str, default=None)
    parser.add_argument('-d', dest='day', type=str, default=None)
    args = parser.parse_args()
    confcase = args.confcase
    freq = args.freq
    year = args.year
    month = args.month
    day = args.day
    dir = args.loc

    # guess CONFCASE if not given
    if confcase == 'noconf':
        cur_dir = os.getcwd()
        cur_dir = cur_dir.split(os.path.sep)
        
        if cur_dir[-1] != 'CDF' and cur_dir[-2] != 'CTL':
            # we are not in CDF/CTL dir and confcase not given, impossible to guess
            print('ERROR: must be executed in the CONFCASE CTL directory')
            raise SystemExit
        else:
            confcase = cur_dir[-3]

    # get work dir
    if dir in os.environ:
        DDIR = os.environ[dir]
    else:
        print('ERROR: Environment variable ${dir} not defined')
        sys.exit()

    # get storage dir
    if 'SDIR' in os.environ:
        SDIR = os.environ['SDIR']
    else:
        print('ERROR: Environment variable $SDIR not defined')
        sys.exit()

    # path to -S
    print(f'Storage dir: {SDIR}')
    print(f'CONFCASE : {confcase}')
    conf, case = confcase.split('-')
    respath = SDIR + '/' + conf + '/' + confcase + '-S/' + freq
    if not os.path.exists(respath) and not os.path.isdir(respath):
        print(f'ERROR: {respath} does not exist')
        sys.exit()

    # path to PLOTS
    plotpath = SDIR + '/' + conf + '/' + confcase + '-PLOTS/snapshots'
    print(f'Plot dir: {plotpath}')
    if not os.path.exists(plotpath):
        os.makedirs(plotpath)

    # proceed
    main(respath,plotpath,confcase,freq,year,month,day)
