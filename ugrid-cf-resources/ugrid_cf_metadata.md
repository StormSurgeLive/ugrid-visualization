# Viewing & Modifying CF/UGRID Metadata in an ADCIRC netCDF File

## Background

The netCDF file format is a type of format used to store large amounts of scientific data efficiently. As well as the data itself, netCDF files contain metadata
which helps to identify the data and its properties.

The metadata and structure of ADCIRC output files in netCDF format are based on the CF and UGRID conventions. The UGRID conventions were designed as an extension of CF
that allows for data defined on unstructured meshes. As of July 2022, UGRID has not yet been formally incorporated into CF, so there are some discrepancies between
the two sets of conventions. However, metadata from both conventions is still useful when visualizing ADCIRC output.

For detailed background on netCDF, CF, and UGRID, you can refer to the following resources:
* NetCDF frequently asked questions: https://docs.unidata.ucar.edu/netcdf-c/current/faq.html
* CF conventions homepage: https://cfconventions.org/
* UGRID conventions homepage: http://ugrid-conventions.github.io/ugrid-conventions/

## Software requirements

To follow along with the examples in this document with your own netCDF file, you'll need to download some command-line tools for working with netCDF. On
Ubuntu Linux, you can download these tools with the following commands:

```
$ sudo apt install netcdf-bin
$ sudo apt install nco
```
You may need to run `sudo apt update && sudo apt upgrade` beforehand if the packages can't be found. The `netcdf-bin` package includes some basic netCDF tools made by the netCDF developers, and the `nco` (NetCDF Operators) package includes more advanced tools.

On Mac, the following commands may work to get these tools:
```
$ brew install netcdf
$ brew install nco
```
If you need a sample netCDF file, you can download an ADCIRC maxele.63 with the following command:
```
$ wget https://fortytwo.cct.lsu.edu/thredds/fileServer/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/maxele.63.nc
```
This file has maximum water surface elevation data for the storm surge due to Hurricane Laura (2020). The file size is ~129 MB.

## Quick overview of a netCDF file

The simplest way to understand the contents of a netCDF file is to view the file's header, which contains a summary of its metadata.
To view a file's header, use the `ncdump` utility with the `-h` flag (on Ubuntu, this utility is included in the `netcdf-bin` package, and should be on your path once you've installed `netcdf-bin`). Make sure not to miss the `-h`
flag; otherwise, ncdump will try to display the entire contents of the file, which may be a very large amount of data.

Here's the result of running `ncdump -h` on the sample maxele.63 file from the [Software requirements](#Software-requirements) section:
```diff
$ ncdump -h maxele.63.nc
netcdf maxele.63 {
dimensions:
        time = UNLIMITED ; // (1 currently)
        node = 4535035 ;
        nele = 8975076 ;
        nvertex = 3 ;
        nope = 1 ;
        neta = 238 ;
        max_nvdll = 238 ;
        nbou = 968 ;
        nvel = 95803 ;
        max_nvell = 6170 ;
        mesh = 1 ;
variables:
        double time(time) ;
                time:long_name = "model time" ;
                time:standard_name = "time" ;
                time:units = "seconds since 2020-07-22 00:00:00" ;
                time:base_date = "2020-07-22 00:00:00" ;
        double x(node) ;
                x:long_name = "longitude" ;
                x:standard_name = "longitude" ;
                x:units = "degrees_east" ;
                x:positive = "east" ;
        double y(node) ;
                y:long_name = "latitude" ;
                y:standard_name = "latitude" ;
                y:units = "degrees_north" ;
                y:positive = "north" ;
        int element(nele, nvertex) ;
                element:long_name = "element" ;
                element:cf_role = "face_node_connectivity" ;
                element:start_index = 1 ;
                element:units = "nondimensional" ;
        int adcirc_mesh(mesh) ;
                adcirc_mesh:long_name = "mesh_topology" ;
                adcirc_mesh:cf_role = "mesh_topology" ;
                adcirc_mesh:topology_dimension = 2 ;
                adcirc_mesh:node_coordinates = "x y" ;
                adcirc_mesh:face_node_connectivity = "element" ;
        int neta ;
                neta:long_name = "total number of elevation specified boundary nodes" ;
                neta:units = "nondimensional" ;
        int nvdll(nope) ;
                nvdll:long_name = "number of nodes in each elevation specified boundary segment" ;
                nvdll:units = "nondimensional" ;
        int max_nvdll ;
        int ibtypee(nope) ;
                ibtypee:long_name = "elevation boundary type" ;
                ibtypee:units = "nondimensional" ;
        int nbdv(neta) ;
                nbdv:long_name = "node numbers on each elevation specified boundary segment" ;
                nbdv:units = "nondimensional" ;
        int nvel ;
                nvel:long_name = "total number of normal flow specified boundary nodes including both the front and back nodes on internal barrier boundaries" ;
                nvel:units = "nondimensional" ;
        int nvell(nbou) ;
                nvell:long_name = "number of nodes in each normal flow specified boundary segment" ;
                nvell:units = "nondimensional" ;
        int max_nvell ;
        int ibtype(nbou) ;
                ibtype:long_name = "type of normal flow (discharge) boundary" ;
                ibtype:units = "nondimensional" ;
        int nbvv(nvel) ;
                nbvv:long_name = "node numbers on normal flow boundary segment" ;
                nbvv:units = "nondimensional" ;
        double depth(node) ;
                depth:long_name = "distance  below geoid" ;
                depth:standard_name = "depth below geoid" ;
                depth:coordinates = "time y x" ;
                depth:location = "node" ;
                depth:mesh = "adcirc_mesh" ;
                depth:units = "m" ;
        double zeta_max(node) ;
                zeta_max:long_name = "maximum water surface elevationabove geoid" ;
                zeta_max:standard_name = "maximum_sea_surface_height_above_geoid" ;
                zeta_max:coordinates = "y x" ;
                zeta_max:location = "node" ;
                zeta_max:mesh = "adcirc_mesh" ;
                zeta_max:units = "m" ;
                zeta_max:_FillValue = -99999. ;
        double time_of_zeta_max(node) ;
                time_of_zeta_max:long_name = "time of maximum water surface elevationabove geoid" ;
                time_of_zeta_max:standard_name = "time_of_maximum_sea_surface_height_above_geoid" ;
                time_of_zeta_max:coordinates = "y x" ;
                time_of_zeta_max:location = "node" ;
                time_of_zeta_max:mesh = "adcirc_mesh" ;
                time_of_zeta_max:units = "sec" ;
                time_of_zeta_max:_FillValue = -99999. ;

// global attributes:
                :_FillValue = -99999. ;
                :model = "ADCIRC" ;
                :version = "v53.05-1-gb2460f8" ;
                :grid_type = "Triangular" ;
                :description = "ASGS cs:20200722000000 cy:LAURA27 ASGS" ;
                :agrid = "ctx_p87_tcm.grd" ;
                :rundes = "ASGS cs:20200722000000 cy:LAURA27 ASGS" ;
                :runid = "nhcConsensus" ;
                :title = "Texas ASGS" ;
                :institution = "Computational Hydraulics Group, SeahorseCoastal Consulting LLC" ;
                :source = "Texas Advanced Computing Center" ;
                :history = "ASGS Nowcast/Forecast" ;
                :references = "http://www.tacc.utexas.edu" ;
                :comments = "Model time is relative to UTC." ;
                :host = "TACC" ;
                :convention = "CF" ;
                :Conventions = "UGRID-0.9.0" ;
                :contact = "jason.fleming@seahorsecoastal.com" ;
                :creation_date = "2020-08-26 12:23:05 -05:00" ;
                :modification_date = "2020-08-26 12:23:05 -05:00" ;
                :fort.15 = "==== Input File Parameters (below) ====" ;
                :dt = 0.5 ;
                :ihot = 568 ;
                :ics = 2 ;
                :nolibf = 1 ;
                :nolifa = 2 ;
                :nolica = 0 ;
                :nolicat = 0 ;
                :nwp = 8 ;
                :ncor = 1 ;
                :ntip = 0 ;
                :nws = 20 ;
                :nramp = 1 ;
                :tau0 = -3. ;
                :statim = 0. ;
                :reftim = 0. ;
                :rnday = 40.5 ;
                :dramp = 5. ;
                :a00 = 0.35 ;
                :b00 = 0.3 ;
                :c00 = 0.35 ;
                :h0 = 0.1 ;
                :slam0 = -93.37 ;
                :sfea0 = 29. ;
                :cf = 0.00026 ;
                :eslm = 4. ;
                :cori = 0. ;
                :ntif = 8 ;
                :nbfr = 8 ;
}
```
## Key parts of an ADCIRC netCDF header
As you can see from the previous section, a typical header for an ADCIRC netCDF file is fairly long. This section will summarize the key parts of the metadata
that are most relevant for visualization.

You can find the number of timesteps in the dataset, as well as the number of nodes and elements in the mesh, in the dimensions section:
```
dimensions:
        time = UNLIMITED ; // (1 currently)
        node = 4535035 ;
        nele = 8975076 ;
```
The properties listed under each variable are known as "attributes". The time variable is defined relative to a specified date/time, so the `time:units` attribute
is needed to interpret the raw time values:
```
        double time(time) ;
                time:long_name = "model time" ;
                time:standard_name = "time" ;
                time:units = "seconds since 2020-07-22 00:00:00" ;
                time:base_date = "2020-07-22 00:00:00" ;
```
The following 4 variables define the geometry of the unstructured mesh, according to the UGRID conventions:
```
        double x(node) ;
                x:long_name = "longitude" ;
                x:standard_name = "longitude" ;
                x:units = "degrees_east" ;
                x:positive = "east" ;
        double y(node) ;
                y:long_name = "latitude" ;
                y:standard_name = "latitude" ;
                y:units = "degrees_north" ;
                y:positive = "north" ;
        int element(nele, nvertex) ;
                element:long_name = "element" ;
                element:cf_role = "face_node_connectivity" ;
                element:start_index = 1 ;
                element:units = "nondimensional" ;
        int adcirc_mesh(mesh) ;
                adcirc_mesh:long_name = "mesh_topology" ;
                adcirc_mesh:cf_role = "mesh_topology" ;
                adcirc_mesh:topology_dimension = 2 ;
                adcirc_mesh:node_coordinates = "x y" ;
                adcirc_mesh:face_node_connectivity = "element" ;
```
Finally, the following variables define the bathymetry/topography and water surface elevation, which are the key variables for visualization:
```
        double depth(node) ;
                depth:long_name = "distance  below geoid" ;
                depth:standard_name = "depth below geoid" ;
                depth:coordinates = "time y x" ;
                depth:location = "node" ;
                depth:mesh = "adcirc_mesh" ;
                depth:units = "m" ;
        double zeta_max(node) ;
                zeta_max:long_name = "maximum water surface elevationabove geoid" ;
                zeta_max:standard_name = "maximum_sea_surface_height_above_geoid" ;
                zeta_max:coordinates = "y x" ;
                zeta_max:location = "node" ;
                zeta_max:mesh = "adcirc_mesh" ;
                zeta_max:units = "m" ;
                zeta_max:_FillValue = -99999. ;
````
## What to do if your file is missing UGRID metadata

If the header of your netCDF file looks similar to the example shown above, then you're probably ready to try out the ParaView and QGIS tutorials in this repository. However, depending on how your ADCIRC output has been generated, it may be the case that some attributes needed to indicate key UGRID and CF metadata are missing, leading to errors when you try to visualize your file.

For example, note the differnce between the attributes of the following `adcirc_mesh` variable:
```
        int adcirc_mesh(single) ;
                adcirc_mesh:long_name = "mesh topology" ;
                adcirc_mesh:standard_name = "mesh_topology" ;
                adcirc_mesh:dimension = 2 ;
                adcirc_mesh:node_coordinates = "x y" ;
                adcirc_mesh:face_node_connectivity = "element" ;
```
and the attributes of the `adcirc_mesh` variable in the header of the maxele.63 file from earlier:
```
        int adcirc_mesh(mesh) ;
                adcirc_mesh:long_name = "mesh_topology" ;
                adcirc_mesh:cf_role = "mesh_topology" ;
                adcirc_mesh:topology_dimension = 2 ;
                adcirc_mesh:node_coordinates = "x y" ;
                adcirc_mesh:face_node_connectivity = "element" ;
```
In the first example, we are missing the `cf_role` attribute, and there is a `dimension` attribute instead of `topology_dimension`. These are both required attributes in the UGRID convention, and will lead to errors if the visualization software you're using expects UGRID metadata.

If you think you're running into issues due to missing metadata, you can compare the `ncdump -h` output from your file to the output for the sample maxele.63 file used for the examples in this document, and see if you're missing any attributes (especially in the key sections listed in the [Key parts of an ADCIRC netCDF header](#Key-parts-of-an-ADCIRC-netCDF-header) section.

Another option is to use the `ugrid-checks` utility developed by Patrick Peglar and available on GitHub (https://github.com/pp-mo/ugrid-checks). You can find installation instructions and usage examples on the `ugrid-checks` repository. However, note that as of July 2022, this utility is still in fairly early development, so it may not cover all UGRID errors.

Once you've determined which attributes you're missing, you can use the `ncatted` utility (from the `nco` package) to make the needed changes. **Note that `ncatted` permanently changes your netCDF file**, so if you want to keep you original file, make sure to make a copy before changing any metadata. 

For example, in the first `adcirc-mesh` variable shown earlier in this section, we need to add a `cf_role`, delete the `dimension`, and add a `topology_dimension`. You can make these changes with the following commands (assuming the file with missing metadata is also called `maxele.63.nc`):
```
$ ncatted -h -a cf_role,adcirc_mesh,o,c,"mesh_topology" maxele.63.nc
$ ncatted -h -a dimension,adcirc_mesh,d,, maxele.63.nc
$ ncatted -h -a topology_dimension,adcirc_mesh,o,i,2 maxele.63.nc
```
The `-h` flag doesn't refer to the netCDF header here. When using a utility from the `nco` package, the `-h` flag can be included to prevent the command you ran to be added to the file's `history` global attribute. If you do want to have a record of that command, you can remove the `-h` flag. For more information about the meaning of `ncatted` flags and parameters, you can run `ncatted --help` for a brief summary.

## A note on CF compliance of ADCIRC output

As of July 2022, there are some discrepancies between the metadata in ADCIRC netCDF files and the CF conventions. Some of these discrepancies are due to incorrect metadata, and others are due to the fact that UGRID hasn't yet been formally incorporated into CF (and will remain unavoidable until UGRID and CF are merged).

These differences shouldn't cause any issues for the visualization tutorials in this repository, which use ParaView and QGIS. However, if you want to read more about this topic, refer to the `ADCIRC_UGRID_CF_Changes.pdf` document in this directory. This document also includes information about CF compliance checkers.
