#!/bin/bash

# Define variables
DOCKER_CONTAINER="ft42_g6xai"
PYTHON_SCRIPT="/NAS/shared_data/for_VNLST/ft42/DukeLungRads_Dir/resample_images.py"
INPUT_FOLDER="/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest_nifti_ct"
OUTPUT_FOLDER="/NAS/shared_data/for_VNLST/ft42/ct_public/unitochest/unitochest_nifti_ct_resampled"
SPACING="0.703125 0.703125 1.25"
START=0
END=715
EXTENSION=".nii.gz"

# Run the Docker command
docker exec -it "$DOCKER_CONTAINER" bash -c "python $PYTHON_SCRIPT $INPUT_FOLDER $OUTPUT_FOLDER --spacing $SPACING --start $START --end $END --extension $EXTENSION"