#!/bin/csh -f
#
# 05/07/2019    V. 0.2.2
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
set ppre = ""
set fpre = "/data01/VSTin/s190510g"
set ocpth = "/gdrive/Data/phot-pipe/VST"
set prepc = "01.VST.Preparazione_1epoch.csh"
set anac = "02.VST.Analisi_1epoch.csh"
set selc = "03.VST.Selezione_1epoch.csh"
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
            set strl = "$strl $f $f:r.flag.fits"
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
        tar cvzf $ppre$p:r.tar.gz $logprep $logana Ep_all_6.vo Ep_all_9.vo Ep_all_10.vo Ep_all_6.skycat Ep_all_9.skycat Ep_all_10.skycat Ep_all_6.fits Ep_all_9.fits Ep_all_10.fits
        mv $ppre$p:r.tar.gz $ocpth
    endif
    #
    cd ..
end
#


