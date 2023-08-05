#!/bin/csh -f
#
# 03/05/2017    V. 0.2.0
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
set pixsize = 1.0291
set satlevel = 62000
set noglob
# Frame pic
#
# Source detection
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n.cat) then
        set cmd = "SRPFitsHeaders -f $argv[$f] -k SEEPIX"
        echo $cmd
        set res = `$cmd`
        set FW = `echo "scale=2;$res[2]" | bc `
        set cmd = "SRPGWSourceFinder -v -i $argv[$f] -o $rt$n.cat -f $FW -s -c -t 3"
        echo $cmd
        eval $cmd
    endif
end
#
# Table conversion
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n.tab) then
        set cmd = "SRPGWImportCats -v -i $rt$n.cat -o $rt$n.tab -f $argv[$f] -I CNEOST"
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
# Roundness
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_2.tab) then
        set cmd = "SRPGWStat -i $rt$n:r_1.tab -c xy"
        echo $cmd
        set res = `$cmd`
        set xymin = `echo "scale=2;$res[1]-3*$res[2]" | bc `
        set xymax = `echo "scale=2;$res[1]+3*$res[2]" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_1.tab -s '(( xy >= $xymin) & ( xy <= $xymax))' -o $rt$n:r_2.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# peaky
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_3.tab) then
        set cmd = "SRPGWCalc -i $rt$n:r_2.tab -o $rt$n:r_2.tab -c ':peaky = peak / npix '"
        echo $cmd
        eval $cmd
        set cmd = "SRPGWStat -i $rt$n:r_2.tab -c peaky"
        echo $cmd
        set res = `$cmd`
        set shmax = `echo "scale=2;$res[3]*3" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_2.tab -s '( peaky <= $shmax)' -o $rt$n:r_3.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# fwhm
set n = 0
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_4.tab) then
        set cmd = "SRPGWStat -i $rt$n:r_3.tab -c FWHM_IMAGE"
        echo $cmd
        set res = `$cmd`
        set shmin = `echo "scale=2;$res[1]-3*$res[2]" | bc `
        set shmax = `echo "scale=2;$res[1]+3*$res[2]" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_3.tab -s '(( FWHM_IMAGE >= $shmin) & ( FWHM_IMAGE <= $shmax))' -o $rt$n:r_4.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# Saturation
set n = 0
    foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_5.tab) then
        set cmd = "SRPGWSelect -v -i $rt$n:r_4.tab -s ' peak < $satlevel ' -o $rt$n:r_5.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# Command line
set n = 0
set strl = "./02.CNEOST.Analisi.csh "
foreach f (`seq 1 1 $#argv`)
    @ n = $n + 1
    set strl = "$strl $rt$n:r_5.tab "
end
echo $strl
#


