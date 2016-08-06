#! /usr/bin/env python
import sys
import os
import subprocess
from array import array
from ROOT import TH1D,TH2D,TFile,TMath,TCanvas,THStack,TLegend,TPave,TLine,TLatex
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kMagenta,kYellow,kCyan,kGreen,kGray,kBlack,kTRUE

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--var', metavar='T', type='string', action='store',
                  default='hTopPt',
                  dest='var',
                  help='variable to plot')
parser.add_option('--Lumi', metavar='D', type='float', action='store',
                  default= 3000000., 
                  dest='Lumi',
                  help='Data Luminosity in pb-1')
parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Aug05Plots',
                  dest='plotDir',
                  help='output directory of plots')
parser.add_option('--rebin', metavar='T', type='int', action='store',
                  default='1',
                  dest='rebin',
                  help='rebin the histograms')
parser.add_option('--logScale',action='store',
                  default=0,
                  dest='logScale',
                  help='draw on log scale (1/0)')
parser.add_option('--verbose',action='store_true',
                  default=False,
                  dest='verbose',
                  help='verbose switch')
(options,args) = parser.parse_args()
# ==========end: options =============
var = options.var
rebinS = options.rebin
outDir = options.plotDir
lumi = options.Lumi
drawLog = options.logScale
verbose = options.verbose
# ==========add the input ============

execfile("input.py")

# === prepare the input labels and legends ===========

topLabel      = 'Top_'
topLeg        = 't#bar{t}'
vJetsLabel    = 'VJets_'
vJetsLeg      = 'V+Jets'
stopLebel     = 'st_'
stopLeg       = 'single t'
TbjLabel      = 'Tbj_M1000'
TbjLeg        = 'Tbj (T #rightarrow tH), 100pb'


# === create structure ============
top = [
    [f_tt_0_600,         tt_0_600_xs,            tt_0_600_num,            lumi],
    [f_tt_600_1100,      tt_600_1100_xs,         tt_600_1100_num,         lumi],
    [f_tt_1100_1700,     tt_1100_1700_xs,        tt_1100_1700_num,        lumi],
    [f_tt_1700_2500,     tt_1700_2500_xs,        tt_1700_2500_num,        lumi],
    [f_tt_2500_100000,   tt_2500_100000_xs,      tt_2500_100000_num,      lumi],
    ]

vJets =[
    [f_Vj_0_300,         Vj_0_300_xs,            Vj_0_300_num,            lumi],
    [f_Vj_300_600,       Vj_300_600_xs,          Vj_300_600_num,          lumi],
    [f_Vj_600_1100,      Vj_600_1100_xs,         Vj_600_1100_num,         lumi],
    [f_Vj_1100_1800,     Vj_1100_1800_xs,        Vj_1100_1800_num,        lumi],
    [f_Vj_2700_3700,     Vj_2700_3700_xs,        Vj_2700_3700_num,        lumi],
    [f_Vj_3700_100000,   Vj_3700_100000_xs,      Vj_3700_100000_num,      lumi],   
    ]

st = [
    [f_tj_0_500,         tj_0_500_xs,            tj_0_500_num,            lumi],
    [f_tj_500_1000,      tj_500_1000_xs,         tj_500_1000_num,         lumi],
    [f_tj_1000_1600,     tj_1000_1600_xs,        tj_1000_1600_num,        lumi],
    [f_tj_1600_2400,     tj_1600_2400_xs,        tj_1600_2400_num,        lumi],
    [f_tj_2400_100000,   tj_2400_100000_xs,      tj_2400_100000_num,      lumi],  
    ]

Tbj = [[f_Tbj_M1,        Tbj_M1_xs,              Tbj_M1_num,              lumi]]

h_top         = getHisto(topLabel,        topLeg,      var,  top,       8,          verbose)
h_vJet        = getHisto(vJetsLabel,      vJetsLeg,    var,  vJets,     kBlue,      verbose)
h_st          = getHisto(stopLebel,       stopLeg,     var,  st,        kCyan,      verbose)
h_Tbj         = getHisto(TbjLabel,        TbjLeg,      var,  Tbj,       kBlack,     verbose)  

c1 = TCanvas('c1', 'c1', 1000, 600)

templates = []
templates.append(h_top)
templates.append(h_vJet)
templates.append(h_st)
templates.append(h_Tbj)

#histo properties
nBins = h_top.GetNbinsX()
bMin = h_top.GetBinLowEdge(1)
bMax = h_top.GetBinLowEdge(nBins+1)
bin1 = h_top.GetXaxis().FindBin(bMin)
bin2 = h_top.GetXaxis().FindBin(bMax)

#for ibin in range(0,nBins+1):
#    iTop = h_top.GetBinContent(ibin) 

f = TFile(outDir+"/"+var+".root", "RECREATE")
integralError = Double(5)
for ihist in templates :
    if var != 'hEff': overUnderFlow(ihist)
    ihist.IntegralAndError(bin1,bin2,integralError)
    print '{0:<5} & {1:<5.2f} $\pm$ {2:<5.2f} \\\\ '.format(ihist.GetName().split('_')[1], ihist.Integral(bin1,bin2), integralError)
    ihist.Write() 
print '\hline'

f.Close()


hs = THStack("","")
for ihist in reversed(templates[0:3]):
    hs.Add(ihist)
    print 'histo added', ihist.GetName()
   
if h_Tbj.GetMaximum() > hs.GetMaximum():
    hs.SetMaximum(h_Tbj.GetMaximum())
else:
    h_Tbj.SetMaximum(hs.GetMaximum())

#hs.SetMaximum(hs.GetMaximum()*5)
if var == 'hEff':hs.SetMinimum(100000)
else: hs.SetMinimum(10)

if drawLog == '1':
    gPad.SetLogy()

hs.Draw("Hist")
h_Tbj.Draw("same, hist")     

xTitle= h_top.GetXaxis().GetTitle()
yTitle= h_top.GetYaxis().GetTitle()

setTitle(hs, xTitle, yTitle)
gPad.RedrawAxis()

ll = TLatex()
ll.SetNDC(kTRUE)
ll.SetTextSize(0.05)
ll.DrawLatex(0.68,0.92, "3000 fb^{-1} (14 TeV)");

prel = TLatex()
prel.SetNDC(kTRUE)
prel.SetTextFont(52)
prel.SetTextSize(0.05)
prel.DrawLatex(0.25,0.92,"Preliminary")

cms = TLatex()
cms.SetNDC(kTRUE)
cms.SetTextFont(61)
cms.SetTextSize(0.05)
cms.DrawLatex(0.15,0.92,"CMS")
leg.Draw()

c1.SaveAs(outDir+"/"+var+".png")
c1.SaveAs(outDir+"/"+var+".pdf")
raw_input("hold on")
