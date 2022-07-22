# Loading ADCIRC netCDF Files with QGIS and Adding Basemaps

## Background

There are two major differences between visualizing ADCIRC netCDF output with QGIS and ParaView. The first is that QGIS can read ADCIRC netCDF files directly, while [ParaView needs an additional XDMF file](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/getting_started.md#background) to interpret netCDF.

The second is that QGIS makes it easy to load basemaps which provide a geographic context for ADCIRC output and serve as background imagery. This tutorial will show you how to load ADCIRC netCDF files into QGIS, use the default QGIS basemap, and add new basemaps.

For resources on QGIS basics, see the `README.md` in this directory.

## Installing QGIS

There are [instructions on the QGIS website](https://qgis.org/en/site/forusers/download.html) for downloading and installing the latest version. You can find installation instructions for Windows, Mac, and Linux machines.

The tutorials in this directory were tested with QGIS versions 3.22.6 and 3.26.0. Although later versions should work as well, you can use one of these versions if you encounter any errors with newer ones.

## Loading an ADCIRC netCDF file

There are two options for loading an ADCIRC netCDF file into QGIS. The first option is to use the Browser panel to navigate to the file you want to load. Once you get to a netCDF file, you can expand its contents to show different layers, as seen under the `maxele.63.nc` file in this figure:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_01.png)

To load an ADCIRC netCDF file, right-click on the `adcirc_mesh` layer that has a mesh icon next to it, and select "Add Layer to Project" (you can also click and drag the layer into the Layers panel under the Browser panel). 

For the second option, see [this section](https://docs.qgis.org/3.22/en/docs/user_manual/managing_data_source/opening_data.html#loading-a-mesh-layer) of the QGIS documentation.

If your data is on a large mesh, it will take a few seconds for the file to load in. If you have timeseries files like fort.63 and fort.74 with many timesteps and on a large mesh, QGIS may actually crash when trying to load them in. The [`fort63_fort74_qgis.md`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/fort63_fort74_qgis.md) tutorial shows a possible workaround for this issue, but in general it's best to load files with as few timesteps as possible (you may have to make subsets of your files if they have too many timesteps).

## Loading the default QGIS basemap

By default, QGIS should include the OpenStreetMap basemap. Like Google Maps, the OpenStreetMap basemap adapts its level of detail to how far zoomed in you are, making it easy to see cities and roads.

To find and load OpenStreetMap, scroll down in the Browser panel until you see "XYZ Tiles"; OpenStreetMap should be under this section:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_03.png)

To load the basemap layer, you can either right-click and select "Add Layer to Project" or click and drag the layer into the Layers panel.

The easiest way to use basemaps with ADCIRC output is to **first load the ADCIRC netCDF file you want to visualize**, and then load any basemaps you want to use. When you load a basemap layer after loading an ADCIRC netCDF file, QGIS will automatically place the basemap layer at the top of the Layers panel. To move the basemap underneath the ADCIRC data, you can left-click on it in the Layers panel and select "Move to Bottom":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_07.png)

Or click and drag it under the ADCIRC netCDF file layer.

## Adding other basemaps

You can also add other types of basemaps, such as Google street maps and satellite imagery. For instructions on adding these and other basemaps, see [this tutorial](https://hydro-informatics.com/geopy/use-qgis.html#basemaps-for-qgis-google-or-open-street-maps-worldmap-tiles).
