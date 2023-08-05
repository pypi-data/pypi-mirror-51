#!/bin/csh -f
#
# 29/04/2019    V. 0.2.0
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
set ppre = ""
set fpre = "/Users/covino/GINAF/Lab/REM/Cagliari/FRBz"
set ocpth = "."
set prepc = "01.Marcon.Preparazione.csh"
set anac = "02.Marcon.Analisi.csh"
set selc = "03.Marcon.Selezione.csh"
set logprep = "logprep.txt"
set logana = "logana.txt"
set noglob
# Work dir
#
foreach p ($argv)
    echo "Pointing $ppre$p..."
    if !(-e $ppre$p) then
        mkdir $ppre$p
    endif
    #
    cd $ppre$p
    #
    cp ../$prepc .
    cp ../$anac .
    cp ../$selc .
    chmod u+x $prepc $anac $selc
    #
    set res = `find $fpre -name "$ppre$p*.fit" -print | sort `
    if ($#res > 0) then
        set strl = ""
        foreach f ($res)
            set strl = "$strl $f "
        end
        #
        set cmd = "./$prepc $strl"
        echo $cmd
        $cmd >> $logprep
        #
        set anacmd = `tail -1 $logprep`
        echo $anacmd
        $anacmd >> $logana
        #
        set selcmd = `tail -1 $logana`
        echo $selcmd
        $selcmd
        #
        tar cvzf $ppre$p.tar.gz GWPics $logprep $logana Ep_all_13.tab Ep_all_14.tab
        #
    endif
    #
    cd ..
end
#


