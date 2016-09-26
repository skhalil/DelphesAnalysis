#! /usr/bin/env python
import sys
from ROOT import TH1D,TFile,TMath,TCanvas,TLegend,TLatex,TLine
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kMagenta,kYellow,kCyan,kGreen,kGray,kTRUE

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)
#gROOT.SetBatch()
gROOT.SetStyle("Plain")
gStyle.SetOptTitle(0)
gStyle.SetPalette(1)
gStyle.SetNdivisions(405,"x");
gStyle.SetEndErrorSize(0.)
gStyle.SetErrorX(0.001)
gStyle.SetPadTickX(1)
gStyle.SetPadTickY(1)
gStyle.SetOptStat(0) 

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
 
def binomialUnc(eff, Ngen):
    unc = TMath.Sqrt(eff*(1-eff)/Ngen)
    return unc
 
# Legend
#leg = TLegend(0.70,0.91,0.94,0.60)
leg = TLegend(0.60,0.88,0.86,0.60)#44 
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.SetLineColor(10)
leg.SetLineWidth(0)
 
def setCosmetics(hist, legname, hname, color, var):
    if var == 'st': Var = 'S_{T}'
    elif var == 'TPrimeMRecoBoost': Var = 'M_{T}'#'M_{#Chi^{2}}'
    legname.split('_',0)[0]
    hist.SetLineColor(color)
    hist.GetYaxis().SetTitle('Efficieny ( '+Var+' ) %')
    hist.GetYaxis().SetTitleOffset(1.0)
    hist.GetYaxis().SetTitleFont(62)
    hist.GetXaxis().SetTitleOffset(1.2)
    hist.GetXaxis().SetTitleFont(62)
    hist.SetTitle('')
    hist.SetName(hname)
    hist.SetLineWidth(2)
    leg.AddEntry(hist, legname, 'l')
     
# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()

parser.add_option('--var', metavar='V', type='string', action='store',
                  default='TPrimeMRecoBoost',#
                  dest='var',
                  help='variable to plot')
parser.add_option('--plotDir', metavar='P', type='string', action='store',
                  default='Sep20Plots',
                  dest='plotDir',
                  help='output directory of plots')
(options,args) = parser.parse_args()
# ==========end: options =============
var = options.var
plotDir = options.plotDir
path = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/condor/Histo_Sep20/'
pathH = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/limit/inputFiles/'

channel = ['Tbj', 'Ttj']
massString = ['1', '1p5', '2', '2p5', '3']
massNum = [1, 1.5, 2, 2.5, 3]
mass = zip (massNum, massString) 
templates = []
#print mass
hEff = TH1D('', 'Signal Efficiency; T Mass [GeV]; efficiency (%)', 5, 750, 3250)
hEff2 = TH1D('', 'Signal Efficiency; T Mass [GeV]; efficiency (%)', 3, 750, 2250)
#hSig = TH1D('', 'Significance; T Mass [GeV]; S/sqrt(S+B) (%)', 5, 750, 3250)


icol = 0
for ch in channel:
    h_eff = hEff.Clone()
    h_eff.SetDirectory(0)
    #h_Sig =  hSig.Clone()
    #h_Sig.SetDirectory(0)
    ibin = 0
    for m, s in mass:
        
        f = TFile(path+ch+'_M'+s+'.root')
        
        # get the histogram and normalization    
        h1 = f.Get('h'+var).Clone()
        nGen = f.Get('hNGenEvents').GetBinContent(1)*(1/0.58)
        print 'nGen :' ,nGen
        sig = h1.GetEntries()
        # compute eff and uncertainy per mass point
        eff = sig/nGen
        unc = binomialUnc(eff, nGen)
         
        print 'channel: {0:<5}, Mass: {1:<5.1f} TeV, Signal: {2:<5.0f}, NGen = {3:<5.0f}, Eff(%) = {4:<5.2f}+/-{5:<5.2f}'.format(ch, m, sig, nGen, eff*100, unc*100)
        ibin = (m*2)-1
        print ibin
        h_eff.SetBinContent(int(ibin), eff*100)
        h_eff.SetBinError(int(ibin), unc*100)
        
    # make cosmetic changes to the histogram and iterate to next one
    setCosmetics(h_eff, ch+', T #rightarrow tH (14 TeV)', var+'_Eff_'+ch, kGreen*2+icol, var)
    templates.append(h_eff)
    ibin = 0
    icol = icol+1

#======Plots from Heiner======
M_H = [1000, 1500, 1800]
b_H = [1, 2, 3]
Ch_H = ['TpB', 'TpT']
He_H = ['LH', 'RH']
T_H = zip (Ch_H, He_H)
binM_H = zip (M_H, b_H)

for Ch, He in T_H: 
    h_eff2 = hEff2.Clone()
    h_eff2.SetDirectory(0)
    for M, ibin in binM_H:
        f_H =  TFile(pathH+'ThetaHistos-'+Ch+He+'.root')
        h_el = f_H.Get('el__Signal_'+Ch+'_TH_'+He+'_M'+str(M)).Clone()
        h_mu = f_H.Get('mu__Signal_'+Ch+'_TH_'+He+'_M'+str(M)).Clone()
        eff = (h_el.GetEntries() +  h_mu.GetEntries())/100000.
        unc= binomialUnc(eff, 100000.)
        print 'Mass: {0:<5.1f} TeV, Eff for Tbj(%) = {1:<5.2f}+/-{2:<5.2f}'.format(M, eff*100, unc*100) 
        
        print ibin
        if ibin == 3: eff = eff*0.90
        h_eff2.SetBinContent(int(ibin), eff*100)
        h_eff2.SetBinError(int(ibin), unc*100)
    if Ch=='TpB': Ch='Tbj'
    elif Ch=='TpT': Ch='Ttj'
    #setCosmetics(h_eff2, Ch+', T #rightarrow tH (13 TeV)', var+'_Eff_'+Ch, kRed+icol, var)
    #templates.append(h_eff2) 
    icol = icol+1
   

# ==============================
# plot
# ==============================
c1 = TCanvas('c1', 'c1', 800, 600)
 
for h in templates :
    print h.GetName()
    h.SetMaximum(8.0);
    h.SetMinimum(0.0);
    h.Draw("L, same, hist")
leg.Draw()
     
prel = TLatex()
prel.SetNDC(kTRUE)
prel.SetTextFont(52)
prel.SetTextSize(0.05)
#prel.DrawLatex(0.18,0.92,"Simulation")
 
cms = TLatex()
cms.SetNDC(kTRUE)
cms.SetTextFont(61)
cms.SetTextSize(0.05)
cms.DrawLatex(0.10,0.92,"CMS Simulation")
leg.Draw()
 
ll = TLatex()
ll.SetNDC(kTRUE)
ll.SetTextSize(0.05)
ll.DrawLatex(0.64,0.93, "3000 fb^{-1}(14 TeV)");
 
#chan = TLatex()
#chan.SetNDC(kTRUE)
#chan.SetTextSize(0.05)
#chan.DrawLatex(0.20, 0.84, 'T #rightarrow tH')
c1.SaveAs(plotDir+'/'+var+'_eff.pdf')
raw_input('---')
