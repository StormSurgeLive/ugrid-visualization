# Visualizing a Combined ADCIRC fort.63 and fort.74 File with QGIS

## Software requirements

Before starting this tutorial, see the [Loading ADCIRC netCDF Files with QGIS and Adding Basemaps](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md) document for QGIS installation instructions and how to load ADCIRC netCDF files into QGIS. Also, if you haven't used `conda` before, see the `README.md` in this directory for a link to the installation instructions.

The sample files for this tutorial are a fort.63 and a fort.74 from the storm surge and winds due to Hurricane Laura (2020). Since you'll be [downloading subsets of these files](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/ugrid-cf-resources/downloading_netcdf.md#using-ncks-to-download-a-subset-of-a-fort63-file), you'll need to [install the `nco` package](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/ugrid-cf-resources/downloading_netcdf.md#software-requirements) on a Unix shell.

Once you've installed `nco`, run the following commands to download the sample files:
```
$ ncks -7 -h -L 5 -d time,0,9 -d time,10,19 'http://fortytwo.cct.lsu.edu/thredds/dodsC/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/fort.63.nc' -o fort.63.nc
$ ncks -7 -h -L 5 -d time,0,9 -d time,10,19 'http://fortytwo.cct.lsu.edu/thredds/dodsC/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/fort.74.nc' -o fort.74.nc
```
For more information about these commands, refer to the [Downloading ADCIRC NetCDF Output Files from a THREDDS Server](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/ugrid-cf-resources/downloading_netcdf.md) tutorial. The file sizes are ~387 MB for the fort.63 and ~1.1 GB for the fort.74, so they will take a few seconds to download.

You will also need the files [`fix_adcirc_modwind.py`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/qgis-files/fix_adcirc_modwind.py), [`fort63_style_file.qml`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/qgis-files/fort63_style_file.qml), and [`color_bar_qgis.png`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/qgis-files/color_bar_qgis.png) from the `ugrid-visualization/qgis/qgis-files` directory.

## Generating a combined fort.63 and fort.74 file

As mentioned in [Loading ADCIRC netCDF Files with QGIS and Adding Basemaps](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md#loading-an-adcirc-netcdf-file), QGIS can struggle to load large timeseries ADCIRC output files. If you try to load either the `fort.63.nc` or `fort.74.nc` sample file into QGIS directly, it probably won't be able to load them and will eventually crash.

Also, the fort.74 file needs some modifications for QGIS to understand that the wind variables form a vector dataset. To make these modifications, you'll need to run the `fix_adcirc_modwind.py` script (modified version of a  script developed by Marcelo Andrioni, https://github.com/marceloandrioni), which also combines the variables from the fort.63 and fort.74 into a single netCDF file.

The recommended way to run `fix_adcirc_modwind.py` is to set up a conda environment that has script's dependencies installed:
```
$ conda create -n fix_adcirc_env -c conda-forge xarray dask netCDF4 bottleneck
$ conda activate fix_adcirc_env
```
Assuming you've moved the `fix_adcirc_modwing.py` to the same directory where you downloaded `fort.63.nc` and `fort.74.nc`, run the following command (in the `fix_adcirc_env` conda environment):
```
$ python fix_adcirc_modwind.py fort.63.nc fort.74.nc fort.63-74.nc
```

## Loading the `fort.63-74.nc` file

After [loading the combined `fort.63-74.nc` file](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md#loading-an-adcirc-netcdf-file) into QGIS, your Map canvas should look like this:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_02.png)

## Color mapping water surface elevation and showing wind vectors

The `fort63_style_file.qml` file will make it easy to set color mapping properties for the water surface elevation variable and display wind vectors. 

Right-click on the `adcirc_mesh` layer in the Layers panel and select "Properties...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_04.png)

This will take you to the Layer Properties menu. At the bottom left of this menu, there is a Style drop-down menu; open this menu and select "Load Style...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_05.png)

Then, browse for the `fort63_style_file.qml` file and apply it. After selecting "OK" in the Layer Properties menu, your Map canvas should look like this:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_13.png)

## Load the OpenStreetMap basemap

Next, [load the OpenStreetMap basemap layer](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md#loading-the-default-qgis-basemap) and move it below the `adcirc_mesh` layer in the Layers panel. Your Map canvas should now look like this:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_14.png)

## Add a color bar (and optionally other annotations)

In the View menu at the uppermost toolbar, select "Decorations" -> "Image...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_09.png)

Now, select the "Enable Image" checkbox and browse for `color_bar_qgis.png`, set the size to 75.00 mm, and select "OK". You should now see a color bar at the bottom left of the Map canvas.

You can also add other annotations to the visualization, such as a scale bar:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_10.png)

## Zooming in

The spacing of the wind vectors is customized for a more zoomed-in view, so you can now zoom in on the Map canvas to a more specific area of interest. For example, the following view shows the areas of the Louisiana and Texas coast around the location of Hurricane Laura's landfall:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_15.png)

You can modify the spacing of the wind vectors in [the Layer Styling Panel](https://docs.qgis.org/3.22/en/docs/user_manual/introduction/general_tools.html#layer-styling-panel) if you want to use a more zoomed-out view.

## Enabling time navigation

Currently, you can only see data for the first timestep in the fort.63 and fort.74 files. To see data for other timesteps, you need to enable the Temporal Controller Panel by clicking on its icon:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_16.png)

Once you've enabled this panel, you should see it appear above the Map canvas. Initially, time navigation will be disabled in the panel, so you need to click on the third icon ("Animated temporal navigation"):

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_17.png)

Now, you should see a slider in the Temporal Controller Panel which you can use to navigate through the different timesteps:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_18.png)

## Saving frames for an animation

You can also use the Temporal Contoller Panel to save frames which you can use to generate an animation. Click on the save icon at the bottom right of the panel to open the Export Map Animation menu:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_19.png)

This will only save the frames, so you'll need to generate the animation outside of QGIS. For example, here is a GIF made from animation frames exported from QGIS:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_figure_2.gif)

## Visualizing other fort.63 and fort.74 files

The `fort63_style_file.qml` is intended for the specific sample files used in this tutorial, so it may not work with other fort.63 and fort.74 files. However, if you want to use the same color mapping and wind vector properties for your own files, you can open [the Layer Styling Panel](https://docs.qgis.org/3.22/en/docs/user_manual/introduction/general_tools.html#layer-styling-panel) and see which parameters and settings have been modified.
