#!/bin/csh -f
#
# 29/04/2019    V. 0.3.0
#
# .1, date, pixel
# .2, fwhm
# .3, xy selection
# .4, magnitude
# .5, mag normalization
# .6, neighbor
# .7, gaia, simbad, leda, usno & score
# .8, mag and score selection
# .9, selection
# .10, minor planets.
# .11, psf magnitude
# .12, psf mag selection
# .13, pictures
# .14, select no minor planets
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
set rt = Ep_all.tab
set aptool = dao
set aprad = "7 10 15"
set naxis = 4096
set magthreshold = 5
set scothreshold = 5
set varindexthreshold = 5
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
	set cmd = "SRPGWUnionMatch -v -i $strl -r 1.5 -o $rt -I CIMP"
    echo $cmd
    eval $cmd
endif
#
# Date, pixel information
if !(-e $rt:r_1.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r.tab -D -x -o $rt:r_1.tab"
    echo $cmd
    eval $cmd
endif
#
# Fwhm information
if !(-e $rt:r_2.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_1.tab -F 20 -o $rt:r_2.tab"
    echo $cmd
    eval $cmd
endif
#
set n = 0
set strl = "'( "
foreach f ($argv)
    @ n = $n + 1
    set strl = "$strl ( X_IMAGE_$n > 1.0 ) & ( X_IMAGE_$n <= $naxis ) & ( Y_IMAGE_$n > 1.0 ) & ( Y_IMAGE_$n <= $naxis ) & ( FWHM_IMAGE_$n > 0)"
    if ! ($n == $#argv) then
        set strl = "$strl & "
    endif
end
set strl = "$strl )'"
#
# XY and FWHM selection
if !(-e $rt:r_3.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_2.tab -s $strl -o $rt:r_3.tab"
    echo $cmd
    eval $cmd
endif
#
# Magnitudes
if !(-e $rt:r_4.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_3.tab -a -o $rt:r_4.tab -A $aptool -r $aprad"
    echo $cmd
    eval $cmd
endif
#
# Calibration
if !(-e $rt:r_5.tab) then
    set cmd = "SRPGWMagNormVar -v -i $rt:r_4.tab -o $rt:r_5.tab"
    echo $cmd
    eval $cmd
endif
#
# Neighborhood
if !(-e $rt:r_6.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_5.tab -n $rt:r_5.tab -o $rt:r_6.tab"
    echo $cmd
    eval $cmd
endif
#
# GAIA, Simbad, Leda & Score
if !(-e $rt:r_7.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -o $rt:r_7.tab -g 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_7.tab -s 5"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_7.tab -l 60.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_7.tab -G 60.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_7.tab -u 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_7.tab -S"
    echo $cmd
    eval $cmd
endif
#
# Magnitude, score, varindices selection
if !(-e $rt:r_8.tab) then
    set cmd = "SRPGWAdaptSelect -v -i $rt:r_7.tab -o $rt:r_8.tab -M -m $magthreshold -C -S -s $scothreshold -n 500 -X -x $varindexthreshold"
    echo $cmd
    eval $cmd
endif
#
# GAIA selection
if !(-e $rt:r_9.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_8.tab -o $rt:r_9.tab -s "'"( GAIA == -99 )"'""
    echo $cmd
    eval $cmd
endif
#
# Minor planets
if !(-e $rt:r_10.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_9.tab -o $rt:r_10.tab -m 30"
    echo $cmd
    eval $cmd
endif
#
# PSF magnitudes
if !(-e $rt:r_11.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_10.tab -o $rt:r_11.tab -p $rt:r_6.tab -r $aprad -A $aptool"
    echo $cmd
    eval $cmd
endif
# PSF Magnitude and score selection
if !(-e $rt:r_12.tab) then
    set cmd = "SRPGWAdaptSelect -v -i $rt:r_11.tab -o $rt:r_12.tab -M -G -S -c PSFMAG ePSFMAG"
    echo $cmd
    eval $cmd
endif
#
# Picture drawing
if !(-e $rt:r_13.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_12.tab -o $rt:r_13.tab -j"
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
if !(-e $rt:r_14.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_13.tab -s $strl -o $rt:r_14.tab"
    echo $cmd
    eval $cmd
endif
#
echo "./03.CIMP.Selezione.csh $rt:r_7.tab $rt:r_14.tab"

