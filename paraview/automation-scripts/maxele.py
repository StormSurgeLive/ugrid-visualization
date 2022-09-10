#!/usr/bin/env python3
#----------------------------------------------------------------
# maxele.py: Prototype script to extract key parameters from
# ADCIRC netCDF4 maxele.63.nc files, send request to web service
# and receive a matching maxele.63.nc.xmf file in response.
#----------------------------------------------------------------
# Copyright(C) 2022 Jason Fleming
#
# This file is part of the ADCIRC Surge Guidance System (ASGS).
#
# The ASGS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ASGS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with the ASGS.  If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------
# prerequisite : 'pip3 install netCDF4'
# prerequisite : 'pip3 install requests' # already satisfied on Ubuntu 20.04 ...
#----------------------------------------------------------------
import sys
from os import path
import netCDF4 as nc
import requests
#
fn = '/home/jason/scratch/asgs2579977/2022062206/nowcast/maxele.63.nc'
ds = nc.Dataset(fn)
print(len(ds.dimensions['node']))
print(len(ds.dimensions['nele']))
print(getattr(ds, 'agrid'))
print( "{ \"node\" : ",len(ds.dimensions['node']),", \"nele\" : ", len(ds.dimensions['nele']),", \"agrid\" : \"",getattr(ds, 'agrid'),"\" }" )
r = requests.post('https://stormsurge.live/post', data={'node': len(ds.dimensions['node']), 'nele' : len(ds.dimensions['nele']), 'agrid' :  getattr(ds, 'agrid') })
print(r.text)