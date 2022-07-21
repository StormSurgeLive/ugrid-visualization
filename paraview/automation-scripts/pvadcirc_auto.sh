#!/bin/bash

# Author: Marcos Botto Tornielli, July 2022 (Contact email: mbottot@mit.edu)

################################################################################
# DEFINE PARAMETERS FOR PVPYTHON AUTOMATION                                    #
################################################################################
# Define shell variables for paths (for input to pvpython)
# Directory where maxele and fort.63 files are located
IN_DIR=${IN_DIR:-"$PWD"}
# Directory where visualizations should be saved
OUT_DIR=${OUT_DIR:-"$PWD"}
# Directory where color maps are located
CMAP_DIR=${CMAP_DIR:-"$PWD"}

# Paths for automation of running commands
# ParaView installation directory
if [ -z "$PV_DIR" ] ; then
    echo "PV_DIR has not been set as an environment variable. Exiting..."
    exit 1
else
    PV_DIR="$PV_DIR"
fi
# Directory where pvpython scripts are located
SCRPT_DIR=${SCRPT_DIR:-"$PWD"}

# Name of area to zoom into when using 3D pvpython scripts
# Default value is empty value, which means 2D pvpython scripts are used
# (Possible values as of July 2022: New_Orleans_East, Lake_Pontchartrain,
# Houma, Morgan_City, Cameron)
ZOOM_AREA=${ZOOM_AREA:-}

# Names of pvpython scripts
if [ -z "$ZOOM_AREA" ] ; then
    MAXELE_SCRPT="latx_2D_maxele.py"
    FORT63_SCRPT="latx_2D_fort63.py"
else
    MAXELE_SCRPT="latx_3D_maxele.py"
    FORT63_SCRPT="latx_3D_fort63.py"
fi

# Define visualization-related inputs for pvpython
# Upper bound for water surface elevation color map (default value: 5m) 
ZETA_BND=${ZETA_BND:-5}
# Define index of starting timestep for fort.63 animation (default value: 0)
START_T=${START_T:-0}
# Define index of final timestep for fort.63 animation (default value: 9)
FINAL_T=${FINAL_T:-9}
# Contact email for annotation on visualizations
C_EMAIL=${C_EMAIL:-placeholder@email.com}

# Parameter for deciding whether or not to clean up temporary files
# Default action is to clean the file
FILE_CLEAN=${FILE_CLEAN:-true}

################################################################################
# CHECK IF ADCIRC OUTPUT FILES AND XDMFs EXIST IN INPUT DIRECTORY              #
################################################################################

if [ ! -f "$IN_DIR/maxele.63.nc" ]; then
    echo "Input directory is missing a maxele.63.nc file. Exiting..."
    exit 1
elif [ ! -f "$IN_DIR/maxele.63.nc.xmf" ]; then
    echo "Input directory is missing a maxele.63.nc.xmf file. Exiting..."
    exit 1
elif [ ! -f "$IN_DIR/fort.63.nc" ]; then
    echo "Input directory is missing a fort.63.nc file. Exiting..."
    exit 1
elif [ ! -f "$IN_DIR/fort.63.nc.xmf" ]; then
    echo "Input directory is missing a fort.63.nc.xmf file. Exiting..."
    exit 1
fi

################################################################################
# STEP 1: GENERATE TEXT FILE WITH NETCDF HEADER INFORMATION                    #
################################################################################
# Generate label_info.txt file
# If a maxele and fort.63 are from the same advisory, 
# the results of label_info.txt should be the same for both
# Only need to do this for one of them, arbitrarily choosing fort.63

# Credit for this function goes to the NCO documentation
function ncattget { ncks --trd -M -m ${3} | grep -E -i "^${2} attribute [0-9]+: ${1}" | cut -f 11- -d ' ' | sort ; }

ncattget model global "$IN_DIR"/fort.63.nc > "$IN_DIR"/label_info.txt
{
    ncattget agrid global "$IN_DIR"/fort.63.nc 
    ncattget title global "$IN_DIR"/fort.63.nc 
    ncattget rundes global "$IN_DIR"/fort.63.nc 
    ncattget runid global "$IN_DIR"/fort.63.nc 
    ncattget units time "$IN_DIR"/fort.63.nc 
} >> "$IN_DIR"/label_info.txt

################################################################################
# STEP 2: GENERATE VISUALIZATION FROM MAXELE FILE                              #
################################################################################
# Run pvpython script to generate the maxele figure
if [ -z "$ZOOM_AREA" ] ; then
    echo "Zoom area not set, running 2D maxele figure script..."
    "$PV_DIR"/bin/pvpython "$SCRPT_DIR"/"$MAXELE_SCRPT" "$IN_DIR" \
        "$OUT_DIR" "$CMAP_DIR" "$ZETA_BND" "$C_EMAIL"
else
    echo "Running 3D maxele figure script for area" "$ZOOM_AREA""..."
    "$PV_DIR"/bin/pvpython "$SCRPT_DIR"/"$MAXELE_SCRPT" "$IN_DIR" \
        "$OUT_DIR" "$CMAP_DIR" "$ZETA_BND" "$ZOOM_AREA" "$C_EMAIL"
fi


################################################################################
# STEP 3: GENERATE ANIMATION (GIF) FROM FORT.63 FILE                           #
################################################################################
# Make a directory to store the frames
mkdir "$OUT_DIR"/anim-frames

# Run pvpython script to generate frames
if [ -z "$ZOOM_AREA" ] ; then
    echo "Zoom area not set, running 2D fort.63 animation script..."
    "$PV_DIR"/bin/pvpython "$SCRPT_DIR"/"$FORT63_SCRPT" "$IN_DIR" \
        "$OUT_DIR"/anim-frames "$CMAP_DIR" "$ZETA_BND" "$START_T" \
        "$FINAL_T" "$C_EMAIL"
else
    echo "Running 3D fort.63 animation script for area" "$ZOOM_AREA""..."
    "$PV_DIR"/bin/pvpython "$SCRPT_DIR"/"$FORT63_SCRPT" "$IN_DIR" \
        "$OUT_DIR"/anim-frames "$CMAP_DIR" "$ZETA_BND" "$START_T" \
        "$FINAL_T" "$ZOOM_AREA" "$C_EMAIL"
fi

# Generate a GIF from the frames using ffmpeg
# The resolution chosen here is 1/2 of the one used in the pvpython scripts
# Note that this will overwrite if you already have an animation file
echo "Generating GIF from fort.63 animation frames..."

if [ -z "$ZOOM_AREA" ] ; then
    ffmpeg -y -f image2 -framerate 10 -start_number "$START_T" \
        -i "$OUT_DIR"/anim-frames/latx_2D_frame.%04d.png \
        -loop 0 -vf "scale=725:389" "$OUT_DIR"/latx_2D_fort63_anim.gif \
        > "$OUT_DIR"/ffmpeg_log.txt 2>> "$OUT_DIR"/ffmpeg_log.txt
else
    ffmpeg -y -f image2 -framerate 10 -start_number "$START_T" \
        -i "$OUT_DIR"/anim-frames/latx_3D_frame.%04d.png \
        -loop 0 -vf "scale=725:389" "$OUT_DIR"/latx_3D_fort63_anim.gif \
        > "$OUT_DIR"/ffmpeg_log.txt 2>> "$OUT_DIR"/ffmpeg_log.txt
fi


################################################################################
# STEP 3: CLEAN UP TEMPORARY FILES                                             # 
################################################################################
if [ "$FILE_CLEAN" = true ] ; then
# Delete text file with ffmpeg command line output
    rm "$OUT_DIR"/ffmpeg_log.txt
# Delete animation frames and their directory
    rm -r "$OUT_DIR"/anim-frames
# Delete label_info.txt
    rm "$IN_DIR"/label_info.txt
fi
