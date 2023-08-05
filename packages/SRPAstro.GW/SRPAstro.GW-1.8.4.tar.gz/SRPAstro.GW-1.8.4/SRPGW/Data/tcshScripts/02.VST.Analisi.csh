#!/bin/csh -f
#
# 28/04/2019    V. 1.5.3
#
# .1, weight, weightarea
# .2, weight selection
# .3, date, pixel
# .4, fwhm
# .5, magnitude
# .6, mag normalization
# .7, neighbor
# .8, gaia, simbad, leda, usno & score
# .9, mag and score selection
# .10, catalogue selection
# .11, minor planets.
# .12, psf magnitude
# .13, psf mag selection
# .14, pictures
# .15, select no minor planets
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
set rt = Ep_all.tab
set aptool = dao
set aprad = "5 5 8"
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
	set cmd = "SRPGWUnionMatch -v -i $strl -r 0.5 -o $rt"
    echo $cmd
    eval $cmd
endif
#
# Weights, weightareas information
if !(-e $rt:r_1.tab) then
    set cmd = "SRPGWQuery -v -i $rt -w -W 15 0.0 -o $rt:r_1.tab"
    echo $cmd
    eval $cmd
    set n = 0
    foreach f ($argv)
        @ n = $n + 1
        set cmd = "SRPGWCalc -v -i $rt:r_1.tab -o $rt:r_1.tab -c ' :GoodData_$n = Weight_$n == 2'"
        echo $cmd
        eval $cmd
    end
endif
#
set n = 0
set strl = "'( "
foreach f ($argv)
    @ n = $n + 1
    set strl = "$strl ( WeightArea_$n > 0.0) & ( WeightArea_$n <= 2.0 ) "
    if ! ($n == $#argv) then
        set strl = "$strl & "
    endif
end
set strl = "$strl )'"
#
# Weight selection
if !(-e $rt:r_2.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_1.tab -s $strl -o $rt:r_2.tab"
    echo $cmd
    eval $cmd
endif
#
# Date, pixel information
if !(-e $rt:r_3.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_2.tab -D -x -o $rt:r_3.tab"
    echo $cmd
    eval $cmd
endif
#
# Fwhm information
if !(-e $rt:r_4.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_3.tab -F 20 -o $rt:r_4.tab"
    echo $cmd
    eval $cmd
endif
#
# Magnitudes
if !(-e $rt:r_5.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_4.tab -a -o $rt:r_5.tab -A $aptool -r $aprad"
    echo $cmd
    eval $cmd
endif
#
# Calibration
if !(-e $rt:r_6.tab) then
    set cmd = "SRPGWMagNormVar -v -i $rt:r_5.tab -o $rt:r_6.tab -G"
    echo $cmd
    eval $cmd
endif
#
# Neighborhood
if !(-e $rt:r_7.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -n $rt:r_6.tab -o $rt:r_7.tab"
    echo $cmd
    eval $cmd
endif
#
# GAIA, Simbad, Leda & Score
if !(-e $rt:r_8.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_8.tab -g 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_8.tab -o $rt:r_8.tab -s 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_8.tab -o $rt:r_8.tab -l 60.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_8.tab -o $rt:r_8.tab -G 60.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_8.tab -o $rt:r_8.tab -u 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_8.tab -o $rt:r_8.tab -S"
    echo $cmd
    eval $cmd
endif
#
# Magnitude, score, varindices selection
if !(-e $rt:r_9.tab) then
    set cmd = "SRPGWAdaptSelect -v -i $rt:r_8.tab -o $rt:r_9.tab -M -m $magthreshold -C -G -S -s $scothreshold -X -x $varindexthreshold"
    echo $cmd
    eval $cmd
endif
#
# GAIA selection
if !(-e $rt:r_10.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_9.tab -o $rt:r_10.tab -s "'"( GAIA == -99 )"'""
    echo $cmd
    eval $cmd
endif
#
# Minor planets
if !(-e $rt:r_11.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_10.tab -o $rt:r_11.tab -m 30"
    echo $cmd
    eval $cmd
endif
#
# PSF magnitudes
if !(-e $rt:r_12.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_11.tab -o $rt:r_12.tab -p $rt:r_7.tab -r $aprad -A $aptool"
    echo $cmd
    eval $cmd
endif
# PSF Magnitude and score selection
if !(-e $rt:r_13.tab) then
    set cmd = "SRPGWAdaptSelect -v -i $rt:r_12.tab -o $rt:r_13.tab -M -G -S -c PSFMAG ePSFMAG"
    echo $cmd
    eval $cmd
endif
#
# Picture drawing
if !(-e $rt:r_14.tab) then
    set cmd = "SRPGWAnalysis -v -i $rt:r_13.tab -o $rt:r_14.tab -j"
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
if !(-e $rt:r_15.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_14.tab -s $strl -o $rt:r_15.tab"
    echo $cmd
    eval $cmd
endif
#
echo "./03.VST.Selezione.csh $rt:r_8.tab $rt:r_15.tab"

