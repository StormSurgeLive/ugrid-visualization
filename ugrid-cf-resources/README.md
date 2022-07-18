# Resources for Working with ADCIRC NetCDF Files

## Contents

* `ugrid_cf_metadata.md` - Examples of viewing and modifying CF and UGRID metadata in ADCIRC netCDF files. This is a good place to start if you have no prior experience with netCDF files. If you're already familiar with viewing and modifying netCDF metadata from the command line (in other words, if you've used the `ncdump` and `ncatted` utilities before), then you may want to skip this.
* `downloading_netcdf.md` - Examples of downloading subsets of timeseries ADCIRC netCDF output from a THREDDS server.
* `ADCIRC_UGRID_CF_Changes.pdf` - Overview of discrepancies between ADCIRC netCDF output and UGRID/CF conventions as of July 2022. You can refer to the [last section of `ugrid_metadata.md`](https://github.com/StormSurgeLive/ugrid-visualization/blob/main/ugrid-cf-resources/ugrid_cf_metadata.md#a-note-on-cf-compliance-of-adcirc-output) to see if this document is relevant for you.

## Requirements and expected background knowledge

Required packages are listed in `ugrid_cf_metadata.md` and `downloading_netcdf.md`.

For `downloading_netcdf.md`, it's expected that you have some previous knowledge about ASGS. Otherwise, you can get a brief overview of ASGS in the "About" section of the ASGS repository (https://github.com/StormSurgeLive/asgs). ASGS is used for automated running of ADCIRC during the formation and duration of hurricanes and tropical storms. Visualizing the ADCIRC netCDF files that ASGS ouputs can show the potential impacts of hurricanes through storm surge and winds.

