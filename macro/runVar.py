#!/bin/python
import sys, os
from ROOT import TH1D,TFile, TIter, TFileIter, TKey, TObject

import subprocess

#suffix = '_sig'

options = [
   #['hEff',            '1', '0'],
   #['hLepIso',         '1', '0'],
   #['hLepIso_sig',     '1', '0'],
   #['hLepEta',         '1', '0'], 
   #['hLepEta_sig',     '1', '0'],
   #['hLepPt',          '1', '0'],
   #['hLepPt_sig',      '1', '0'],
   #['hNJets',              '1', '0'],
   #['hNJets_sig',          '1', '0'],
   #['hNFJets',             '1', '0'],
   #['hNFJets_sig',         '1', '0'],
   #['hNbjets',             '1', '0'],  
   #['hNbjets_sig',         '1', '0'],
   #['hForwardJetPt',       '1', '0'],
   #['hForwardJetPt_sig',   '1', '0'],
   #['hForwardJetEta',      '1', '0'],
   #['hForwardJetEta_sig',  '1', '0'],
   #['hLeadingJetPt',       '1', '0'],
   #['hLeadingJetPt_sig',   '1', '0'],
   #['hSecLeadingJetPt',    '1', '0'],
   #['hSecLeadingJetPt_sig','1', '0'],
   #['hLeadingbJetPt',      '1', '0'],
   #['hLeadingbJetPt_sig',  '1', '0'],
   #['hMet',                '1', '0'],
   #['hMet_sig',            '1', '0'],
   #['hDelRJet1Met',        '1', '0'],
   #['hDelRJet1Met_sig',    '1', '0'],
   #['hHT',                 '1', '1'],
   #['hHT_sig',             '1', '1'],
   #['hST',                 '1', '1'],
   #['hST_sig',             '1', '1'],

  # ['hDelPtRel',           '1', '0'],
  # ['hPtRel',              '1', '0'],   
  # ['hDPtRel',             '1', '0'],   
  # ['hDRMin',              '1', '0'],
  # ['hDR',                 '1', '0'],
  # ['hHiggsMReco',         '1', '0'], 
   #['hHiggsMRecoBoost',    '1', '0'],   
  # ['hHiggsPt',            '1', '0'],
   #['hHiggsPtBoost',       '1', '0'], 
  # ['hTopPt',              '1', '0'],
   #['hTopPtBoost',         '1', '0'],
  # ['hTopMReco',           '1', '0'],
  #['hTopMRecoBoost',      '1', '0'],

  #['hTPrimeMReco',         '1', '1'],
  ['hTPrimeMRecoBoost',    '1', '1'],
  # ['hTPrimeMReco_1bjet',   '1', '1'],
  # ['hTPrimeMReco_2bjet',   '1', '1'],
  # ['hdR_Ht',               '1', '0'],
   #['hdR_HtBoost',          '1', '0'],
   #['hWMReco',              '1', '0'],
  # ['hChi2',                '1', '0'],
   #['hChi2Boost',           '1', '1'],
  
    #['hSTBoost',            '1', '1'],     
    #['hSTResolved',         '1', '1'],
   # ['hSoftMass',           '1', '0'],
   # ['hSoftPt',             '1', '0'],
    #['h2DdPtReldR',         '0', '0'],
     
    ]

command = "python plot.py --var={0:s} --logScale={1:s} --plotDir='Sep20Plots'"

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
        f_out = TFile("Sep20Plots/"+option[0]+".root")
        print 'histos to be added in new file: \n' 
        f_out.ls()
        for key in f_out.GetListOfKeys():
            kname = key.GetName()
            h = f_out.Get(kname)
            f_new = TFile("Sep20Plots/all.root", "UPDATE")
            h.Write()
            f_new.Close()
        f_out.Close()
    
