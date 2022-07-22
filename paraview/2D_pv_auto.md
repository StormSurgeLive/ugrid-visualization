# Automated Visualization of ADCIRC Output with ParaView: 2D View

## Background

The goal of this tutorial is to generate the following figures from an ADCIRC maxele.63 and fort.63 file in an automated way using ParaView:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/tutorial-figures/latx_2D_maxele_img.png)
![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/tutorial-figures/latx_2D_fort63_anim.gif)

## Software requirements

For this tutorial, you'll need to be working in a Linux environment. All commands shown here have been tested on the Ubuntu Linux 20.04 command line (running from Windows Subsystem for Linux), but any Linux distribution that has access to the APT package manager should work.

If this is your first time using ParaView to visualize ADCIRC output, make sure to follow along with the [Getting Started with ParaView for Visualizing ADCIRC NetCDF Output](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/getting_started.md) tutorial in this directory. The Getting Started tutorial will also show you which version of ParaView you need to install, which is different to the standard ParaView desktop application.

Once you're caught up with the Getting Started steps, you'll need to install these additional packages if you don't already have them:
```
$ sudo apt install nco
$ sudo apt install ffmpeg
```
You may need to run `sudo apt update && sudo apt upgrade` beforehand if any packages can't be found.

You'll also need files from the `ugrid-visualization/paraview/automation-scripts` and `ugrid-visualization/paraview/color-maps` directories, so you can either clone this repository or download the files manually. The specific files you'll need are:
* Both color maps in the `color-maps` directory ([`RdYlBu_Brewer.xml`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/color-maps/RdYlBu_Brewer.xml) and [`blueBrownGreenBathyTopoColorMap.xml`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/color-maps/blueBrownGreenBathyTopoColorMap.xml))
* [`pvadcirc_auto.sh`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/automation-scripts/pvadcirc_auto.sh), [`latx_2D_maxele.py`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/automation-scripts/latx_2D_maxele.py), and [`latx_2D_fort63.py`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/automation-scripts/latx_2D_fort63.py) from the `automation-scripts` directory.

## Downloading sample ADCIRC output data and generating XDMF files

The first step is to download some sample maxele.63 and fort.63 files. The figures shown in the [Background](#Background) section were generated from output for the storm surge due to Hurricane Laura (2020). You can download this output with the following commands:
```
$ wget https://fortytwo.cct.lsu.edu/thredds/fileServer/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/maxele.63.nc
$ ncks -7 -h -L 5 -d time,0,9 -d time,10,19 'http://fortytwo.cct.lsu.edu/thredds/dodsC/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/fort.63.nc' -o fort.63.nc
```
The file sizes are ~129 MB for the maxele.63 and ~387 MB for the fort.63. For more context on downloading ADCIRC netCDF files, you can refer to the [Downloading ADCIRC NetCDF Output Files from a THREDDS Server](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/ugrid-cf-resources/downloading_netcdf.md) tutorial.

Now, use the `generateXDMF.x` utility to generate the additional XDMF files that ParaView will need to read the ADCIRC netCDF output (if this step is new to you, see the [Getting Started](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/getting_started.md) tutorial):
```
$ ./generateXDMF.x --datafile maxele.63.nc
$ ./generateXDMF.x --datafile fort.63.nc
```
These commands assume that you've copied the `generateXDMF.x` executable to same directory where you downloaded the `maxele.63.nc` and `fort.63.nc` files.

**Make sure that your netCDF files and XDMF files are all in the same directory**; otherwise, ParaView won't be able to read the netCDF files.

## Understanding the automation scripts

`pvadcirc_auto.sh` is a Bash script that implements automation for running `latx_2D_maxele.py` and `latx_2D_fort63.py`. The bash script uses `pvpython` (ParaView's own Python interpreter) to run these Python scripts, which then run the visualization tasks needed to generate the figures. `latx_2D_maxele.py` generates a single PNG figure from the maxele.63 file, and `latx_2D_fort63.py` generates animation frames from the fort.63 file which are then converted to a GIF.

The Bash script has several parameters that you can customize to control the automation. Some of these parameters are paths; make sure to set all path parameters **without a trailing slash** to avoid any errors. For best results, all paths should be **absolute paths**. The following bullet points detail the different parameters:
* `IN_DIR`: The absolute path to the directory where your ADCIRC netCDF files and XDMF files are located. The automation scripts can only handle maxele.63 and fort.63 files, which they recognize by matching the exact names `maxele.63.nc` and `fort.63.nc`. Therefore, this directory should have at most one maxele.63 file and one fort.63 file, each with their corresponding XDMF file. If your files are named something different to `maxele.63.nc` and `fort.63.nc`, they won't be recognized.
* `OUT_DIR`: The absolute path to the directory where you want to save the figures generated by ParaView.
* `CMAP_DIR`: The absolute path to the directory that contains the 2 color map files from the `ugrid-visualization/paraview/color-maps` directory (`RdYlBu_Brewer.xml` and `blueBrownGreenBathyTopoColorMap.xml`). 
* `PV_DIR`: The absolute path to the directory where you installed ParaView, **including the name of the installation directory itself**.
* `SCRPT_DIR`: The absolute path to the directory where the automation scripts (`pvadcirc_auto.sh`, `latx_2D_maxele.py`, and `latx_2D_fort63.py`) are located.
* `ZOOM_AREA`: This parameter won't be used for this tutorial, since it's only needed when using a 3D view.
* `ZETA_BND`: An integer that defines the upper bound for the water surface elevation color map, in meters.
* `START_T` and `FINAL_T`: Integers that define the index of the first and last timesteps that you want to include in the fort.63 animation.
* `C_EMAIL`: A contact email address that will be displayed in an annotation on the figures.
* `FILE_CLEAN`: A Boolean paramater that toggles file cleanup on or off. Some temporary files are generated that aren't needed once the figures have been saved, so this parameter allows you to delete them (leaving only the PNG and GIF figures as output). If you want to keep these files, set this parameter to `false` (for example, if you want to keep the individual frames of the fort.63 animation as PNG files).

## Setting the `pvadcirc_auto.sh` parameters

To facilitate automation, all of the parameters can be set from environment variables. Almost all parameters have a default value as a backup if you haven't set the corresponding environment variable. These are the default values:

* `IN_DIR`, `OUT_DIR`, `CMAP_DIR`, and `SCRPT_DIR`: The default value for all of these parameters is the current working directory where you're running the Bash script.
* `ZOOM_AREA`: This has an empty default value, which is what you'll use in this tutorial.
* `ZETA_BND`: Default value is 5 (meters). This value is intended for strong hurricanes, so you may have to set the parameter to a lower value.
* `START_T` and `END_T`: Default values are 0 and 9. Since the GIF is generated at 10fps, this means that by default, you'll generate a 1-second GIF from the first 10 timesteps of your fort.63 file.
* `C_EMAIL`: Default value is a placeholder email address, "placeholder@email.com"
* `FILE_CLEAN`: Default value is `true`, which means any temporary files are deleted once the figures have been saved.

The only exception is `PV_DIR`, which does not have a default value. It's required to set an environment variable for PV_DIR before running the Bash script; otherwise, the script will exit. 

## Running `pvadcirc_auto.sh`

Since `IN_DIR`, `OUT_DIR`, `CMAP_DIR`, and `SCRPT_DIR` all have a default value of the current working directory, the simplest way to run the Bash script is to move your ADCIRC netCDF files, XDMF files, color map files, and automation scripts all to the same directory, and then run the bash script from there.

Suppose you're in a directory that contains all of these files, and for simplicity, suppose you've also moved the `pvadcirc_auto.sh` to this directory as well. In this case, to reproduce the figures from the [Background](#Background) section, the only parameters you'll need to set before running the script are `PV_DIR` and `FINAL_T`, since the GIF was made from 20 timesteps rather than the default 10.

If you downloaded the recommended ParaView version in the [Getting Started](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/getting_started.md) tutorial, you'll have a directory named `ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit` that contains your ParaView installation. Suppose you've created this directory in your home Linux directory; then the value of `PV_DIR` could be something like `/home/$USER/ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit`. Then, the commands to run the Bash script could be:
```
$ export PV_DIR="/home/$USER/ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit" && export FINAL_T=19
$ bash pvadcirc_auto.sh
```
You should now have the files `latx_2D_maxele_img.png` and `latx_2D_fort63_anim.gif` in the same directory where you ran the script. You can also find sample versions of these files in the `ugrid-visualization/paraview/figures` directory.

A more customized run where the files are spread out across different directories might look something like this:
```
$ export IN_DIR="/home/$USER/adcirc-output" && export OUT_DIR="/home/$USER/figures" && export CMAP_DIR="/home/$USER/color-maps"
$ export SCRPT_DIR="/home/$USER/paraview-scripts" && export PV_DIR="/home/$USER/ParaView-5.9.1-osmesa-MPI-Linux-Python3.8-64bit"
$ export FINAL_T=19
$ bash pvadcirc_auto.sh
```

## A note on the annotation format

The annotation in the top left of the figures that lists some information about the netCDF file is designed for use with ADCIRC output from the ASGS[^1]. If your ADCIRC netCDF files aren't ASGS output, the annotation may not work as expected. The annotation expects your files to have the global netCDF attributes `agrid`, `title`, `rundes`, and `runid`. If the annotation is giving unexpected results, you should check to see if your file has these global attributes. For more information about netCDF attributes and how to modify them, see the [Viewing & Modifying CF/UGRID Metadata in an ADCIRC netCDF File](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/ugrid-cf-resources/ugrid_cf_metadata.md#Software-requirements) tutorial.


[^1]: https://github.com/StormSurgeLive/asgs
