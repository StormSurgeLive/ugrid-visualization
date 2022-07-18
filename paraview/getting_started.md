# Getting Started with ParaView for Visualizing ADCIRC NetCDF Output

## Background
 
ADCIRC's netCDF output files aren't directly readable by ParaView, since ParaView doesn't have a reader for netCDF files that use UGRID metadata. However, you can read an ADCIRC netCDF file if you generate an accompanying XDMF[^1] file for it. XDMF files describe the metadata and structure of a netCDF file in a small XML file that ParaView can interpret.

This document will show you how to build and use a utility for generating XDMF files from ADCIRC output, which is a necessary first step before visualizing ADCIRC output with ParaView. Also, the last section will give instructions for downloading the version of ParaView needed for the tutorials in this directory.

You'll need to use a Linux command line for the ParaView tutorials, so any instructions for running commands in this document will assume you're in a Linux environment. If you're using a Windows machine, you can use Windows Subsystem for Linux (WSL).[^2] The ParaView scripts used in the tutorials were developed and tested in Ubuntu Linux version 20.04.

## Building the `generateXDMF.x` utility

Before you can build the XDMF generation utility, you may need to install some packages that the build process depends on. On Ubuntu Linux, these are:
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
You should now have the executable `generateXDMF.x` in `asgs/output`.

## Using the `generateXDMF.x` utility

For the ParaView tutorials, you'll need to generate XDMF files for a sample maxele.63 and fort.63. Suppose you're in a directory that contains the files `maxele.63.nc` and `fort.63.nc`, and you've copied the `generateXDMF.x` executable to this directory as well. Then, run the following commands:
```
$ ./generateXDMF.x --datafile maxele.63.nc
$ ./generateXDMF.x --datafile fort.63.nc
```
You should now have the files `maxele.63.nc.xmf` and `fort.63.nc.xmf` in the same directory.

## Downloading ParaView for Linux with no GUI support

The ParaView version you'll need for the tutorials in this directory is intended for command-line use only, and doesn't include a GUI. This is known as running ParaView in "headless" mode.

The ParaView automation scripts used for the tutorials were developed for ParaView version 5.9.1, so it's recommended that you download this version as well. You may get the same results with later versions, but this isn't guaranteed since ParaView Python scripts aren't always compatible across ParaView versions.

You can run the following command to download ParaView 5.9.1 for Linux through the command line:
```
wget -O ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit.tar.gz "https://www.paraview.org/paraview-downloads/download.php?submit=Download&version=v5.9&type=binary&os=Linux&downloadFile=ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit.tar.gz"
```
If you'd prefer to download through a browser, you can find the download links at the following page:
```
https://www.paraview.org/download/?version=v5.9&filter=Linux
```
Make sure to choose the file named `ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit.tar.gz`.

Once you've downloaded the ParaView `.tar.gz` and extracted the contents, you're ready to move on to the ParaView tutorials for visualizing ADCIRC netCDF files.


[^1]: For background reading see: https://www.xdmf.org/index.php/Main_Page
[^2]: For setting up a Linux command line on Windows using WSL see: https://docs.microsoft.com/en-us/windows/wsl/setup/environment
