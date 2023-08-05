#!/bin/csh -f
#
# 26/08/2019    V. 0.2.1
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
#set ppre = "p"
set ppre = ""
set fpre = "/data01/VSTin/S190728q"
set extref = "/data03/padova/S190728q/PS1"
set ocpth = "/gdrive/Data/phot-pipe/VST"
set prepc = "01.VST.Preparazione.csh"
set anac = "02.VST.Analisi.csh"
set selc = "03.VST.Selezione.csh"
set mjdgw = "57382.152002"
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
    set res = `find $fpre -name "*$ppre$p*p0.fits" -print | sort `
    set resext = `find $extref -name "*$ppre$p*p0.fits" -print | sort `
    if ($#res > 0) then
        set strl = ""
        foreach f ($res)
            set strl = "$strl $f $f:r.flag.fits"
        end
        foreach f ($resext)
            set strl = "$strl $f $f:r.bpm.fits"
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
        tar cvzf $ppre$p.tar.gz GWPics $logprep $logana Ep_all_8.tab Ep_all_15.tab Ep_all_8.vo Ep_all_15.vo Ep_all_8.skycat Ep_all_15.skycat
        mv $ppre$p.tar.gz $ocpth
    endif
    #
    cd ..
end
#


