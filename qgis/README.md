# Tutorials for Visualizing ADCIRC Output with QGIS

## Contents

* `qgis-files/` - QGIS-specific files that will facilitate formatting and annotation of visualizations.
* `tutorial-figures/` - Figures referenced in the tutorial documents.
* `getting-started.md` - Introductory tutorial with instructions for QGIS installation, how to load ADCIRC netCDF files, and adding basemaps. Make sure to start here if you've never used QGIS to visualize ADCIRC output before.
* `maxele_qgis.md` - Tutorial for visualizing an ADCIRC maxele.63 file with QGIS.
* `fort63_fort74_qgis.md` Tutorial for visualizing a combined ADCIRC fort.63 and fort.74 files with QGIS.

## Requirements and expected background knowledge

The tutorials should work on Windows, Mac, or Linux machines, but they have only been tested on Windows. The `getting-started.md` document provides a link to QGIS installation instructions.

For the `fort63_fort74_qgis.md` tutorial, you'll need access to a Unix shell that can install the `nco` package. If you're using a Windows machine, you can use [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/setup/environment). You'll also need `conda` to set up a Python environment. If you haven't used `conda` before, you can find installation instructions for Miniconda [here](https://docs.conda.io/en/latest/miniconda.html). Additionally, if you want to generate an animation like the one shown in this tutorial, you'll need to know how to make a GIF from PNG files (for example, you can do this with the command-line tool `ffmpeg`).

### QGIS

QGIS (https://qgis.org/en/site/about/index.html) is an open-source Geographic Information System (GIS) application that can be used for mapping and geospatial analysis. It also has the capability to visualize mesh data, like ADCIRC output, alongside with maps. QGIS is a GUI application.

Before reading the tutorial documents in this directory, it's recommended that you become familiar with key elements of the QGIS GUI. Here are some resources to help you get started:
* [General resource about the QGIS GUI (QGIS docs)](https://docs.qgis.org/3.22/en/docs/user_manual/introduction/qgis_gui.html)
* Documentation on the [Browser Panel](https://docs.qgis.org/3.22/en/docs/user_manual/managing_data_source/opening_data.html#the-browser-panel) and [Layers Panel](https://docs.qgis.org/3.22/en/docs/user_manual/introduction/general_tools.html#layers-panel) (these are the GUI elements you'll be using the most in the tutorials)
* Documentation for [working with mesh data](https://docs.qgis.org/3.22/en/docs/user_manual/working_with_mesh/mesh_properties.html)

There'a also a [tutorial](https://www.lutraconsulting.co.uk/blog/2019/08/26/foss4g-workshop/) by the developers of the QGIS mesh capabilties for loading and visualizing a sample netCDF dataset.

## Credits

The `fix_adcirc_modwind.py` script in the `qgis-files/` directory is a modified version of a script developed by Marcelo Andrioni (https://github.com/marceloandrioni). You can find the original script in [this GitHub discussion](https://github.com/lutraconsulting/MDAL/issues/155).
