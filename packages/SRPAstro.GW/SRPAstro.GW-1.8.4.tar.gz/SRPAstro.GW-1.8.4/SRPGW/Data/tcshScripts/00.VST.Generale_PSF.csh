#!/bin/csh -f
#
# 18/12/2017    V. 0.1.0
#
if ($#argv == 0) exit 1
#
echo "Arguments: " $argv
#
#set ppre = "p"
set ppre = ""
set fpre = "/data01/VSTin/GW170814"
set ocpth = "/data02/ownCloud/Shared/GWshare/ps"
set prepc = "01.VST.Preparazione_PSF.csh"
set anac = "02.VST.Analisi_PSF.csh"
set selc = "03.VST.Selezione_PSF.csh"
set mjdgw = "57979.437998"
set logprep = "logprep.txt"
set logana = "logana.txt"
set noglob
# Work dir
#
foreach p ($argv)
    echo "Pointing $ppre$p..."
    if !(-e $ppre$p"_psf") then
        mkdir $ppre$p"_psf"
    endif
    #
    cd $ppre$p"_psf"
    #
    cp ../$prepc .
    cp ../$anac .
    cp ../$selc .
    chmod u+x $prepc $anac $selc
    #
    set res = `find $fpre -name "*$ppre$p.fits" -print | sort `
    if ($#res > 0) then
        set strl = ""
        foreach f ($res)
            set strl = "$strl $f $f:r.flag.fits $f:r.rd"
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
        tar cvzf $ppre$p"_psf".tar.gz GWPics $logprep $logana Ep_all_13.tab Ep_all_14.tab
        mv $ppre$p"_psf".tar.gz $ocpth
    endif
    #
    cd ..
end
#


