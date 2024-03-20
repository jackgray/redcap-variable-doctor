EQUALIZE VARIABLE NAMES

This script will generate a find/replace change plan and apply it to all files in exported redcap project zip archives it detects, generating a new zip file with the desired changes for each one, which you can upload into redcap's project designer.


usage: bash run.sh [ -d directory ] [ -s separator ]
Where -d directory contains your config files and instrument zip file(s) and -s separator is the character you want to split your variable names by

example: bash run.sh -d ~/Downloads/redcap-test -s '_'

The following files are required and should be in the directory supplied: \
<Instrument downloaded from redcap>.zip 
changemaps.json 

Optionally, you may provide:
preChangemaps.json 
postChangemaps.json

to perform find replace changes on the entire variable name before and/or after they are split and rearranged according to changemaps.json. 


