#! /usr/bin/env python
import sys
from ROOT import TH1D,TH2D,TFile,TMath,TCanvas,THStack,TLegend,TPave,TGraph,TMultiGraph,TLatex,TLine
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kMagenta,kYellow,kCyan,kGreen,kGray,kTRUE

gROOT.Macro("~/rootlogon.C")
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
leg = TLegend(0.70,0.91,0.94,0.60)
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.SetLineColor(10)
leg.SetLineWidth(0)
 
def setCosmetics(hist, legname, hname, color, var):
    if var == 'st': Var = 'S_{T}'
    elif var == 'TPrimeMRecoBoost': Var = 'M_{T}'#'M_{#Chi^{2}}'
    legname.split('_',0)[0]
    hist.SetLineColor(color)
    hist.GetYaxis().SetTitle('S/sqrt(S+B)')
    hist.GetYaxis().SetTitleOffset(1.2)
    hist.GetYaxis().SetTitleFont(42)
    hist.GetXaxis().SetTitleOffset(1.2)
    hist.GetXaxis().SetTitleFont(42)
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
perBin = False
path = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/macro/Sep20Plots/'
pathH = '/uscms_data/d2/skhalil/Delphes2/CMSSW_8_0_4/src/DelphesAnalysis/limit/inputFiles/'

#channel = ['Tbj', 'Ttj']
#massString = ['1', '1p5', '2', '2p5', '3']
#massNum = [1, 1.5, 2, 2.5, 3]
#mass = zip (massNum, massString) 
#templates = []
#print mass
#hEff = TH1D('', 'Signal Efficiency; T Mass [GeV]; efficiency (%)', 5, 750, 3250)
leg = TLegend(0.75,0.75,0.95,0.92)
leg.SetBorderSize(1)
leg.SetFillColor(10)

optPoint = [TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph()]
optGraph = [TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph(), TGraph()]
optMultiGraph = TMultiGraph()
optMultiPoint = TMultiGraph()
#optMultiGraph.SetTitle("significance;"+xTitle+"; S/ #sqrt{S+B}")
hSig = TH1D('', 'Significance; T Mass [GeV]; S/sqrt(S+B) ', 5, 750, 3250)
hSig2 = TH1D('', 'Significance; T Mass [GeV]; S/sqrt(S+B)', 3, 750, 2250)
icol = 0
mass = [1000, 1500, 2000, 2500, 3000]
channel = ['Tbj', 'Ttj']
templates = []
f = TFile(path+'h'+var+'.root')
h_bkg = f.Get('Tot_h'+var).Clone()
Nbins = h_bkg.GetNbinsX()

igraph = 0
for ch in channel:
    h_Sig =  hSig.Clone()
    h_Sig.SetDirectory(0)
    if not perBin: ibin = 0
    for m in mass:       
        h_sig = f.Get(ch+'_M'+str(m)+'h'+var)
        sOverb = 0
        if perBin:
            optsOverb = 0
            optVal = 0
            optBin = 0
            optSig = 0
            optBkg = 0
            for ibin in range(Nbins):
                mybin = ibin+1
                bkg = h_bkg.Integral(mybin, Nbins)
                sig = h_sig.Integral(mybin, Nbins)
                xAxis = h_bkg.GetBinCenter(mybin)
                if bkg+sig != 0. :
                    sOverb = sig/TMath.Sqrt(bkg+sig)#+0.5*bkg)
                else: sOverb = 0.
                #print '{0:<5.1f} & {1:<5.1f} \\\ '.format((xAxis-5), sOverb)
                optGraph[igraph].SetPoint(ibin, xAxis, sOverb)
                if sOverb > optsOverb:
                    optsOverb = sOverb; optSig = sig; optBkg = bkg; optVal = xAxis; optBin = ibin
            print '{0:<5}  &{1:<5.1f} & {2:<5.1f} & {3:<5.1f} & {4:<5.1f}  \\\\ '.format(str(m), optsOverb, optSig, optBkg, optVal)
            optPoint[igraph].SetPoint(optBin, optVal, optsOverb)
            optMultiPoint.Add(optPoint[igraph])
            optGraph[igraph].SetLineColor(igraph+2)
            optGraph[igraph].SetMarkerColor(igraph+2)
            optMultiGraph.Add(optGraph[igraph])
            leg.AddEntry(optGraph[igraph],ch+'_M'+str(m), 'l')
            igraph = igraph + 1
        else:
            sig = h_sig.Integral()
            bkg = h_bkg.Integral()
            
          #  xAxis = h_bkg.GetBinCenter(m)
            if bkg+sig != 0. :
                sOverb = sig/TMath.Sqrt(bkg+sig)#+0.5*bkg)
            else: sOverb = 0.
            print '{0:<5} & {1:<5.1f} & {2:<5.1f} & {3:<5.1f}\\\ '.format(str(m), sig, bkg, sOverb)
            ibin = ((m*2)-1000)/1000
            #print ibin, sOverb
            h_Sig.SetBinContent(int(ibin), sOverb)
          
    setCosmetics(h_Sig, ch+', T #rightarrow tH (14 TeV)', var+'_Sig_M'+str(m)+'_'+ch, kGreen+icol, var)
    #h_Sig.Draw("")
    #raw_input("hold on")
    templates.append(h_Sig)
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
    h_Sig2 = hSig2.Clone()
    h_Sig2.SetDirectory(0)
    sOverb = 0
    for M, ibin in binM_H:
        f_H =  TFile(pathH+'ThetaHistos-'+Ch+He+'.root')
        h_el = f_H.Get('el__Signal_'+Ch+'_TH_'+He+'_M'+str(M)).Clone()
        h_mu = f_H.Get('mu__Signal_'+Ch+'_TH_'+He+'_M'+str(M)).Clone()
        h_el_bkg = f_H.Get('el__Bkg').Clone()
        h_mu_bkg = f_H.Get('mu__Bkg').Clone()
        sig = (h_el.Integral() +  h_mu.Integral())*(3000./2.3)
        bkg = (h_el_bkg.Integral() + h_mu_bkg.Integral())*(3000./2.3)
        if bkg+sig != 0. :
            sOverb = sig/TMath.Sqrt(bkg+sig)#+0.5*bkg)
        else: sOverb = 0.        
        #unc= binomialUnc(eff, 100000.)
        print '{0:<5} & {1:<5.1f} & {2:<5.1f} & {3:<5.1f}\\\ '.format(str(M), sig, bkg, sOverb)
        #print 'Mass: {0:<5.1f} TeV, S/B = {1:<5.2f}'.format(M, sOverb)
        
        print ibin
        if ibin == 3: eff = sOverb*0.90
        h_Sig2.SetBinContent(int(ibin), sOverb)
        #h_Sig2.SetBinError(int(ibin), sign*100)
    if Ch=='TpB': Ch='Tbj'
    elif Ch=='TpT': Ch='Ttj'
    setCosmetics(h_Sig2, Ch+', T #rightarrow tH (13 TeV)', var+'_Sig_M'+str(M)+'_'+Ch, kRed+icol, var)
    templates.append(h_Sig2) 
    icol = icol+1

# ==========Now plot ========
c1 = TCanvas('c1', 'c1', 800, 600)
for h in templates :
    print h.GetName()
    h.SetMaximum(150.0);
    h.SetMinimum(0.0);
    h.Draw("L, same")

#gPad.SetLogy()
#c1.SetGrid()
#optMultiGraph.Draw("ALP*")
#optMultiPoint.Draw("P*")
leg.Draw()

prel = TLatex()
prel.SetNDC(kTRUE)
prel.SetTextFont(52)
prel.SetTextSize(0.05)
prel.DrawLatex(0.34,0.93,"Simulation")

cms = TLatex()
cms.SetNDC(kTRUE)
cms.SetTextFont(61)
cms.SetTextSize(0.05)
cms.DrawLatex(0.10,0.93,"CMS-Delphes")
leg.Draw()

ll = TLatex()
ll.SetNDC(kTRUE)
ll.SetTextSize(0.05)
ll.DrawLatex(0.64,0.93, "3000 fb^{-1}(14 TeV)");
c1.SaveAs(plotDir+'/'+var+'_sign.pdf')
raw_input("hold on")
