#!/bin/csh -f
#
# 29/04/2019    V. 0.2.0
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
set ppre = ""
set fpre = "/data01/CIin/GW20170225"
set ocpth = "/data02/ownCloud/Shared/GWshare/ps"
set prepc = "01.CIMP.Preparazione_1epoch.csh"
set anac = "02.CIMP.Analisi_1epoch.csh"
set selc = "03.CIMP.Selezione_1epoch.csh"
set mjdgw = "57912.084219"
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
    set res = `ls $fpre/"$ppre$p"`
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
        tar cvzf $ppre$p:r.tar.gz $logprep $logana Ep_all_4.vo Ep_all_7.vo Ep_all_4.skycat Ep_all_7.skycat
        mv $ppre$p:r.tar.gz $ocpth
    endif
    #
    cd ..
end
#


