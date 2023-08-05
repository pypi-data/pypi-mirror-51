#!/bin/csh -f
#
# 27/04/2019    V. 0.1.0
#
# .1, date, pixel
# .2, fwhm
# .3, xy & fw
# .4, magnitude
# .5, mag normalization
# .6, gaia, simbad, leda, glade, usno & score
# .7, catalogue selection
# .8, minor planets.
# .9, Bright magnitude
# .10, select no minor planets
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
set rt = Ep_all.tab
set aptool = apy
set aprad = "6 10 15"
set naxis = 1024
#
set noglob
#
# Command line
set strl = ""
foreach f ($argv)
	set strl = "$strl $f "
end
#
# Union match
if !(-e $rt) then
	set cmd = "SRPGWUnionMatch -v -i $strl -r 1.5 -o $rt -I REMROS2"
    echo $cmd
    eval $cmd
endif
#
# Date, pixel information
if !(-e $rt:r_1.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r.tab -D -H DATE-OBS -x -o $rt:r_1.tab"
    echo $cmd
    eval $cmd
endif
#
# Fwhm information
if !(-e $rt:r_2.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_1.tab -F 15 -o $rt:r_2.tab"
    echo $cmd
    eval $cmd
endif
#
# Magnitudes
if !(-e $rt:r_3.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_2.tab -a -o $rt:r_3.tab -A $aptool -r $aprad"
    echo $cmd
    eval $cmd
endif
#
# GAIA, Simbad, Leda & Score
if !(-e $rt:r_4.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_3.tab -o $rt:r_4.tab -g 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_4.tab -o $rt:r_4.tab -s 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_4.tab -o $rt:r_4.tab -u 2.0"
    echo $cmd
    eval $cmd
endif
#
# GAIA selection
if !(-e $rt:r_5.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_4.tab -o $rt:r_5.tab -s "'"( GAIA == -99 )"'""
    echo $cmd
    eval $cmd
endif
#
# Minor planets
if !(-e $rt:r_6.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_5.tab -o $rt:r_6.tab -m 30"
    echo $cmd
    eval $cmd
endif
#
set n = 0
set strl = "'( "
foreach f ($argv)
    @ n = $n + 1
    set strl = "$strl ( MinorPlanet_$n == "'"No"'") "
    if ! ($n == $#argv) then
        set strl = "$strl & "
    endif
end
set strl = "$strl )'"
#
# Minor planet selection
if !(-e $rt:r_7.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_6.tab -s $strl -o $rt:r_7.tab"
    echo $cmd
    eval $cmd
endif
#
echo "./03.REMROS2.Selezione_1epoch.csh $rt:r_4.tab $rt:r_7.tab"

