# ParaView Python script to automate visualization of output from the ADCIRC model 
# This script is intended for use in headless mode (no GUI)
# You should only use this script with the ParaView headless binaries for Linux

# Author: Marcos Botto Tornielli, July 2022 (Contact email: mbottot@mit.edu)

'''
PURPOSE:
Generate frames for an animation of bathymetry/topography and water surface elevation from a  
zoomed-in 3D perspective for an ADCIRC fort.63 file
'''

'''
ARGUMENTS:
    Argument 1: The path to the input directory which contains the file to be visualized
    Argument 2: The path to the output directory where you want the visualization to be saved
    Argument 3: The path to the directory which contains necessary color maps
    Argument 4: An integer that defines the upper bound for the water surface elevation color map
    Argument 5: An integer representing the index of the first timestep to be animated 
    Argument 6: An integer representing the index of the last timestep to be animated 
    Argument 7: A string that defines the zoom area for the visualiation to focus on 
    Argument 8: A string that defines a contact email to be displayed in the visualization

    Note that argument 3 becomes optional once you've run any similar scripts for the first time,
since ParaView will remember loaded color maps. However, for simplicity in automation, you can
always include the 3rd argument, since this script checks whether or not the color maps have been
previously loaded and doesn't load them again if they have been already.
'''

'''
REQUIREMENTS:
This script will only work for visualizing a fort.63.nc file (water surface elevation time series
data on an unstructured mesh)

The input directory (argument 1) needs to contain a fort.63.nc file, named exactly "fort.63.nc"
and any alternate names will cause errors

The input directory also needs to contain an XDMF file associated with the fort.63.nc, named 
exactly "fort.63.nc.xmf"

Finally, the input directory should also contain a file named label_info.txt which has metadata
from the header of maxele.63.nc that this script needs

The color map directory needs to contain the color map files blueBrownGreenBathyTopoColorMap.xml
and RdYlBu_Brewer.xml

You need to have an installation of headless ParaView for linux, which you can find on the official
ParaView downloads page
'''

'''
EXAMPLE USAGE:
Suppose you have saved the paths for the 8 arguments in shell variables ARG1, ARG2, ARG3, ARG4, ARG5, 
ARG6, ARG7, and ARG8, and you have saved the path to your ParaView installation in shell variable PV_PATH

Then, usage of this script could look like this:
"$PV_PATH"/bin/pvpython latx_3D_fort63.py "$ARG1" "$ARG2" "$ARG3" "$ARG4" "$ARG5" "$ARG6" "$ARG7" "$ARG8"

After running this, you should see images in your output directory corresponding to how many frames
you wanted to output, named with the pattern: latx_3D_frame.0000.png, latx_3D_frame.0001.png, etc.
'''

#### import the simple module from the paraview
from paraview.simple import *
import sys
from os import path
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# Defining a function to check whether or not ParaView has a color map preset loaded
# Credit for this function goes to Utkarsh Ayachit from Kitware
# (as posted in ParaView mailing list answer https://www.paraview.org/pipermail/paraview/2016-September/038002.html)
# Input is a string of the color map's name
def hasPreset(name):
    presets = servermanager.vtkSMTransferFunctionPresets()
    for i in range(presets.GetNumberOfPresets()):
        if presets.GetPresetName(i) == name:
            return True
    return False

#########################################################################################################
# READING THE FILE
#########################################################################################################

# define arguments variable
pvpy_args = sys.argv

# Read maxele file
fort63ncxmf = XDMFReader(registrationName='fort.63.nc.xmf', FileNames=[path.join(pvpy_args[1],"fort.63.nc.xmf")])

#########################################################################################################
# COLOR MAPPING AND ZOOM
#########################################################################################################

# find settings proxy
colorPalette = GetSettingsProxy('ColorPalette')

# Properties modified on colorPalette
colorPalette.Background = [0.4196078431372549, 0.4196078431372549, 0.4196078431372549]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1441, 755]

# get layout
layout1 = GetLayout()

#change interaction mode for render view
renderView1.InteractionMode = '3D'

# get the material library
materialLibrary1 = GetMaterialLibrary()

# reset view to fit data
renderView1.ResetCamera()

# set the camera position
camera = GetActiveCamera()
if (pvpy_args[7] == "New_Orleans_East"):
    camera.SetFocalPoint(-88.52198467458054, 120.77437874524261, -53.14711660731809)
    camera.SetPosition(-89.91221667152026, 29.757427626075984, 0.13809094985389764)
    camera.SetViewUp(-0.08048528313755052, 0.504504793355946, 0.8596493661250165)
elif (pvpy_args[7] == "Lake_Pontchartrain"):
    camera.SetFocalPoint(-97.56869230238291, 117.98331797520105, -56.89910324463696)
    camera.SetPosition(-90.20234730232661, 29.644767158998413, 0.2618001901315108)
    camera.SetViewUp(-0.04304880871766271, 0.5402193360289785, 0.8404224348792694)
elif (pvpy_args[7] == "Morgan_City"):
    camera.SetFocalPoint(-97.95118461067642, 123.29648413856498, -47.639893050168425)
    camera.SetPosition(-91.18869129297727, 29.48385678588233, 0.09679214853201257)
    camera.SetViewUp(-0.07518244471188659, 0.44791977875377836, 0.8909071061610804)
elif (pvpy_args[7] == "Houma"):
    camera.SetFocalPoint(-99.81617677071728, 117.0705114173826, -57.72866880402744)
    camera.SetPosition(-90.69149529387974, 29.354860067427644, 0.13354837303017356)
    camera.SetViewUp(-0.033301673027102054, 0.5479210084418503, 0.8358669553712851)
elif (pvpy_args[7] == "Cameron"):
    camera.SetFocalPoint(-97.02134386618157, 121.22573980784554, -51.49317345576091)
    camera.SetPosition(-93.34469007272982, 29.39921274787589, 0.27267074128462293)
    camera.SetViewUp(-0.039636821825489214, 0.4894877094531209, 0.8711088936808713)
    
Render()

# find source
if (FindSource('fort.63.nc_fort.74.nc.xmf')) is not None:
    generalSource = FindSource('fort.63.nc_fort.74.nc.xmf')
    sourceName = 'fort.63.nc_fort.74.nc.xmf'
elif (FindSource('fort.63.nc.xmf')) is not None:
    generalSource = FindSource('fort.63.nc.xmf')
    sourceName = 'fort.63.nc.xmf'
elif (FindSource('maxele.63.nc.xmf')) is not None:
    generalSource = FindSource('maxele.63.nc.xmf')
    sourceName = 'maxele.63.nc.xmf'

#### This section defines the color mapping properties for bathymetry/topography ####
# get color transfer function/color map for 'BathymetricDepth'
bathymetricDepthLUT = GetColorTransferFunction('BathymetricDepth')
bathymetricDepthLUT.RGBPoints = [-106.09833, 0.231373, 0.298039, 0.752941, 3938.042335, 0.865003, 0.865003, 0.865003, 7982.183, 0.705882, 0.0156863, 0.14902]
bathymetricDepthLUT.ScalarRangeInitialized = 1.0

# Import custom bathy/topo color map only if it hasn't been imported before
if (hasPreset("blueBrownGreenBathyTopo") is False):
    ImportPresets(filename=path.join(pvpy_args[3],"blueBrownGreenBathyTopoColorMap.xml"))

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
bathymetricDepthLUT.ApplyPreset('blueBrownGreenBathyTopo', False)

# get opacity transfer function/opacity map for 'BathymetricDepth'
bathymetricDepthPWF = GetOpacityTransferFunction('BathymetricDepth')
bathymetricDepthPWF.Points = [-106.09833, 0.0, 0.5, 0.0, 7982.183, 1.0, 0.5, 0.0]
bathymetricDepthPWF.ScalarRangeInitialized = 1

# Rescale transfer function
bathymetricDepthPWF.RescaleTransferFunction(-20.0, 100.0)

bathymetricDepthLUT.AutomaticRescaleRangeMode = 'Never'

# get color legend/bar for bathymetricDepthLUT in view renderView1
bathymetricDepthLUTColorBar = GetScalarBar(bathymetricDepthLUT, renderView1)
bathymetricDepthLUTColorBar.ComponentTitle = ''
bathymetricDepthLUTColorBar.AutoOrient = 0
bathymetricDepthLUTColorBar.Orientation = 'Horizontal'
bathymetricDepthLUTColorBar.WindowLocation = 'AnyLocation'
bathymetricDepthLUTColorBar.Position = [0.4461287659431904, 0.8996311649840824]
bathymetricDepthLUTColorBar.Title = 'Bathymetry/Topography (m)'
bathymetricDepthLUTColorBar.AddRangeLabels = 0
bathymetricDepthLUTColorBar.ScalarBarLength = 0.2
bathymetricDepthLUTColorBar.LabelFontSize = 10
bathymetricDepthLUTColorBar.ScalarBarThickness = 16
bathymetricDepthLUTColorBar.TitleBold = 1
bathymetricDepthLUTColorBar.TitleShadow = 1
bathymetricDepthLUTColorBar.LabelBold = 1
bathymetricDepthLUTColorBar.LabelShadow = 1
#### end definition of bathymetry/topography color map properties ####

#### This section defines scalar warp properties to produce an exaggerated 3D effect based on bathymetry/topography values ####
bathyTopoScalarWarp = WarpByScalar(registrationName='BathyTopoWarp',Input=generalSource)
bathyTopoScalarWarp.Scalars = ['POINTS', 'BathymetricDepth']
bathyTopoScalarWarp.ScaleFactor = -0.001
bathyTopoScalarWarpDisplay = Show(bathyTopoScalarWarp, renderView1, 'UnstructuredGridRepresentation')
Hide(generalSource, renderView1)
bathyTopoScalarWarpDisplay.SetScalarBarVisibility(renderView1, True)
renderView1.Update()
bathymetricDepthLUTColorBar.WindowLocation = 'AnyLocation'
bathymetricDepthLUTColorBar.Position = [0.4461287659431904, 0.8996311649840824]
#### end definition of bathymetry/topography scalar warp properties ####

#### This section defines the color mapping properties for water surface elevation ####
# create a new 'Threshold' to filter out ADCIRC missing values for water surface elevation
zetaThreshold = Threshold(registrationName='WaterSurfEleThreshold',Input=generalSource)
if (FindSource('maxele.63.nc.xmf')) is not None:
    zetaThreshold.Scalars = ['POINTS', 'zeta_max']
else:
    zetaThreshold.Scalars = ['POINTS', 'zeta']
	
zetaThreshold.ThresholdRange = [-9999.0, 7982.183]

# show data in view
zetaThresholdDisplay = Show(zetaThreshold, renderView1, 'UnstructuredGridRepresentation')

# set scalar coloring
ColorBy(zetaThresholdDisplay, ('POINTS', zetaThreshold.Scalars[1]))

# rescale color and/or opacity maps used to include current data range
zetaThresholdDisplay.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
zetaThresholdDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'zeta' or 'zeta_max'
zetaLUT = GetColorTransferFunction(zetaThreshold.Scalars[1])

# get opacity transfer function/opacity map for 'zeta' or 'zeta_max'
zetaPWF = GetOpacityTransferFunction(zetaThreshold.Scalars[1])

# Import custom zeta color map only if it hasn't been imported before
if (hasPreset("RdYlBu_Brewer") is False):
    ImportPresets(filename=path.join(pvpy_args[3],"RdYlBu_Brewer.xml"))

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
zetaLUT.ApplyPreset('RdYlBu_Brewer', True)

# Rescale transfer function
zetaLUT.RescaleTransferFunction(0.0, float(pvpy_args[4]))

# Rescale transfer function
zetaPWF.RescaleTransferFunction(0.0, float(pvpy_args[4]))

zetaLUT.AutomaticRescaleRangeMode = 'Never'

# get color legend/bar for zetaLUT in view renderView1
zetaLUTColorBar = GetScalarBar(zetaLUT, renderView1)
zetaLUTColorBar.ComponentTitle = ''
zetaLUTColorBar.AutoOrient = 0
zetaLUTColorBar.Orientation = 'Horizontal'
zetaLUTColorBar.WindowLocation = 'AnyLocation'
zetaLUTColorBar.Position = [0.7248275862068965, 0.8996311649840824] 
zetaLUTColorBar.Title = 'Water Surface Elevation (m)'
zetaLUTColorBar.AddRangeLabels = 0
zetaLUTColorBar.ScalarBarLength = 0.2
zetaLUTColorBar.LabelFontSize = 10
zetaLUTColorBar.ScalarBarThickness = 16
zetaLUTColorBar.TitleBold = 1
zetaLUTColorBar.TitleShadow = 1
zetaLUTColorBar.LabelBold = 1
zetaLUTColorBar.LabelShadow = 1
#### end definition of water surface elevation color map properties ####

#### This section defines scalar warp properties to produce an exaggerated 3D effect based on water surface elevation values ####
zetaScalarWarp = WarpByScalar(registrationName='WaterSurfEleWarp',Input=zetaThreshold)
zetaScalarWarp.Scalars = ['POINTS', zetaThreshold.Scalars[1]]
zetaScalarWarp.ScaleFactor = 0.001
zetaScalarWarpDisplay = Show(zetaScalarWarp, renderView1, 'UnstructuredGridRepresentation')
Hide(zetaThreshold, renderView1)
zetaScalarWarpDisplay.SetScalarBarVisibility(renderView1, True)
#ColorBy(zetaScalarWarpDisplay, ('POINTS', zetaThreshold.Scalars[1]))
renderView1.Update()
zetaLUTColorBar.WindowLocation = 'AnyLocation'
zetaLUTColorBar.Position = [0.7248275862068965, 0.8996311649840824]

# get display properties
zetaScalarWarpDisplay = GetDisplayProperties(zetaScalarWarp, view=renderView1)
# set scalar coloring
ColorBy(zetaScalarWarpDisplay, ('POINTS', zetaThreshold.Scalars[1]))
# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(bathymetricDepthLUT, renderView1)
# rescale color and/or opacity maps used to include current data range
zetaScalarWarpDisplay.RescaleTransferFunctionToDataRange(True, False)
# show color bar/color legend
zetaScalarWarpDisplay.SetScalarBarVisibility(renderView1, True)
# change scalar bar placement
zetaLUTColorBar.WindowLocation = 'AnyLocation'
zetaLUTColorBar.Position = [0.7248275862068965, 0.8996311649840824]
# Rescale transfer function
zetaLUT.RescaleTransferFunction(0.0, float(pvpy_args[4]))
# Rescale transfer function
zetaPWF.RescaleTransferFunction(0.0, float(pvpy_args[4]))

# Opacity/lighting properties
zetaScalarWarpDisplay.Opacity = 0.95
zetaScalarWarpDisplay.Diffuse = 0.9
#### end definition of water surface elevation scalar warp properties ####

# Hide orientation axes
renderView1.OrientationAxesVisibility = 0

#########################################################################################################
# NETCDF HEADER INFO ANNOTATION
#########################################################################################################

dir_path = pvpy_args[1]

# create a new 'Programmable Annotation'
programmableAnnotation1 = ProgrammableAnnotation(registrationName='ProgrammableAnnotation1', Input=generalSource)
programmableAnnotation1.PythonPath = ''

# Properties modified on programmableAnnotation1
programmableAnnotation1.Script = """from datetime import datetime, timedelta
from os import path

mydir = \"""" + dir_path + """\"

myfile = "label_info.txt"

path = path.join(mydir, myfile)

with open(path) as header_file:
    header_list = [line.rstrip() for line in header_file]
	
# Label has 3 lines:
# Line 1: Model info
# Line 2: Storm/Advisory info
# Line 3: Current date/time

# Create label string for line 1
model_name = header_list[0]
grid_name = header_list[1]
if ".grd" in grid_name:
    grid_name = grid_name.replace(".grd",'')
model_label = model_name + " " + grid_name 

# Create label string for line 2
adv_string = header_list[3]
# If netCDF file comes from a NAM-driven ADCIRC run
if "NAM" in adv_string:
    adv_str_split = adv_string.split(\' \')
    adv_label_prt1 = adv_str_split[4]
    adv_label = header_list[2] + " " + adv_label_prt1
# If netCDF file comes from an NHC advisory-driven ADCIRC run
else:
    adv_str_split = adv_string.split(\' \')
    adv_label_prt1 = adv_str_split[2].split(\':\')[1]
    adv_label_prt2 = header_list[4].split(\' \')[0]
    adv_label = header_list[2] + " " + adv_label_prt1 + " " + adv_label_prt2

# Setup for line 3: get date/time info in proper format to pass to calendar
datetime_string = header_list[5]
ymd_string = datetime_string.split(' ')[2]
hms_string = datetime_string.split(' ')[3]
year = int(ymd_string.split('-')[0])
month = int(ymd_string.split('-')[1])
day = int(ymd_string.split('-')[2])
hour = int(hms_string.split(':')[0])
min = int(hms_string.split(':')[1])
sec = int(hms_string.split(':')[2])

# Pass date/time info to calendar
date_since = datetime(year,month,day,hour,min,sec)

# Get current "seconds after" time
sec_add = inputs[0].GetInformation().Get(vtk.vtkDataObject.DATA_TIME_STEP())

date_curr = date_since + timedelta(seconds=sec_add)

source_type = \"""" + sourceName + """\"

to = self.GetTableOutput()
arr = vtk.vtkStringArray()
arr.SetName("Text")
arr.SetNumberOfComponents(1)
if source_type == "maxele.63.nc.xmf":
    arr.InsertNextValue(model_label + '\\n\\n' + adv_label)
else:
    arr.InsertNextValue(model_label + '\\n\\n' + adv_label + '\\n\\n' + str(date_curr) + ' ' + "UTC")
to.AddColumn(arr)"""

# show data in view
programmableAnnotation1Display = Show(programmableAnnotation1, renderView1, 'TextSourceRepresentation')

programmableAnnotation1Display.Bold = 1
programmableAnnotation1Display.Shadow = 1
programmableAnnotation1Display.FontSize = 20

# update the view to ensure updated data information
renderView1.Update()

#########################################################################################################
# CONTACT EMAIL ANNOTATION
#########################################################################################################

textEmail = Text(registrationName='TextEmail')
textEmail.Text = 'Contact Email: ' + pvpy_args[8] 
textEmailDisplay = Show(textEmail, renderView1, 'TextSourceRepresentation')
textEmailDisplay.Bold = 1
textEmailDisplay.Shadow = 1
textEmailDisplay.WindowLocation = 'LowerLeftCorner'
textEmailDisplay.FontSize = 25

renderView1.Update()

#########################################################################################################
# SAVE IMAGE
#########################################################################################################

# get layout
layout1 = GetLayout()

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(1450, 778)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
if (pvpy_args[7] == "New_Orleans_East"):
    renderView1.CameraPosition = [-89.91221667152026, 29.757427626075984, 0.13809094985389764]
    renderView1.CameraFocalPoint = [-88.52198467458054, 120.77437874524261, -53.14711660731809]
    renderView1.CameraViewUp = [-0.08048528313755052, 0.504504793355946, 0.8596493661250165]
    renderView1.CameraParallelScale = 26.777118184744843
elif (pvpy_args[7] == "Lake_Pontchartrain"):
    renderView1.CameraPosition = [-90.20234730232661, 29.644767158998413, 0.2618001901315108]
    renderView1.CameraFocalPoint = [-97.56869230238291, 117.98331797520105, -56.89910324463696]
    renderView1.CameraViewUp = [-0.04304880871766271, 0.5402193360289785, 0.8404224348792694]
    renderView1.CameraParallelScale = 26.777118184744843
elif (pvpy_args[7] == "Morgan_City"):
    renderView1.CameraPosition = [-91.18869129297727, 29.48385678588233, 0.09679214853201257]
    renderView1.CameraFocalPoint = [-97.95118461067642, 123.29648413856498, -47.639893050168425]
    renderView1.CameraViewUp = [-0.07518244471188659, 0.44791977875377836, 0.8909071061610804]
    renderView1.CameraParallelScale = 26.777118184744843
elif (pvpy_args[7] == "Houma"):
    renderView1.CameraPosition = [-90.69149529387974, 29.354860067427644, 0.13354837303017356]
    renderView1.CameraFocalPoint = [-99.81617677071728, 117.0705114173826, -57.72866880402744]
    renderView1.CameraViewUp = [-0.033301673027102054, 0.5479210084418503, 0.8358669553712851]
    renderView1.CameraParallelScale = 26.777118184744843
elif (pvpy_args[7] == "Cameron"):
    renderView1.CameraPosition = [-93.34469007272982, 29.39921274787589, 0.27267074128462293]
    renderView1.CameraFocalPoint = [-97.02134386618157, 121.22573980784554, -51.49317345576091]
    renderView1.CameraViewUp = [-0.039636821825489214, 0.4894877094531209, 0.8711088936808713]
    renderView1.CameraParallelScale = 26.844335881058356

# Modify animation mode from default Sequence mode to Snap To TimeSteps
# The default Sequence mode only saves 10 frames, evenly spaced, for the whole time frame
# So it's necessary to change to Snap To TimeSteps for every timestep to be considered at 1fps
# This is only an issue when scripting with Python; in normal GUI use the mode defaults to Snap To Timesteps
animScene = GetAnimationScene()
animScene.PlayMode = 'Snap To TimeSteps'

# Save animation
animStartTime = int(pvpy_args[5])
animEndTime = int(pvpy_args[6])
SaveAnimation(path.join(pvpy_args[2],"latx_3D_frame.png"), renderView1, ImageResolution=[1450, 778], FrameWindow=[animStartTime,animEndTime])
