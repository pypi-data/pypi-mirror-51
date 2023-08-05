#!/bin/csh -f
#
# 27/04/2019    V. 0.1.0
#
if ($#argv == 0) exit 1
#
# .1, flags
# .2, roundness
# .3, peaky
# .4, FWHM
# .5, saturation
#
echo "Arguments: " $argv
#
set rt = "Ep"
set pixsize = 0.6
set FW = 8.
set SATUR = 62000
set noglob
#
# Source detection
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n.cat) then
        set cmd = "SRPGWSourceFinder -v -i $argv[$f] -o $rt$n.cat -f $FW -s -c -t 1.4"
        echo $cmd
        eval $cmd
    endif
end
#
# Table conversion
set m = 0
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    @ m = $m + 2
    if !(-e $rt$n.tab) then
        set cmd = "SRPGWImportCats -v -i $rt$n.cat -o $rt$n.tab -f $argv[$f] -I REMROS2"
        echo $cmd
        eval $cmd
    endif
end
#
# Flags
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
if !(-e $rt$n:r_1.tab) then
        set cmd = "SRPGWSelect -v -i $rt$n.tab -s '(( flag != 16) & ( flag != 4))' -o $rt$n:r_1.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# Saturation
set n = 0
    foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_2.tab) then
        set cmd = "SRPGWSelect -v -i $rt$n:r_1.tab -s ' peak < $SATUR ' -o $rt$n:r_2.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# computation table
set n = 0
	foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n.temp) then
    	set cmd = "SRPGWStat -i $rt$n:r_2.tab -c flux"
    	echo $cmd
    	set res = `$cmd`
        set cmd = "SRPGWSelect -i $rt$n:r_2.tab -o $rt$n.temp -s ' :flux >= $res[7]' "
        echo $cmd
        eval $cmd
    endif
end
#
# Roundness
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_3.tab) then
        set cmd = "SRPGWStat -i $rt$n.temp -c xy"
        echo $cmd
        set res = `$cmd`
        set xymin = `echo "scale=2;$res[1]-3*$res[2]" | bc `
        set xymax = `echo "scale=2;$res[1]+3*$res[2]" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_2.tab -s '(( xy >= $xymin) & ( xy <= $xymax))' -o $rt$n:r_3.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# peaky
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_4.tab) then
        set cmd = "SRPGWCalc -i $rt$n:r_3.tab -o $rt$n:r_3.tab -c ':peaky = peak / npix '"
        echo $cmd
        eval $cmd
        set cmd = "SRPGWCalc -i $rt$n.temp -o $rt$n.temp -c ':peaky = peak / npix '"
        echo $cmd
        eval $cmd
        set cmd = "SRPGWStat -i $rt$n.temp -c peaky"
        echo $cmd
        set res = `$cmd`
        set shmax = `echo "scale=2;$res[1]+3*$res[2]" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_3.tab -s '( peaky <= $shmax)' -o $rt$n:r_4.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# fwhm
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_5.tab) then
        set cmd = "SRPGWStat -i $rt$n.temp -c FWHM_IMAGE"
        echo $cmd
        set res = `$cmd`
        set shmin = `echo "scale=2;$res[1]-3*$res[2]" | bc `
        set shmax = `echo "scale=2;$res[1]+3*$res[2]" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_4.tab -s '(( FWHM_IMAGE >= $shmin) & ( FWHM_IMAGE <= $shmax))' -o $rt$n:r_5.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# remove computation table
set n = 0
    foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if (-e $rt$n.temp) then
        rm $rt$n.temp
    endif
end
#
# Command line
set n = 0
set strl = "./02.REMROS2.Analisi_1epoch.csh "
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    set strl = "$strl $rt$n:r_5.tab "
end
echo $strl
#


