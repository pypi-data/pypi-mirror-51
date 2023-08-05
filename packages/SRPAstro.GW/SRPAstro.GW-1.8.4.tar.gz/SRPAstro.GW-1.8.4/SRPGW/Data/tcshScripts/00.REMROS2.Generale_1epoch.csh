#!/bin/csh -f
#
# 27/04/2019    V. 0.1.0
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
#set ppre = "p"
set ppre = ""
set fpre = "/Users/covino/Desktop"
set ocpth = "."
set prepc = "01.REMROS2.Preparazione_1epoch.csh"
set anac = "02.REMROS2.Analisi_1epoch.csh"
set selc = "03.REMROS2.Selezione_1epoch.csh"
set mjdgw = "57979.437998"
set logprep = "logprep.txt"
set logana = "logana.txt"
set noglob
# Work dir
#
foreach p ($argv)
    echo "Field $ppre$p..."
    if !(-e $ppre$p:r) then
        mkdir $ppre$p:r
    endif
    #
    cd $ppre$p:r
    #
    cp ../$prepc .
    cp ../$anac .
    cp ../$selc .
    chmod u+x $prepc $anac $selc
    #
    set res = `find $fpre -name "$ppre$p" -print `
    if ($#res > 0) then
        set strl = ""
        foreach f ($res)
            set strl = "$strl $f"
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
        tar cvzf $ppre$p:r.tar.gz $logprep $logana Ep_all_7.tab Ep_all_10.tab
        mv $ppre$p:r.tar.gz $ocpth
    endif
    #
    cd ..
end
#


