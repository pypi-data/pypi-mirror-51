#!/bin/csh -f
#
# 05/07/2019    V. 0.3.0
#
# .1, weight, weightarea
# .2, weight selection
# .3, date, pixel
# .4, fwhm
# .5, magnitude
# .6, mag normalization
# .7, neighbor
# .8, gaia, simbad, leda, usno & score
# .9, catalogue selection
# .10, minor planets.
# .11, Bright magnitude
# .12, pictures
# .13, select no minor planets
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
set rt = Ep_all.tab
set aptool = apy
set aprad = "5 5 8"
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
# GAIA, Simbad, Leda & Score
if !(-e $rt:r_6.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_5.tab -o $rt:r_6.tab -g 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -o $rt:r_6.tab -s 2.0"
    echo $cmd
    eval $cmd
    set cmd = "SRPGWQuery -v -i $rt:r_6.tab -o $rt:r_6.tab -u 2.0"
    echo $cmd
    eval $cmd
endif
#
# GAIA selection
if !(-e $rt:r_7.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_6.tab -o $rt:r_7.tab -s "'"( GAIA == -99 )"'""
    echo $cmd
    eval $cmd
endif
#
# Minor planets
if !(-e $rt:r_8.tab) then
    set cmd = "SRPGWQuery -v -i $rt:r_7.tab -o $rt:r_8.tab -m 30"
    echo $cmd
    eval $cmd
endif
#
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
if !(-e $rt:r_9.tab) then
    set cmd = "SRPGWSelect -v -i $rt:r_8.tab -s $strl -o $rt:r_9.tab"
    echo $cmd
    eval $cmd
endif
#
# USNO selection
    if !(-e $rt:r_10.tab) then
        set cmd = "SRPGWSelect -v -i $rt:r_9.tab -o $rt:r_10.tab -s "'"( USNO == '"'No'"' )"'""
        echo $cmd
        eval $cmd
endif
#
# Add ASRPMAG column
set cmd = "SRPGWCalc -v -i $rt:r_10.tab -o $rt:r_10.tab -c ' :ASRPMAG = SRPMAG_1 '"
echo $cmd
eval $cmd
#
echo "./03.VST.Selezione_1epoch.csh $rt:r_6.tab $rt:r_9.tab $rt:r_10.tab"

