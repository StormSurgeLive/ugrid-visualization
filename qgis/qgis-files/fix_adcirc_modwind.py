"""Join in a single file ADCIRC unstructured grid files zeta (fort.63.nc) and
uv (fort.64.nc) and make it compatible with CF/UGRID Conventions. With this
the output file can be read by THREDDS and ncWMS2/Godiva3.

Author: Marcelo Andrioni (https://github.com/marceloandrioni)
"""

import sys
import argparse
from pathlib import Path
import datetime
import numpy as np
import pandas as pd
import xarray as xr


def _file_exists(file, parser):

    file = Path(file)
    if file.exists():
        return file
    else:
        parser.error(f'File {file} does not exist.')


def _str2datetime(time, parser):

    try:
        return datetime.datetime.strptime(time, '%Y%m%d')
    except:
        parser.error(f"Could not convert '{time}' using format 'yyyymmdd'.")


def main():

    parser = argparse.ArgumentParser(
        description='ADCIRC netcdf output to CF/UGRID Conventions.')

    parser.add_argument('infile_zeta', type=lambda x: _file_exists(x, parser),
                        help='input nc file with zeta')
    parser.add_argument('infile_windxy', type=lambda x: _file_exists(x, parser),
                        help='input nc file with x and y components of wind velocity')
#    parser.add_argument('time0', type=lambda x: _str2datetime(x, parser),
#                        help=('date in yyymmdd format that represents time=0 '
#                              'for the run'))
    parser.add_argument('outfile', type=lambda x: Path(x),
                        help='output nc file following CF/UGRID Conventions')

    args = parser.parse_args()

    print(f'Infiles:\n{args.infile_zeta}\n{args.infile_windxy}')
    print(f'Outfile: {args.outfile}')

    # open zeta and windxy as one file dropping non essential variables
    ds = xr.open_mfdataset(
        [args.infile_zeta, args.infile_windxy],
        drop_variables=['nvdll', 'nbdv', 'nvell', 'ibtype', 'nbvv'],
        combine='by_coords')

    ds = ds.rename({'x': 'adcirc_mesh_x',
                    'y': 'adcirc_mesh_y',
                    'depth': 'bathymetry',
                    'zeta': 'ssh',
                    'windx': 'u',
                    'windy': 'v'})

    # -------------------------------------------------------------------------
    # coord vars

    # fix time reference
#    ds['time'] = pd.to_timedelta(ds['time'].values / 3600, unit='h') + args.time0
#    ds['time'].attrs = {'long_name': 'time', 'standard_name': 'time'}
#    ds['time'].attrs = {'calendar': 'proleptic_gregorian'}
    ds['time'].encoding = {'dtype': 'f8',
                           'units': 'seconds since 2020-07-22 00:00:00',
                           'calendar': 'proleptic_gregorian',
                           '_FillValue': None}

    ds['adcirc_mesh_y'].attrs = {'long_name': 'latitude',
                            'standard_name': 'latitude',
                            'units': 'degrees_north'}

    ds['adcirc_mesh_x'].attrs = {'long_name': 'longitude',
                             'standard_name': 'longitude',
                             'units': 'degrees_east'}

    for var in ['adcirc_mesh_y', 'adcirc_mesh_x']:
        ds[var].encoding = {'dtype': 'f4', '_FillValue': None}

    # -------------------------------------------------------------------------
    # data vars

    ds['bathymetry'].attrs = {'long_name': 'bathymetry',
                              'standard_name': 'sea_floor_depth',
                              'units': 'm'}

    ds['ssh'].attrs= {'long_name': 'sea surface height',
                      'standard_name': 'sea_surface_height_above_geoid',
                      'units': 'm'}

    del ds['u'].attrs['positive']
    del ds['v'].attrs['positive']

    ds['u'].attrs = {'long_name': 'u component of wind velocity',
                     'standard_name': 'eastward_wind',
                     'units': 'm s-1'}

    ds['v'].attrs = {'long_name': 'v component of wind velocity',
                     'standard_name': 'northward_wind',
                     'units': 'm s-1'}

    for var in ['bathymetry', 'ssh', 'u', 'v']:

        ds[var].attrs['location'] = 'node'
        ds[var].attrs['mesh'] = 'adcirc_mesh'

        # chunking for faster access
        nnodes = ds['node'].size
        chunksize = [1, nnodes] if 'time' in list(ds[var].coords) else nnodes

        ds[var].encoding = {'dtype': 'f4',
                            '_FillValue': np.nan,
                            # 'zlib': True,
                            # 'complevel': 1,
                            'chunksize': chunksize}

    # set some attributes to follow CF convetions for unstructured grids
    # https://github.com/ugrid-conventions/ugrid-conventions
    ds['adcirc_mesh'].attrs['node_coordinates'] = 'adcirc_mesh_x adcirc_mesh_y'
    ds['adcirc_mesh'].attrs['cf_role'] = 'mesh_topology'
#    ds['mesh_topology'].attrs['topology_dimension'] = \
#        ds['mesh_topology'].attrs['dimension']

    # -------------------------------------------------------------------------
    # global attributes

    ds.attrs = {'title': 'ADCIRC',
                'institution': 'My Institution',
                'source': 'ADCIRC - ADvanced CIRCulation Model',
#                'history': '{}: {}'.format(
#                    datetime.datetime.utcnow().strftime('%FT%TZ'),
#                    Path(sys.argv[0]).name),
                'references': 'http://www.myinstitution.com/',
                'Conventions': 'CF-1.7, UGRID-1.0'}
#                '_CoordinateModelRunDate': args.time0.strftime('%FT%TZ')}

    ds.encoding['unlimited_dims'] = 'time'

    # -------------------------------------------------------------------------
    # output file

    # reorder
    ds = ds[['time', 'adcirc_mesh_y', 'adcirc_mesh_x', 'element', 'adcirc_mesh',
            'bathymetry', 'ssh', 'u', 'v']]

    for var in list(ds.data_vars):
        print(f'Loading {var}')
        ds[var].load()

    print(f'Writing {args.outfile}')
    ds.to_netcdf(args.outfile, mode='w', format='NETCDF4')


if __name__ == "__main__":

    main()
