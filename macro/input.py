#! /usr/bin/env python
import sys, os
from ROOT import TH1D,TFile,TLegend

# =====================================================
#  INPUTS               
# =====================================================
gSF = 0.97 #trigger SF
path = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/condor/Histo_Sep9/'

f_tt_0_600        =  TFile(path+'tt-4p-0-600.root')
f_tt_600_1100     =  TFile(path+'tt-4p-600-1100.root')
f_tt_1100_1700    =  TFile(path+'tt-4p-1100-1700.root')
f_tt_1700_2500    =  TFile(path+'tt-4p-1700-2500.root')
f_tt_2500_100000  =  TFile(path+'tt-4p-2500-100000.root')
f_Vj_0_300        =  TFile(path+'Bj-4p-0-300.root')
f_Vj_300_600      =  TFile(path+'Bj-4p-300-600.root')
f_Vj_600_1100     =  TFile(path+'Bj-4p-600-1100.root')
f_Vj_1100_1800    =  TFile(path+'Bj-4p-1100-1800.root')
f_Vj_1800_2700    =  TFile(path+'Bj-4p-1800-2700.root')
f_Vj_2700_3700    =  TFile(path+'Bj-4p-2700-3700.root')
f_Vj_3700_100000  =  TFile(path+'Bj-4p-3700-100000.root')
f_tj_0_500        =  TFile(path+'tj-4p-0-500.root')
f_tj_500_1000     =  TFile(path+'tj-4p-500-1000.root')
f_tj_1000_1600    =  TFile(path+'tj-4p-1000-1600.root')
f_tj_1600_2400    =  TFile(path+'tj-4p-1600-2400.root')
f_tj_2400_100000  =  TFile(path+'tj-4p-2400-100000.root')
f_BB_0_300        =  TFile(path+'BB-4p-0-300.root')
f_BB_300_700      =  TFile(path+'BB-4p-300-700.root')
f_BB_700_1300     =  TFile(path+'BB-4p-700-1300.root')
f_BB_1300_2100    =  TFile(path+'BB-4p-1300-2100.root')
f_BB_2100_100000  =  TFile(path+'BB-4p-2100-100000.root')

f_Tbj_M1          =  TFile(path+'Tbj_M1.root')
f_Tbj_M1p5        =  TFile(path+'Tbj_M1p5.root')
f_Tbj_M2          =  TFile(path+'Tbj_M2.root')
f_Tbj_M2p5        =  TFile(path+'Tbj_M2p5.root')
f_Tbj_M3          =  TFile(path+'Tbj_M3.root')

f_Ttj_M1          =  TFile(path+'Ttj_M1.root')
f_Ttj_M1p5        =  TFile(path+'Ttj_M1p5.root')
f_Ttj_M2          =  TFile(path+'Ttj_M2.root')
f_Ttj_M2p5        =  TFile(path+'Ttj_M2p5.root')
f_Ttj_M3          =  TFile(path+'Ttj_M3.root')

#===== cross sections (pb)==========
tt_0_600_xs       = 530.89358   * gSF * 1.6562
tt_600_1100_xs    = 42.55351    * gSF * 1.6562
tt_1100_1700_xs   = 4.48209     * gSF * 1.6562    
tt_1700_2500_xs   = 0.52795     * gSF * 1.6562
tt_2500_100000_xs = 0.05449     * gSF * 1.6562
Vj_0_300_xs       = 34409.92339 * gSF * 1.23
Vj_300_600_xs     = 2642.85309  * gSF * 1.23
Vj_600_1100_xs    = 294.12311   * gSF * 1.23
Vj_1100_1800_xs   = 25.95000    * gSF * 1.23
Vj_1800_2700_xs   = 2.4211      * gSF * 1.23
Vj_2700_3700_xs   = 0.22690     * gSF * 1.23
Vj_3700_100000_xs = 0.02767     * gSF * 1.23
tj_0_500_xs       = 109.73602   * gSF * 1.00
tj_500_1000_xs    = 5.99325     * gSF * 1.00
tj_1000_1600_xs   = 0.37680     * gSF * 1.00
tj_1600_2400_xs   = 0.03462     * gSF * 1.00
tj_2400_100000_xs = 0.00312     * gSF * 1.00
BB_0_300_xs       = 249.97710   * gSF * 1.00
BB_300_700_xs     = 35.23062    * gSF * 1.00
BB_700_1300_xs    = 4.13743     * gSF * 1.00
BB_1300_2100_xs   = 0.41702     * gSF * 1.00
BB_2100_100000_xs = 0.04770     * gSF * 1.00

Tbj_M1_xs         = 1.0; #0.2;
Tbj_M1p5_xs       = 1.0;
Tbj_M2_xs         = 1.0;
Tbj_M2p5_xs       = 1.0;
Tbj_M3_xs         = 1.0;
Ttj_M1_xs         = 1.0; #0.2;
Ttj_M1p5_xs       = 1.0;
Ttj_M2_xs         = 1.0;
Ttj_M2p5_xs       = 1.0;
Ttj_M3_xs         = 1.0;

#===== generated events==========
tt_0_600_num       = f_tt_0_600.Get('hNGenEvents').GetBinContent(1)
tt_600_1100_num    = f_tt_600_1100.Get('hNGenEvents').GetBinContent(1)
tt_1100_1700_num   = f_tt_1100_1700.Get('hNGenEvents').GetBinContent(1)
tt_1700_2500_num   = f_tt_1700_2500.Get('hNGenEvents').GetBinContent(1)
tt_2500_100000_num = f_tt_2500_100000.Get('hNGenEvents').GetBinContent(1)
Vj_0_300_num       = f_Vj_0_300.Get('hNGenEvents').GetBinContent(1) 
Vj_300_600_num     = f_Vj_300_600.Get('hNGenEvents').GetBinContent(1) 
Vj_600_1100_num    = f_Vj_600_1100.Get('hNGenEvents').GetBinContent(1) 
Vj_1100_1800_num   = f_Vj_1100_1800.Get('hNGenEvents').GetBinContent(1)
Vj_1800_2700_num   = f_Vj_1800_2700.Get('hNGenEvents').GetBinContent(1)
Vj_2700_3700_num   = f_Vj_2700_3700.Get('hNGenEvents').GetBinContent(1)
Vj_3700_100000_num = f_Vj_3700_100000.Get('hNGenEvents').GetBinContent(1)
tj_0_500_num       = f_tj_0_500.Get('hNGenEvents').GetBinContent(1)
tj_500_1000_num    = f_tj_500_1000.Get('hNGenEvents').GetBinContent(1)
tj_1000_1600_num   = f_tj_1000_1600.Get('hNGenEvents').GetBinContent(1)
tj_1600_2400_num   = f_tj_1600_2400.Get('hNGenEvents').GetBinContent(1)
tj_2400_100000_num = f_tj_2400_100000.Get('hNGenEvents').GetBinContent(1)
BB_0_300_num       = f_BB_0_300.Get('hNGenEvents').GetBinContent(1)
BB_300_700_num     = f_BB_300_700.Get('hNGenEvents').GetBinContent(1)
BB_700_1300_num    = f_BB_700_1300.Get('hNGenEvents').GetBinContent(1)
BB_1300_2100_num   = f_BB_1300_2100.Get('hNGenEvents').GetBinContent(1)
BB_2100_100000_num = f_BB_2100_100000.Get('hNGenEvents').GetBinContent(1)

Tbj_M1_num         = f_Tbj_M1.Get('hNGenEvents').GetBinContent(1)
Tbj_M1p5_num       = f_Tbj_M1p5.Get('hNGenEvents').GetBinContent(1)
Tbj_M2_num         = f_Tbj_M2.Get('hNGenEvents').GetBinContent(1)
Tbj_M2p5_num       = f_Tbj_M2p5.Get('hNGenEvents').GetBinContent(1)
Tbj_M3_num         = f_Tbj_M3.Get('hNGenEvents').GetBinContent(1)
Ttj_M1_num         = f_Ttj_M1.Get('hNGenEvents').GetBinContent(1)
Ttj_M1p5_num       = f_Ttj_M1p5.Get('hNGenEvents').GetBinContent(1)
Ttj_M2_num         = f_Ttj_M2.Get('hNGenEvents').GetBinContent(1)
Ttj_M2p5_num       = f_Ttj_M2p5.Get('hNGenEvents').GetBinContent(1)
Ttj_M3_num         = f_Ttj_M3.Get('hNGenEvents').GetBinContent(1)

# =====================================================
#  VARIABLES           
# =====================================================

# Legend
leg = TLegend(0.70,0.90,0.96,0.60)
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.SetLineColor(10)
leg.SetLineWidth(0)

# =====================================================
#  FUNCTIONS            
# =====================================================

def overUnderFlow(hist):
    xbins = hist.GetNbinsX()
    hist.SetBinContent(xbins, hist.GetBinContent(xbins)+hist.GetBinContent(xbins+1))
    hist.SetBinContent(1, hist.GetBinContent(0)+hist.GetBinContent(1))
    hist.SetBinError(xbins, TMath.Sqrt(TMath.Power(hist.GetBinError(xbins),2)+TMath.Power(hist.GetBinError(xbins+1),2)))
    hist.SetBinError(1, TMath.Sqrt(TMath.Power(hist.GetBinError(0),2)+TMath.Power(hist.GetBinError(1),2)))
    hist.SetBinContent(xbins+1, 0.)
    hist.SetBinContent(0, 0.)
    hist.SetBinError(xbins+1, 0.)
    hist.SetBinError(0, 0.)

def setCosmetics(hist, legname, hname, color):
    hist.Rebin(rebinS)
    hist.SetLineColor(color)
    hist.SetName(hname)
    #hist.SetTitle("")
    if 'Tbj' in hname or 'Ttj' in hname:
        hist.SetLineWidth(2)
        leg.AddEntry(hist, legname, 'l')
    else:
        hist.SetFillColor(color)
        leg.AddEntry(hist, legname, 'f')

def setTitle(hs,xTitle,yTitle):
    y = hs.GetYaxis()
    x = hs.GetXaxis()
    #y.SetTitle("Events / Bin")
    y.SetTitle(yTitle)
    x.SetTitle(xTitle)
    y.SetLabelSize(0.04)
    y.SetTitleSize(0.06)
    y.SetTitleOffset(0.75)
    y.SetTitleFont(42)
    x.SetTitleSize(0.04)
    x.SetTitleFont(42)

def getHisto( label, leg, var, Samples, color, verbose) :
    histos = []
    for iSample in Samples :
        ifile = iSample[0]
        xs = iSample[1]
        nevt = iSample[2]
        lumi = iSample[3]
        readname = var
        hist  = ifile.Get( readname ).Clone()
        if verbose:
            print 'file: {0:<20}, histo:{1:<10}, integral before weight:{2:<3.3f}, nEntries:{3:<3.0f}, weight:{4:<2.3f}'.format(
                ifile.GetName(),
                hist.GetName(),
                hist.Integral(), hist.GetEntries(), xs * lumi /nevt
                )
        hist.Sumw2()
        hist.Scale( xs * lumi /nevt)
        histos.append( hist )

    histo = histos[0]
    setCosmetics(histo, leg, label+var, color)
    for ihisto in range(1, len(histos) ):
        #print 'ihisto =', ihisto, 'integral', histos[ihisto].Integral(), ', entries', histos[ihisto].GetEntries()
        histo.Add( histos[ihisto] )
        #print 'after addition', histo.Integral()
    if verbose:
        print 'newName: {0:<5}, Entries:{1:5.2f},  newIntegral: {2:5.2f}'.format(label+var, histo.GetEntries(), histo.Integral() )
    return histo
