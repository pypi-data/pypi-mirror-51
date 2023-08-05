#!/bin/csh -f
#
# 15/07/2016    V. 0.3.0
#
# .1, date, pixel, fwhm
# .2 xy seletion
# .3, magnitude
# .4, mag normalization
# .5, neighbor
# .6, igaia, simbad, leda & score
# .7, igaia selection
# .8, mag and score selection
# .9, minor planets.
# .10, psf magnitude
# .11, pictures
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
set rt = Ep_all.tab
set aptool = dao
set aprad = "5 5 8"
set naxis = 10560
set magthreshold = 5
set scothreshold = 5
#
set noglob
#
# Check SRPGW version
set cmd = "SRPGWVersion"
echo $cmd
set res = `$cmd`
set Vers = `echo $res | cut -d . -f 1`
if ($Vers != 1) then
    echo "Wrong SRP.GW version"
    exit
endif
#
# Command line
set strl = ""
foreach f ($argv)
	set strl = "$strl $f "
end
#
# Union match
if !(-e $rt) then
	set cmd = "SRPGWUnionMatch -v -i $strl -r 0.5 -o $rt -I CNEOST -r 1"
    echo $cmd
    eval $cmd
endif
#
# Date, pixel, fwhm information
if !(-e $rt:r_1.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r.tab -F -D -x -o $rt:r_1.tab -H SEEPIX DATE-OBS"
    echo $cmd
    eval $cmd
endif
#
set n = 0
set strl = "'( "
foreach f ($argv)
    @ n = $n + 1
    set strl = "$strl ( X_IMAGE_$n >= 0.0 ) & ( X_IMAGE_$n <= $naxis ) & ( Y_IMAGE_$n >= 0.0 ) & ( Y_IMAGE_$n <= $naxis )"
    if ! ($n == $#argv) then
        set strl = "$strl & "
    endif
end
set strl = "$strl )'"
#
# XY selection
if !(-e $rt:r_2.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_1.tab -s $strl -o $rt:r_2.tab"
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
# Calibration
if !(-e $rt:r_4.tab) then
    set cmd = "SRPGWMagNorm -v -i $rt:r_3.tab -o $rt:r_4.tab"
    echo $cmd
    eval $cmd
endif
#
# Neighborhood
if !(-e $rt:r_5.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_4.tab -n $rt:r_4.tab -o $rt:r_5.tab"
    echo $cmd
    eval $cmd
endif
#
# IGAIA, Simbad, Leda & score
if !(-e $rt:r_6.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_5.tab -o $rt:r_6.tab -g 0.5"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -o $rt:r_6.tab -s 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -o $rt:r_6.tab -l 60.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -o $rt:r_6.tab -S"
    echo $cmd
    eval $cmd
endif
#
# IGAIA & Simbad selection
if !(-e $rt:r_7.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_6.tab -o $rt:r_7.tab -s "'"( GAIA == -99 ) | ( Simbad != '"'No'"' )"'""
    echo $cmd
    eval $cmd
endif
#
# Magnitude and score selection
if !(-e $rt:r_8.tab) then
    set cmd = "SRPGWAdaptSelect -v -i $rt:r_7.tab -o $rt:r_8.tab -M -m $magthreshold -C -G -S -s $scothreshold"
    echo $cmd
    eval $cmd
endif
# Minor planets
if !(-e $rt:r_9.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_8.tab -o $rt:r_9.tab -m 30"
    echo $cmd
    eval $cmd
endif
#
# PSF magnitudes
if !(-e $rt:r_10.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_9.tab -o $rt:r_10.tab -p $rt:r_5.tab -r $aprad"
    echo $cmd
    eval $cmd
endif
#
# Picture drawing
if !(-e $rt:r_11.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_10.tab -o $rt:r_11.tab -j"
    echo $cmd
    eval $cmd
endif
#
echo "SRPGWCandSelect -v -i $rt:r_11.tab -r SumResults.tab"

