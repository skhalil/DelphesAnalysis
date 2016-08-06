#!/bin/python
import sys, os
from ROOT import TH1D,TFile, TIter, TFileIter, TKey, TObject

import subprocess

#suffix = '_sig'

options = [
   ['hEff',          '1', '0'],
   ['hLepIso',       '1', '0'],
   ['hDelPtRel',     '0', '0'],
   ['hDR',           '0', '0'],
   ['hLeadingJetPt', '0', '0'],
   ['hST',           '0', '1'],
   ['hHiggsMReco',   '0', '0'],
   ['hTopPt',        '0', '0'],
   ['hTopMReco',     '0', '0'],
   ['hTPrimeMReco',  '0', '1'],
   ['hdR_Ht',        '0', '0'],
   ['hWMReco',       '0', '0'],
   ['hChi2',         '1', '0'],
 
    ##['hTopEta'],
    ##['hTopMass'],
    #['hHigssMass'],
    #['hLepPt'+suffix],
    #['hLepEta'+suffix],
    #['hDRMin'+suffix],
    #['hPtRel'+suffix],
    #['hNJets'+suffix],
    #['hNbjets'+suffix],
    #['hNFJets'+suffix],
    #['hLeadingJetPt'+suffix],
    #['hSecLeadingJetPt'+suffix],
    #['hForwardJetPt'+suffix],
    #['hForwardJetEta'+suffix],
    #['hLeadingJetPt'+suffix],
    #['hSecLeadingJetPt'+suffix],
    #['hHT'+suffix],
    #['hMet'+suffix],
     
    ]

command = "python plot.py --var={0:s} --logScale={1:s} --plotDir='Aug05Plots'"

hists = []
for option in options :
    s = command.format(
        option[0], option[1]
        )
    
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo %s"%s,""]                                                                      , shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( ["echo --------------------------------------------------------------------------",""], shell=True)
    subprocess.call( [s, ""]                                                                               , shell=True)

    # write the desired plots in a single output file
    if option[2] == '1':
        f_out = TFile("Aug05Plots/"+option[0]+".root")
        print 'histos to be added in new file: \n' 
        f_out.ls()
        for key in f_out.GetListOfKeys():
            kname = key.GetName()
            h = f_out.Get(kname)
            f_new = TFile("Aug05Plots/all.root", "UPDATE")
            h.Write()
            f_new.Close()
        f_out.Close()

