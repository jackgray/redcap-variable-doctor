#!/bin/env bash

# VERSION='1.0.0'
# appname=redcap_variable_doctor

#Usage message to display
usage() {
  cat <<EOF
  
EQUALIZE VARIABLE NAMES

usage: $0 [ -d directory ] [ -s separator ]

Where -d directory contains your config files and instrument zip file(s)

The following files are required and should be in the directory supplied: \
<Instrument downloaded from redcap>.zip 
changemaps.json 

Optionally, you may provide:
preChangemaps.json 
postChangemaps.json

to perform find replace changes on the entire variable name before and/or after they are split by underscores and rearranged according to changemaps.json. 

This script will generate a find/replace change plan and apply it to all instrument zip files it detects, generating a new zip file with the desired changes for each one, which you can upload into redcap's project designer.
EOF
}

# Ensure minimum args are supplied
if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

# Read command arguments
while [ "$1" != "" ]; do
    case $1 in
        -d )
            shift
            dir=$1
            ;;
        -s )
            shift
            separator=$1
            ;;
        -h | --help )
            usage
            exit
            ;;
        * )
            usage
            exit 1
    esac
    shift
done

############################## CONTAINER SETUP #################################
image="jackgray/${appname}:${VERSION}"

# Set defaults if flags are omitted
if [ -z "${dir}" ]; then
  dir="${HOME}/Downloads"
  echo -e "\nUsing $dir for directory"
fi

# UID and GID
uid=$(id -u)  # UID of person running this script for permission-fixing | could be set with config file
printf "\nUsing UID ${uid}"
TOF=$(date +"%Ih%M%p")  # hour-minute time in docker & unix acceptable format | ex: 01h15pm
printf "\nSet container time of flight as ${TOF}"

#----------SERVICE NAME---------------
service_name="${appname}_$(id -un)_${TOF}"
#-------------------------------------

#- - - - - - - - - - - - - - - - DOCKER APP - - -- - - - - - - - - - - - - - - - - - -- - - - - - - -
run() {
  docker run \
  -v "${dir}:/input" \
  -e INPUT_DIR="/input"
  -e SEPARATOR="$separator" \
  -it \
  --name "${service_name}" \
  "${image}" 
}
