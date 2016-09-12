#! /usr/bin/env python
import sys
from array import array
from ROOT import TH1D,TH2D,TFile,TMath,TCanvas,THStack,TLegend,TPave,TLine,TLatex
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kMagenta,kYellow,kCyan,kGreen,kGray,kTRUE

gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

def setCosmetics(hist, color, name, leg):
    hist.SetLineColor(color)
    if 'LQD' in name:          
        hist.SetLineWidth(2)
        leg.AddEntry(hist, name, 'l')
    else:
        hist.SetFillColor(color)
        leg.AddEntry(hist, name, 'f')
        
def prepareCanvas(c2):
    c2.Divide(1,2)
    scale = (1 - 0.3)/0.3

    pad = c2.cd(1)
    pad.SetPad(0, 0.2, 1, 1)
    pad.SetTopMargin(0.1)
    pad.SetLeftMargin(0.13)
    pad.SetRightMargin(0.03)
    pad.SetBottomMargin(0.125)

    pad = c2.cd(2)
    pad.SetPad(0, 0.0, 1, 0.3)
    pad.SetTopMargin(0.0)
    pad.SetLeftMargin(0.13)
    pad.SetRightMargin(0.03)
    pad.SetBottomMargin(0.3)
    pad.SetTickx(1)
    pad.SetTicky(1)

def setTitle(hTop, hs, xTitle):
    title = hTop.GetTitle()
    yTitle= hTop.GetYaxis().GetTitle()

    y = hs.GetYaxis()
    x = hs.GetXaxis() 
    y.SetTitle(yTitle)
    x.SetTitle(xTitle)
    y.SetTitleSize(0.05)
    y.SetTitleFont(42)
    x.SetTitleSize(0.05)
    x.SetTitleFont(42)

def prepareRatio(h_ratio, h_ratiobkg, xTitle):
    scale = (1 - 0.3)/0.3
    h_ratio.SetTitle("")
    h_ratio.GetYaxis().SetTitle("Data/Bkg")
    h_ratio.GetXaxis().SetTitle(xTitle)
    
    h_ratio_bkg.SetMarkerSize(0)
    h_ratio_bkg.SetFillColor(kGray+1)
    h_ratio_bkg.SetMaximum(2)
    h_ratio_bkg.SetMinimum(0)
    h_ratio_bkg.GetYaxis().SetLabelSize(0.04*scale)
    h_ratio_bkg.GetYaxis().SetTitleOffset(1.00/scale*0.9)
    h_ratio_bkg.GetYaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio_bkg.GetYaxis().SetTitleFont(42)
    h_ratio_bkg.GetXaxis().SetLabelSize(0.04*scale*1.00)
    h_ratio_bkg.GetXaxis().SetTitleOffset(0.95*scale*0.39)
    h_ratio_bkg.GetXaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio_bkg.GetYaxis().SetNdivisions(505)
    h_ratio_bkg.GetXaxis().SetNdivisions(510)
    h_ratio_bkg.SetTickLength(0.08,"X")
    
    h_ratio.SetMarkerStyle(8)
    h_ratio.SetMaximum(2)
    h_ratio.SetMinimum(0)
    h_ratio.GetYaxis().SetLabelSize(0.04*scale)
    h_ratio.GetYaxis().SetTitleOffset(1.00/scale*0.9)
    h_ratio.GetYaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio.GetYaxis().SetTitleFont(42)
    h_ratio.GetXaxis().SetLabelSize(0.04*scale*1.00)
    h_ratio.GetXaxis().SetTitleOffset(0.95*scale*0.39)
    h_ratio.GetXaxis().SetTitleSize(0.06*scale*1.00)
    h_ratio.GetYaxis().SetNdivisions(505)
    h_ratio.GetXaxis().SetNdivisions(510)
    h_ratio.SetTickLength(0.08,"X")
    
# ===============
# options
# ===============
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--var', metavar='V', type='string', action='store',
                  default='hTPrimeMRecoBoost',
                  dest='var',
                  help='var to get')

parser.add_option('--plot',action='store_true',
                  default=False,
                  dest='plot',
                  help='plot the distribution')

parser.add_option('--latex',action='store_true',
                  default=False,
                  dest='latex',
                  help='print the latex table for sum of jet bins')

(options,args) = parser.parse_args()
# ==========end: options =============
var = options.var
Path = 'inputFiles/'
f = TFile(Path+'all.root')
histMass = []
templates = []
mass = ['1000', '1500', '2000', '2500', '3000']

h_top  = f.Get('Top_'+var).Clone()
h_vjet  = f.Get('VJets_'+var).Clone()
h_singTop = f.Get('st_'+var).Clone()
h_vv      = f.Get('vv_'+var).Clone()

#add single top and top backgrounds
h_alltop = h_top.Clone()
h_alltop.Reset()
n =  h_alltop.GetName(); old = n.split('_')[0]; new = n.replace(old, 'allTop')
h_alltop.SetName(new)
h_alltop.Add(h_top)
h_alltop.Add(h_singTop)

#add vjet and vv backgrounds
h_allvjet = h_vjet.Clone()
h_allvjet.Reset()
n1 =  h_allvjet.GetName(); old1 = n1.split('_')[0]; new1 = n1.replace(old1, 'allVJet')
h_allvjet.SetName(new1)
h_allvjet.Add(h_vjet)
h_allvjet.Add(h_vv)

# sum all the backgrounds
h_total = h_top.Clone()
h_total.Reset()
nt =  h_total.GetName(); oldt = nt.split('_')[0]; newt = n.replace(oldt, 'total')
h_total.SetName(newt)
h_total.Add(h_top)
h_total.Add(h_singTop)
h_total.Add(h_vjet)
h_total.Add(h_vv)

templates.append(h_alltop)
templates.append(h_allvjet)
templates.append(h_total)

for m in mass:
    h_VLQ =  f.Get('Tbj_M'+m+var)
    histMass.append(h_VLQ)
    if m == '1000':
        templates.append(h_VLQ)
    #print 'mass = ', m, 'value = ', h_VLQ.Integral()

nBins = h_top.GetNbinsX()
bMin = h_top.GetBinLowEdge(1)
bMax = h_top.GetBinLowEdge(nBins+1)
bin1 = h_top.GetXaxis().FindBin(bMin)
bin2 = h_top.GetXaxis().FindBin(bMax)

integralError = Double(5)

for h in histMass:
    vlq = h.GetName()#.split('_')[1]
    vlq = vlq.replace(var, '')
    
    h.IntegralAndError(bin1,bin2,integralError)  
    sig    = h.Integral(bin1,bin2)          ; sig_e     = integralError
    
    h_alltop.IntegralAndError(bin1,bin2,integralError)
    alltop = h_alltop.Integral(bin1,bin2)   ; alltop_e   = integralError

    h_allvjet.IntegralAndError(bin1,bin2,integralError)
    allvjet= h_allvjet.Integral(bin1,bin2)  ; allvjet_e =  integralError
    
    print 'sig events: ', sig
    d_out = open('datacards/'+vlq+'_card.txt', 'w')   
    d_out.write("imax 1  number of channels \n")
    d_out.write("jmax 2  number of backgrounds \n")
    d_out.write("kmax 9  number of nuisance parameters \n")
    d_out.write("------------------------------------------- \n")
    d_out.write("# we have just one channel, in which we observe x data events \n")
    d_out.write("bin         {0:<8} \n".format('1'))  
    d_out.write("observation {0:<8} \n".format('0'))      
    d_out.write("--------------------------------------------------------------------------\n")        
    d_out.write("# now we list the expected events for sig and all backgrounds in that bin \n")
    d_out.write("# the second 'process' line must have a positive number for backgrounds, and 0 for signal \n")
    d_out.write("# then we list the independent sources of uncertainties, and give their effect (syst. error) \n")
    d_out.write("# on each process and bin \n")
    d_out.write("bin                         {0:<8}  {1:<8}  {2:<8}   \n".format('1', '1', '1') ) 
    d_out.write("process                     {0:<8}  {1:<8}  {2:<8}   \n".format(vlq, 'top', 'vjets'))      
    d_out.write("process                     {0:<8}  {1:<8}  {2:<8}   \n".format('0', '1', '2'))
    d_out.write("rate                        {0:<8.4f}  {1:<8.4f}  {2:<8.4f}  \n".format(sig, alltop, allvjet)) 
    d_out.write("--------------------------------------------------------------------------\n")
    
    d_out.write("lumi         lnN            {0:<8.4f}  {1:<8}  {2:<8}  lumi \n".format(1.015, 1.015, 1.015))
    d_out.write("norm_ttbar   lnN            {0:<8}  {1:<8.4f}  {2:<8}   ttbar normalization \n".format('-', 1.160, '-') )
    d_out.write("norm_vjets   lnN            {0:<8}  {1:<8}  {2:<8.4f}   vjets normalization \n".format('-', '-', 1.200) )
    d_out.write("b-tagSF      lnN            {0:<8.4f}  {1:<8.4f}  {2:<8.4f}    b-tag SF \n".format(1.027, 1.027, 1.027) )
    d_out.write("ID           lnN            {0:<8.4f}  {1:<8.4f}  {2:<8.4f}    ID SF \n".format(1.010, 1.010, 1.010) )
    d_out.write("trigger      lnN            {0:<8.4f}  {1:<8.4f}  {2:<8.4f}    trigger SF \n".format(1.010, 1.010, 1.010) )
    d_out.write("lep_iso      lnN            {0:<8.4f}  {1:<8.4f}  {2:<8.4f}    lepton isolation SF \n".format(1.030, 1.030, 1.030) )
    d_out.write("JES          lnN            {0:<8.4f}  {1:<8.4f}  {2:<8.4f}    JES \n".format(1.038, 1.038, 1.038) )
    d_out.write("JER          lnN            {0:<8.4f}  {1:<8.4f}  {2:<8.4f}    JER \n".format(1.010, 1.010, 1.010) )
    d_out.close()    



if options.latex:
    l_out = open('latex/latex.txt', 'w')
    integralError = Double(5)
    bin1 = h_top.GetXaxis().FindBin(bMin)
    bin2 = h_top.GetXaxis().FindBin(bMax)
    #print '\n'
    l_out.write('\\begin{tabular}{|c|c| } \n')
    l_out.write('\hline \n')
    l_out.write('Sample     & Events  \\\\ \n')
    l_out.write('\hline \n')
    count = 0
    for h in templates:
        count = count+1
        #if 'M' in h.GetName(): hname = h.GetName().split('_')[1]
        #else: hname = h.GetName().split('_')[0]
        #h.IntegralAndError(5,bin2,integralError)
        #if count == 4 or count == 6 : l_out.write('\hline \n')
        #if count == 5: l_out.write('\hline \hline \n')
        #l_out.write('{0:<10} & {1:<7.2f} $\pm$ {2:<7.2f} \\\\  \n'.format(hname, h.Integral(5,bin2), integralError))
    l_out.write('\hline \n')
    l_out.write('\end{tabular} \n')
    l_out.close()

if options.plot:
    leg = TLegend(0.75,0.75,0.95,0.92)
    leg.SetBorderSize(1)
    leg.SetFillColor(10)

    #h_data.SetMarkerStyle(8)
    #leg.AddEntry(h_data, "Data 19.6 fb^{-1}", 'pl')

    setCosmetics(h_alltop, 8, 'TTJets',leg)
    setCosmetics(h_allvjet, 90, 'VJets',leg)
    #setCosmetics(h_stop, 38, 'Diboson',leg)
    setCosmetics(h_VLQ, kBlue-3, model+'_1000',leg)
    
    hs = THStack("","")
    for ihist in reversed(templates[0:2]):
        hs.Add(ihist)
        print 'histo added', ihist.GetName()
    if h_VLQ.GetMaximum() > hs.GetMaximum() :
        hs.SetMaximum(h_VLQ.GetMaximum()+6)#+3
        
    #h_nonTop = h_top.Clone()
    #h_nonTop.Reset()
    #h_nonTop.Add(h_other,1)
    #h_nonTop.Add(h_zjet,1)

    #h_bkg = h_top.Clone()
    #h_bkg.Reset()
    #h_bkg.Add(h_top)
    #h_bkg.Add(h_zjet)
    #h_bkg.Add(h_other)
    #h_bkg.SetMarkerSize(0)
    #h_bkg.SetLineWidth(2)
    #h_bkg.SetFillColor(14)
    #h_bkg.SetLineColor(0)
    #h_bkg.SetFillStyle(3244)#3244,3345
    #leg.AddEntry(h_bkg,'Uncertainty','f')

 
    ## add flat uncertainties to total background
    #for ibin in range(0,nBins+1):
    #    iTot    = h_total.GetBinContent(ibin)
    #    ierrTot = h_total.GetBinError(ibin)
    #    iTop = h_top.GetBinContent(ibin)
    #    iNonTop = h_nonTop.GetBinContent(ibin)
    #    new_err = ierrTot*ierrTot + (0.5*iNonTop)**2 +(0.1*iTop)**2
    #    #print iTot
    #    #h_bkg.SetBinError(ibin, TMath.Sqrt(new_err))

    ## Canvas
    #c1 = TCanvas('c1', 'c1', 1000, 800)
    #prepareCanvas(c1)
    #c1.cd(1)
    #gPad.SetLogy()
    #hs.SetMinimum(0.1)

    #hs.Draw("Hist")
    #h_bkg.Draw("e2 same")
    #h_data.Draw("esame")
    #h_LQD.Draw("hist,same")
    #leg.Draw()

    #xTitle = 'S_{T}(GeV)'
    #setTitle(h_top, hs, xTitle)
    #gPad.RedrawAxis()
    
    #ll = TLatex()
    #ll.SetNDC(kTRUE)
    #ll.SetTextSize(0.04)
    #ll.DrawLatex(0.1,0.92, "CMS Preliminary, #sqrt{s} = 8 TeV, #it{e + jets}");

    
    #c1.cd(2)
    # add the systematic band
    #h_ratio = h_data.Clone()
    #h_ratio_bkg = h_data.Clone()
    #h_ratio_bkg.SetDirectory(0)
    #h_ratio.SetDirectory(0)
    #h_ratio.Divide(h_data, h_total)
    #h_ratio_bkg.Divide(h_bkg, h_total)
    
    #prepareRatio(h_ratio, h_ratio_bkg, xTitle)

    #line = TLine(bMin, 1, bMax, 1)
    #h_ratio.Draw("")
    #h_ratio.GetXaxis().SetTitle(xTitle)
    #h_ratio_bkg.SetTitle("")
    #h_ratio_bkg.Draw("e2same")
    #h_ratio.Draw("same")
    #line.Draw()
