#!/bin/csh -f
#
# 29/04/2019    V. 0.3.1
#
# .1, fits
#
if ($#argv != 2) exit 1
#
echo "Arguments: " $argv
set outtab = SumResults.tab
#set cvsdir = "/data02/roma/csv"
set mjdgw = "57382.152002"
#
set noglob
#
# Selection
set cmd = "SRPGWCandSelect -v -i $1 -r $outtab -n $2 -m $mjdgw"
echo $cmd
eval $cmd
#
# Skycat
if -e $outtab then
    set cmd = "SRPGWTabViewer -v -i $outtab -S"
    echo $cmd
    eval $cmd
endif
#
# csv and light curves
#if -e $outtab:r_1.tab then
#    set cmd = "SRPGWCandSelect -i $outtab:r_1.tab -r $outtab:r_1.tab -l"
#    echo $cmd
#    eval $cmd
#endif
#
# copy csv
#set p = `pwd`
#set pp = `echo $p | tr '/' ' '`
#cp $outtab:r.csv $cvsdir/$pp[$#pp].csv
#
