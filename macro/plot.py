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
#gROOT.SetBatch()
gROOT.SetStyle("Plain")
gStyle.SetOptStat()
gStyle.SetOptTitle(0)
gStyle.SetPalette(1)
gStyle.SetNdivisions(405,"x");
gStyle.SetEndErrorSize(0.)
gStyle.SetErrorX(0.001)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--var', metavar='T', type='string', action='store',
                  default='hEff',
                  dest='var',
                  help='variable to plot')
parser.add_option('--Lumi', metavar='D', type='float', action='store',
                  default= 3000000.,#2300., 
                  dest='Lumi',
                  help='Data Luminosity in pb-1')
parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Sep19Plots',
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
parser.add_option('--legOnly',action='store_true',
                  default=False,
                  dest='legOnly',
                  help='plot legend only')
(options,args) = parser.parse_args()
# ==========end: options =============
var = options.var
rebinS = options.rebin
outDir = options.plotDir
lumi = options.Lumi
drawLog = options.logScale
verbose = options.verbose
legOnly = options.legOnly
# ==========add the input ============

execfile("input.py")

# === prepare the input labels and legends ===========

topLabel      = 'Top_'
topLeg        = 't#bar{t}'
vJetsLabel    = 'VJets_'
vJetsLeg      = 'V+Jets'
stopLabel     = 'st_'
stopLeg       = 'single t'
vvLabel       = 'vv_'
vvLeg         = 'Diboson'

TbjM1Label    = 'Tbj_M1000_'
TbjM1Leg      = 'Tbj_M1.0 (T #rightarrow tH)'#, 1pb'
TbjM1p5Label  = 'Tbj_M1500_'
TbjM1p5Leg    = 'Tbj_M1.5 (T #rightarrow tH)'#, 1pb'
TbjM2Label    = 'Tbj_M2000_'
TbjM2Leg      = 'Tbj_M2.0 (T #rightarrow tH)'#, 1pb'
TbjM2p5Label  = 'Tbj_M2500_'
TbjM2p5Leg    = 'Tbj_M2.5 (T #rightarrow tH)'#, 1pb'
TbjM3Label    = 'Tbj_M3000_'
TbjM3Leg      = 'Tbj_M3.0 (T #rightarrow tH)'#, 1pb'

TtjM1Label    = 'Ttj_M1000_'
TtjM1Leg      = 'Ttj_M1.0 (T #rightarrow tH)'#, 1pb'
TtjM1p5Label  = 'Ttj_M1500_'
TtjM1p5Leg    = 'Ttj_M1.5 (T #rightarrow tH)'#, 1pb'
TtjM2Label    = 'Ttj_M2000_'
TtjM2Leg      = 'Ttj_M2.0 (T #rightarrow tH)'#, 1pb'
TtjM2p5Label  = 'Ttj_M2500_'
TtjM2p5Leg    = 'Ttj_M2.5 (T #rightarrow tH)'#, 1pb'
TtjM3Label    = 'Ttj_M3000_'
TtjM3Leg      = 'Ttj_M3.0 (T #rightarrow tH)'#, 1pb'

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

vv = [
    [f_BB_0_300,         BB_0_300_xs,            BB_0_300_num,            lumi],
    [f_BB_300_700,       BB_300_700_xs,          BB_300_700_num,          lumi],
    [f_BB_700_1300,      BB_700_1300_xs,         BB_700_1300_num,         lumi],
    [f_BB_1300_2100,     BB_1300_2100_xs,        BB_1300_2100_num,        lumi],
    [f_BB_2100_100000,   BB_2100_100000_xs,      BB_2100_100000_num,      lumi],
    ]

TbjM1  = [[f_Tbj_M1,        Tbj_M1_xs,              Tbj_M1_num,              lumi]]
TbjM1p5= [[f_Tbj_M1p5,      Tbj_M1p5_xs,            Tbj_M1p5_num,            lumi]]
TbjM2  = [[f_Tbj_M2,        Tbj_M2_xs,              Tbj_M2_num,              lumi]]
TbjM2p5= [[f_Tbj_M2p5,      Tbj_M2p5_xs,            Tbj_M2p5_num,            lumi]]
TbjM3  = [[f_Tbj_M3,        Tbj_M3_xs,              Tbj_M3_num,              lumi]]

TtjM1  = [[f_Ttj_M1,        Ttj_M1_xs,              Ttj_M1_num,              lumi]]
TtjM1p5= [[f_Ttj_M1p5,      Ttj_M1p5_xs,            Ttj_M1p5_num,            lumi]]
TtjM2  = [[f_Ttj_M2,        Ttj_M2_xs,              Ttj_M2_num,              lumi]]
TtjM2p5= [[f_Ttj_M2p5,      Ttj_M2p5_xs,            Ttj_M2p5_num,            lumi]]
TtjM3  = [[f_Ttj_M3,        Ttj_M3_xs,              Ttj_M3_num,              lumi]]

#TbjM1  = [[f_Tbj_M1,        Tbj_M1_xs,              1.,              1.]]
#TbjM1p5= [[f_Tbj_M1p5,      Tbj_M1p5_xs,            1.,              1.]]
#TbjM2  = [[f_Tbj_M2,        Tbj_M2_xs,              1.,              1.]]
#TbjM2p5= [[f_Tbj_M2p5,      Tbj_M2p5_xs,            1.,              1.]]
#TbjM3  = [[f_Tbj_M3,        Tbj_M3_xs,              1.,              1.]]

#TtjM1  = [[f_Ttj_M1,        Ttj_M1_xs,              1.,              1.]]
#TtjM1p5= [[f_Ttj_M1p5,      Ttj_M1p5_xs,            1.,              1.]]
#TtjM2  = [[f_Ttj_M2,        Ttj_M2_xs,              1.,              1.]]
#TtjM2p5= [[f_Ttj_M2p5,      Ttj_M2p5_xs,            1.,              1.]]
#TtjM3  = [[f_Ttj_M3,        Ttj_M3_xs,              1.,              1.]]

h_top         = getHisto(topLabel,        topLeg,      var,  top,       8,          verbose)
h_vJet        = getHisto(vJetsLabel,      vJetsLeg,    var,  vJets,     kBlue,      verbose)
h_st          = getHisto(stopLabel,       stopLeg,     var,  st,        kCyan,      verbose)
h_vv          = getHisto(vvLabel,         vvLeg,       var,  vv,        kRed,       verbose)  
h_TbjM1       = getHisto(TbjM1Label,      TbjM1Leg,    var,  TbjM1,     kBlack,     verbose)  
h_TbjM1p5     = getHisto(TbjM1p5Label,    TbjM1p5Leg,  var,  TbjM1p5,   kBlue+2,    verbose)
h_TbjM2       = getHisto(TbjM2Label,      TbjM2Leg,    var,  TbjM2,     kBlue+3,    verbose)  
h_TbjM2p5     = getHisto(TbjM2p5Label,    TbjM2p5Leg,  var,  TbjM2p5,   kBlue-9,    verbose)
h_TbjM3       = getHisto(TbjM3Label,      TbjM3Leg,    var,  TbjM3,     kBlue-3,    verbose) 
h_TtjM1       = getHisto(TtjM1Label,      TtjM1Leg,    var,  TtjM1,     kOrange,     verbose)  
h_TtjM1p5     = getHisto(TtjM1p5Label,    TtjM1p5Leg,  var,  TtjM1p5,   kYellow+2,    verbose)
h_TtjM2       = getHisto(TtjM2Label,      TtjM2Leg,    var,  TtjM2,     kYellow+3,    verbose)  
h_TtjM2p5     = getHisto(TtjM2p5Label,    TtjM2p5Leg,  var,  TtjM2p5,   kYellow-9,    verbose)
h_TtjM3       = getHisto(TtjM3Label,      TtjM3Leg,    var,  TtjM3,     kYellow-3,    verbose)  

#add single top and top backgrounds
h_alltop = h_top.Clone()
h_alltop.Reset()
n =  h_alltop.GetName(); old = n.split('_')[0]; new = n.replace(old, 'allTop')
h_alltop.SetName(new)
h_alltop.Add(h_top)
h_alltop.Add(h_st)

#add vjet and vv backgrounds
h_allvJet = h_vJet.Clone()
h_allvJet.Reset()
n1 =  h_allvJet.GetName(); old1 = n1.split('_')[0]; new1 = n1.replace(old1, 'allVJet')
h_allvJet.SetName(new1)
h_allvJet.Add(h_vJet)
h_allvJet.Add(h_vv)

#total 
h_tot =  h_top.Clone()
h_tot.Reset()
n2 =  h_tot.GetName(); old2 = n2.split('_')[0]; new2 = n2.replace(old2, 'Tot')
h_tot.SetName(new2)
h_tot.Add(h_top)
h_tot.Add(h_vJet)
h_tot.Add(h_st)
h_tot.Add(h_vv)

#dummy data
h_data =  h_top.Clone()
h_data.Reset()
n3 =  h_data.GetName(); old3 = n3.split('_')[0]; new3 = n3.replace(old3, 'data_obs')
h_data.SetName(new3)

c1 = TCanvas('c1', 'c1', 800, 600)

templates = []
templates.append(h_top)
templates.append(h_vJet)
templates.append(h_st)
templates.append(h_vv)
templates.append(h_tot)
templates.append(h_TbjM1)
templates.append(h_TbjM1p5)
templates.append(h_TbjM2)
templates.append(h_TbjM2p5)
templates.append(h_TbjM3)
templates.append(h_TtjM1)
templates.append(h_TtjM1p5)
templates.append(h_TtjM2)
templates.append(h_TtjM2p5)
templates.append(h_TtjM3)
templates.append(h_alltop)
templates.append(h_allvJet)
templates.append(h_data)

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
    if 'Tbj' in ihist.GetName() or 'Ttj' in ihist.GetName():
        hname = ihist.GetName().split('_')[0]+'_'+ihist.GetName().split('_')[1]
    else:
        hname = ihist.GetName().split('_')[0]
    print '{0:<5} & {1:<5.2f} $\pm$ {2:<5.2f} \\\\ '.format(hname, ihist.Integral(bin1,bin2), integralError)
    ihist.Write() 
print '\hline'

f.Close()

if var == 'hWMReco':
    ibin = int((80.4 - bMin)/(bMax - bMin)*float(nBins))
    fail = h_TbjM1.Integral(ibin+2,bin2)
    tot  = h_TbjM1.Integral(ibin,bin2)
    print 'total: ', tot, 'fail (%): ', (fail/tot)*100 
  
hs = THStack("","")
for ihist in reversed(templates[0:4]):
    hs.Add(ihist)
    print 'histo added', ihist.GetName()
   
if h_TbjM1.GetMaximum() > hs.GetMaximum():
    hs.SetMaximum(h_TbjM1.GetMaximum())
else:
    h_TbjM1.SetMaximum(hs.GetMaximum())

#hs.SetMaximum(hs.GetMaximum()*5)
if var == 'hEff':hs.SetMinimum(100000)
else: hs.SetMinimum(10)
#hs.SetMaximum(3600000)
if drawLog == '1':
    gPad.SetLogy()

if not legOnly:
    hs.Draw("Hist")
for ihist in reversed(templates[5:15]):
    print ihist.GetName()
    #ihist.SetMaximum(10000)
    #ihist.GetYaxis().SetTitle("a.u")
    #ihist.Scale(1/300000.)
    if not legOnly:
        ihist.Draw("same, hist")     
    
xTitle= h_top.GetXaxis().GetTitle()
yTitle= h_top.GetYaxis().GetTitle()

setTitle(hs, xTitle, yTitle)
gPad.RedrawAxis()

ll = TLatex()
ll.SetNDC(kTRUE)
ll.SetTextSize(0.05)
ll.DrawLatex(0.63,0.92, "3000 fb^{-1} (14 TeV)");

prel = TLatex()
prel.SetNDC(kTRUE)
prel.SetTextFont(52)
prel.SetTextSize(0.05)
prel.DrawLatex(0.18,0.92,"Simulation")

cms = TLatex()
cms.SetNDC(kTRUE)
cms.SetTextFont(61)
cms.SetTextSize(0.05)
cms.DrawLatex(0.10,0.92,"CMS")
if var != 'hTPrimeMRecoBoost' and not legOnly:
    leg.Draw()

c1.SaveAs(outDir+"/"+var+".png")
c1.SaveAs(outDir+"/"+var+".pdf")
raw_input("hold on")
