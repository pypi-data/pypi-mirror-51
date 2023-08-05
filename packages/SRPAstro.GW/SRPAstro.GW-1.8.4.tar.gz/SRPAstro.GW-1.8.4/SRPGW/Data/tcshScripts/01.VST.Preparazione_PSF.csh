#!/bin/csh -f
#
# 19/12/2017    V. 0.1.0
#
if ($#argv == 0) exit 1
#
#
echo "Arguments: " $argv
#
set rt = "Ep"
set fc = "FindingChart.png"
set pixsize = 0.21
set noglob
#
#
#Import cat creation
echo "NR" > inpcat.cat
echo "X_WORLD" >> inpcat.cat
echo "Y_WORLD" >> inpcat.cat
echo "X_IMAGE" >> inpcat.cat
echo "Y_IMAGE" >> inpcat.cat
echo "PSFMAG" >> inpcat.cat
echo "ePSFMAG" >> inpcat.cat
echo "CHI2" >> inpcat.cat
echo "SHARP" >> inpcat.cat
# Table conversion
set n = 0
foreach f (`seq 1 3 $#argv`)
    @ n = $n + 1
    @ m = $f + 1
    @ l = $f + 2
    #
    set ff = `basename $argv[$l]`
    echo $ff
    tail -n +4 $argv[$l] > $ff
    #
    if !(-e $rt$n.tab) then
        set cmd = "SRPGWImportCats -v -i $ff -o $rt$n.tab -f $argv[$f] -w $argv[$m] -p inpcat.cat"
        echo $cmd
        eval $cmd
        if -e $ff then
            rm $ff
        endif
    endif
end
#
if -e inpcat.cat then
    rm inpcat.cat
endif
#
# zero-point
set n = 0
foreach f (`seq 1 3 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_1.tab) then
        set cmd = "SRPGWCalc -v -i $rt$n.tab -o $rt$n:r_1.tab -c ' PSFMAG = PSFMAG + 5.0 ' "
        echo $cmd
        eval $cmd
    endif
end
#
# sharp
set n = 0
foreach f (`seq 1 3 $#argv`)
    @ n = $n + 1
    if !(-e $rt$n:r_2.tab) then
        set cmd = "SRPGWStat -i $rt$n:r_1.tab -c SHARP "
        echo $cmd
        set res = `$cmd`
        set smin = `echo "scale=2;$res[3]-$res[2]" | bc `
        set smax = `echo "scale=2;$res[3]+$res[2]" | bc `
        set cmd = "SRPGWSelect -v -i $rt$n:r_1.tab -s '(( SHARP >= $smin) & ( SHARP <= $smax))' -o $rt$n:r_2.tab"
        echo $cmd
        eval $cmd
    endif
end
#
# Command line
set n = 0
set strl = "./02.VST.Analisi_PSF.csh "
foreach f (`seq 1 3 $#argv`)
    @ n = $n + 1
set strl = "$strl $rt$n:r_2.tab "
end
echo $strl
#


