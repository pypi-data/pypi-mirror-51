#!/bin/csh -f
#
# 27/04/2019    V. 0.1.0
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
set noglob
#
foreach p ($argv)
    # skyoutput
    set cmd = "SRPGWTabViewer -v -i $p -S"
    echo $cmd
    eval $cmd
	# votable
	set cmd = "SRPGWTabViewer -v -i $p -V"
	echo $cmd
	eval $cmd
end
#
#
