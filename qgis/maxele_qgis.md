# Visualizing an ADCIRC maxele.63 File with QGIS

## Software requirements

Before starting this tutorial, see the [Loading ADCIRC netCDF Files with QGIS and Adding Basemaps](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md) document for QGIS installation instructions and how to load ADCIRC netCDF files into QGIS.

The sample file for this tutorial is a maxele.63 from the storm surge due to Hurricane Laura (2020). You can download it through a browser at the following page (click on the "HTTPServer" link once you're at the page):
```
https://fortytwo.cct.lsu.edu/thredds/catalog/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/catalog.html?dataset=2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/maxele.63.nc
```
Or, if you prefer to download it through the command line, run the following command on a Unix shell:
```
$ wget https://fortytwo.cct.lsu.edu/thredds/fileServer/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/maxele.63.nc
```

You will also need the files `maxele_style_file.qml` and `color_bar.png` from the `ugrid-visualization/qgis/qgis-files` directory.

## Loading the `maxele.63.nc` file

After [loading the sample maxele.63 file](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md#loading-an-adcirc-netcdf-file) into QGIS, your Map canvas should look like this:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_02.png)

## Color mapping water surface elevation

The `maxele_style_file.qml` file will make it easy to set color mapping properties for the water surface elevation variable. Right-click on the `adcirc_mesh` layer in the Layers panel and select "Properties...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_04.png)

This will take you to the Layer Properties menu. At the bottom left of this menu, there is a Style drop-down menu; open this menu and select "Load Style...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_05.png)

Then, browse for the `maxele_style_file.qml` file and apply it. After selecting "OK" in the Layer Properties menu, your Map canvas should look like this:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_06.png)

## Load the OpenStreetMap basemap

Next, [load the OpenStreetMap basemap layer](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/getting_started.md#loading-the-default-qgis-basemap) and move it below the `adcirc_mesh` layer in the Layers panel. Your Map canvas should now look like this:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_08.png)

## Add a color bar (and optionally other annotations)

In the View menu at the uppermost toolbar, select "Decorations" -> "Image...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_09.png)

Now, browse for `color_bar.png`, set the size to 75.00 mm, and select "OK". You should now see a color bar at the bottom left of the Map canvas.

You can also add other annotations to the visualization, such as a scale bar:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_10.png)

## Saving an image

To save an image from the Map canvas, go to the Project menu at the uppermost toolbar, and select "Import/Export" -> "Export Map to Image...":

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_11.png)

This will take you to the Save Map as Image menu:

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_screenshot_11.png)

If you select the Draw on Canvas option, then you can draw a box on the Map canvas to specify the lat/lon extent of your visualization. Otherwise, you can also zoom in to a specific area before opening the Save Map as Image menu, and use the Map canvas extent as your lat/lon extent.

For example, here is a visualization made by zooming in to the area where Hurricane Laura made landfall:
![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/qgis/tutorial-figures/tutorial_figure_1.png)

## Visualizing other maxele.63 files

The `maxele_style_file.qml` is intended for the specific sample file used in this tutorial, so it may not work with other maxele.63 files. However, if you want to use the same color mapping properties for your own files, you can open [the Layer Styling Panel](https://docs.qgis.org/3.22/en/docs/user_manual/introduction/general_tools.html#layer-styling-panel) and see which parameters and settings have been modified.

