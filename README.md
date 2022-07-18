# UGRID Visualization

![](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/paraview/tutorial-figures/latx_2D_fort63_anim.gif)

Resources for the visualization of output files from the ADCIRC ocean circulation model in netCDF format. You can find general resources for understanding and working with ADCIRC netCDF files, as well as tutorials and scripts to facilitate the visualization of ADCIRC output with ParaView and QGIS. ADCIRC output in netCDF format is based on the CF and UGRID conventions, so if you use a different model that also outputs data based on these conventions, the resources in this repository may be relevant as well.

## Repository structure

This repository is divided into 3 subdirectories:

* `ugrid-visualization/ugrid-cf-resources` - Background information for understanding and working with ADCIRC netCDF files. This is a good place to start if you don't have much experience with netCDF files.
* `ugrid-visualization/paraview` - Scripts for automating the visualization of ADCIRC output using ParaView through the command line (no GUI), along with tutorials.
* `ugrid-visualization/qgis` - Tutorials for visualizing ADCIRC output with QGIS, including some QGIS-specific files for streamlining this process.

## Requirements and expected background knowledge

Specific software requirements will be listed in each subdirectory's Readme file. The most basic requirement is access to a Unix shell that can run a package manager. To follow along with the tutorials in this repository, it's expected that you have at least some experience with running commands and command-line tools on a Unix shell. To reproduce examples that use Ubuntu Linux-based commands, it's also expected that you have access to `sudo` to install packages through `apt`.

The main audience for these resources is ADCIRC users, or anyone who works with ADCIRC output. Therefore, it's expected that you have some familiarity with the types of ADCIRC output, especially `maxele.63` files and `fort.63` files. 

If you don't have previous knowledge of ADCIRC and its output but want to follow along with the tutorials, you can refer to the following resources for some background information:
* Introduction to ADCIRC: https://adcirc.org/home/documentation/users-manual-v50/introduction/
* Types of ADCIRC output (most relevant for this repository are maxele.63, fort.63, and fort.74): https://adcirc.org/home/documentation/users-manual-v53/output-file-descriptions/

## Author information
The tutorials and resources in this repository were developed by Marcos Botto Tornielli (Scientific Visualization Developer for Seahorse Coastal Consulting between April and July 2022).

For any questions, please contact me at mbottot@mit.edu.
