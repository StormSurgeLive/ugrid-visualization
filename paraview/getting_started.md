# Getting Started with ParaView for Visualizing ADCIRC NetCDF Output

## Background
 
ADCIRC's netCDF output files aren't directly readable by ParaView, since ParaView doesn't have a reader for netCDF files that use UGRID metadata. However, you can read an ADCIRC netCDF file if you generate an accompanying XDMF[^1] file for it. XDMF files describe the metadata and structure of a netCDF file in a small XML file that ParaView can interpret.

This document will show you how to build and use a utility for generating XDMF files from ADCIRC output, which is a necessary step before visualizing ADCIRC output with ParaView. Also, the last section will give instructions for downloading the version of ParaView needed for the tutorials in this directory.

You'll need to use a Linux command line for the ParaView tutorials, so any instructions for running commands in this document will assume you're in a Linux environment. If you're using a Windows machine, you can use Windows Subsystem for Linux (WSL).[^2] The ParaView scripts used in the tutorials were developed and tested in Ubuntu Linux version 20.04.

## Building the `generateXDMF.x` utility

Before you can build the XDMF generation utility, you'llto install some packages that it depends on. On Ubuntu Linux, these are:
```
$ sudo apt install make
$ sudo apt install gfortran
$ sudo apt install libnetcdff-dev
```
The utility for generating XDMF files from ADCIRC output is included in the ASGS repository (https://github.com/StormSurgeLive/asgs). You can download this repository using `git clone`:
```
$ git clone https://github.com/StormSurgeLive/asgs.git
```
Once you've downloaded the repository, move into the `asgs/output` directory. Run the following command to build the XDMF generation utility (this also builds other `asgs` utilities, although these won't be used for the ParaView tutorials):
```
$ make all compiler=gfortran NETCDF=enable NETCDF4=enable NETCDF4_COMPRESSION=enable
```



[^1]: For background reading see: https://www.xdmf.org/index.php/Main_Page
[^2]: For setting up a Linux command line on Windows using WSL see: https://docs.microsoft.com/en-us/windows/wsl/setup/environment
