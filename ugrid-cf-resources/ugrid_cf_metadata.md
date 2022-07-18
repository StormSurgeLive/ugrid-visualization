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
The `netcdf-bin` package includes some basic netCDF tools made by the netCDF developers, and the `nco` (NetCDF Operators) package includes more advanced tools.

On Mac, the following commands may work to get these tools:
```
$ brew install netcdf
$ brew install nco
```
If you need a sample netCDF file, you can download an ADCIRC maxele.63 with the following command:
```
$ wget https://fortytwo.cct.lsu.edu/thredds/fileServer/2020/laura/27/CTXCS2017/qbc.loni.org/CTXCS2017_al132020_jgf/nhcConsensus/maxele.63.nc
```
This file has maximum water surface elevation data representing the storm surge due to Hurricane Laura (2020). The file size is ~129 MB.

## Quick overview of a netCDF file

The simplest way to understand the contents of a netCDF file is to view the contents of the file's header, which contains a summary of its metadata.
To view a file's header, use the `ncdump` utility with the `-h` flag (on Ubuntu, this utility is included in the `netcdf-bin` package). Make sure not to miss the `-h`
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
The properties listed under each variable are known as CF attributes. The time variable is defined relative to a specified date/time, so the `time:units` attribute
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
