# Tutorials for Visualizing ADCIRC Ouptut with ParaView

## Contents

* `automation-scripts/` - This directory contains scripts for automating the generation of ADCIRC output visualizations using ParaView. You can see examples of the kinds of visualizations these scripts generate in the [`2D_pv_auto.md`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/2D_pv_auto.md) and [`3D_pv_auto.md`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/3D_pv_auto.md) tutorial files.
* `color-maps/` - Color map files needed by ParaView to set color mapping properties for ADCIRC variables. Credits for the color map designs are listed in the directory's `README.md`.
* `tutorial-figures/` - Sample figures generated with the automation scripts. The tutorials will guide you through the steps to reproduce these figures.
* `getting_started.md` - Introductory tutorial. Make sure to start here if you've never used ParaView to visualize ADCIRC output before.
* `2D_pv_auto.md` - Tutorial to generate visualizations from a maxele.63 and fort.63 file. The visualizations are made from a "2D" perspective (in other words, an overhead view) of the Louisiana-Texas coast and the Gulf of Mexico.
* `3D_pv_auto.md` - Tutorial to generate visualizations from a maxele.63 and fort.63 file. The visualizations are made from a "3D" perspective, zoomed in to a specific area of interest.

## Requirements and expected background knowledge

You will have to work in a Linux environment to follow along with the tutorials in this directory. The recommended Linux distribution and version is Ubuntu 20.04. However, any Linux distribution that has access to the APT package manager should work.

The [Getting Started with ParaView for Visualizing ADCIRC NetCDF Output](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/getting_started.md) tutorial will guide you through the ParaView installation steps, as well as other software requirements. The two visualization tutorials also specify some additional software requirements.

Prior experience with ParaView isn't required to follow the tutorial steps. ParaView (https://www.paraview.org/) is an open-source application for scientific visualization that's commonly used as a desktop GUI application. However, the tutorials in this directory will show you how to use ParaView entirely through the command line, with no GUI support. The goal of these tutorials is to provide the basis for a fully automated workflow; this is why command-line use is emphasized over GUI support. 

ParaView supports Python scripting to automate common visualization tasks that you would normally do through the GUI. This is the purpose of the Python scripts in `automation-scripts/`. The Bash script in `automation-scipts/` is intended to facilitate and automate the running of these ParaView Python scripts, so you don't need any prior experience with ParaView Python scripting. However, if you want to extend the capabilities of the scripts or add new ones for different types of visualizations, you can refer to the [ParaView Python documentation](https://kitware.github.io/paraview-docs/latest/python/index.html) to get started.
