#!/usr/bin/env python
import ROOT
from ROOT import gROOT,gStyle,gPad,gStyle
from ROOT import Double,kBlue,kRed,kOrange,kAzure,kMagenta,kYellow,kCyan,kGreen,kGray,kBlack,kDotted,kTRUE
import imp
import sys
from array import array
from collections import OrderedDict
gROOT.Macro("~/rootlogon.C")
gStyle.SetOptStat(0)

def getLimit(model,masses):

  print model, ' ', masses 

  grexplim = ROOT.TGraph(len(masses))
  grexp1sig = ROOT.TGraphAsymmErrors(len(masses))
  grexp2sig = ROOT.TGraphAsymmErrors(len(masses))
  
  grexplim .SetName('grexplim' +'_'+model) 
  grexp1sig.SetName('grexp1sig'+'_'+model) 
  grexp2sig.SetName('grexp2sig'+'_'+model) 
  
  for mass in masses:
    i = masses.index(mass)
    xsec = 1000.#/(0.97*0.58)
    f = ROOT.TFile.Open("limitFiles_3000_Sep20/higgsCombine_Expected_"+model+"_M"+str(mass)+".Asymptotic.mH120.root", "r")
    limit = f.Get("limit")
    entries = limit.GetEntriesFast()
    obs = 0
    exp = 0
    exp1sLow  = 0
    exp1sHigh = 0
    exp2sLow  = 0
    exp2sHigh = 0
    for e in limit:
      quant = e.quantileExpected
      lim = e.limit
      if quant == -1: obs = lim 
      elif quant > 0.024 and quant < 0.026: exp2sLow = lim 
      elif quant > 0.15 and quant < 0.17: exp1sLow = lim 
      elif quant == 0.5: exp = lim
      elif quant > 0.83 and quant < 0.85: exp1sHigh = lim
      elif quant > 0.97 and quant < 0.98: exp2sHigh = lim 
    grexplim.SetPoint(i, mass, xsec*exp)
    grexp1sig.SetPoint(i, mass, xsec*exp)
    grexp2sig.SetPoint(i, mass, xsec*exp)
    grexp1sig.SetPointError(i, 0, 0, xsec*abs(exp-exp1sLow), xsec*abs(exp1sHigh-exp))
    grexp2sig.SetPointError(i, 0, 0, xsec*abs(exp-exp2sLow), xsec*abs(exp2sHigh-exp))
    print "model %s mass %f exp %f" % (model, mass, xsec*exp)

  return grexplim, grexp1sig, grexp2sig

def plotLimits(model, masses, run2_masses, th_xs, run2_xs ):
  
  grthlim = ROOT.TGraph(len(run2_masses))
  map_th  = zip(run2_masses,th_xs)
  grRun2lim = ROOT.TGraph(len(run2_masses))
  map_run2 = zip(run2_masses,run2_xs)

  p_th=0; p_run2=0;
  for m,x in map_th:
    grthlim.SetPoint(p_th, m, x)
    p_th +=1
  
  for m,x in map_run2:
    grRun2lim.SetPoint(p_run2, m, x)
    p_run2 +=1


  grexplim, grexp1sig, grexp2sig = getLimit(model,masses)

  print grthlim.GetN(), ' ',grexplim.GetN(), ' ', grexp1sig.GetN(), ' ', grexp2sig.GetN(), ' '

  #return

  tdrstyle = imp.load_source('tdrstyle', 'tdrstyle.py')
  CMS_lumi = imp.load_source('CMS_lumi', 'CMS_lumi.py')
  ROOT.gROOT.SetBatch()
  ROOT.gROOT.SetStyle("Plain")
  ROOT.gStyle.SetOptStat()
  ROOT.gStyle.SetOptTitle(0)
  ROOT.gStyle.SetPalette(1)
  ROOT.gStyle.SetNdivisions(405,"x");
  ROOT.gStyle.SetEndErrorSize(0.)
  ROOT.gStyle.SetErrorX(0.001)
  ROOT.gStyle.SetPadTickX(1)
  ROOT.gStyle.SetPadTickY(1)

  canv = ROOT.TCanvas("ExpLimit_"+model,"ExpLimit_"+model,800,600)
  pad=canv.GetPad(0)
  pad.SetBottomMargin(.12)
  pad.SetLeftMargin(.12)
  pad.SetLogy()

  grexp2sig.SetFillColor(401)

  grexp2sig.SetLineColor(41)

  grexp1sig.SetFillColor(3)
  
  grexp1sig.SetLineColor(3)
  
  grexplim.SetLineWidth(2)

  grexplim.SetLineStyle(7)
 

  ymax = grexp2sig.GetHistogram().GetMaximum()*500.0
  ymin = grexp2sig.GetHistogram().GetMaximum()*0.01 
  print ymax, ymin
  #grthlim.SetMinimum(1.)
  #grthlim.SetMaximum(1000.)
  grthlim.SetLineStyle(kDotted)
  grthlim.SetLineColor(kBlack)
  grthlim.SetLineWidth(2)
  grthlim.SetMaximum(ymax)
  grthlim.SetMinimum(ymin)

  grRun2lim.SetLineStyle(kDotted)
  grRun2lim.SetLineColor(kRed)
  grRun2lim.SetLineWidth(2)
  grRun2lim.SetMaximum(ymax)
  grRun2lim.SetMinimum(ymin)
  
  grexplim .Draw("al")
  grexp2sig.Draw("3")
  grexp1sig.Draw("3")
  grexplim .Draw("l")
  grthlim.Draw("Lsame")
  grRun2lim.Draw("Lsame") 
  #grthlim.GetXaxis().SetRangeUser(1000.,2000.);

  grexplim.GetXaxis().SetRangeUser(999,3000)  
  grexplim.GetYaxis().SetLabelSize(0.04)
  grexplim.GetYaxis().SetTitleSize(0.04)
  grexplim.GetYaxis().SetTitleOffset(1.20)
  grexplim.GetXaxis().SetLabelSize(0.04)
  grexplim.GetXaxis().SetLabelSize(0.04)
  grexplim.GetXaxis().SetTitleSize(0.04)
  grexplim.GetXaxis().SetNdivisions(506)
  grexplim.GetXaxis().SetTitleOffset(1.12)
  grexplim.GetXaxis().SetLabelFont(62)
  grexplim.GetYaxis().SetLabelFont(62)
  grexplim.GetXaxis().SetTitleFont(62)
  grexplim.GetYaxis().SetTitleFont(62)
  grexplim.GetXaxis().SetNdivisions(510,1);
  grexplim.GetXaxis().SetTitle("M(T) [GeV]")
  if model == 'Tbj':
    grexplim.GetYaxis().SetTitle("#sigma(pp#rightarrow Tbq)#times#font[52]{B}(T#rightarrow tH) [fb]")
  elif model == 'Ttj':
    grexplim.GetYaxis().SetTitle("#sigma(pp#rightarrow Ttq)#times#font[52]{B}(T#rightarrow tH) [fb]")
  

  grexplim.SetMinimum(ymin)
  grexplim.SetMaximum(ymax)
  if model == 'Tbj':
    grexplim.SetMinimum(ymin)
    grexplim.SetMaximum(ymax)
  elif model == 'Ttj':
    grexplim.SetMinimum(ymin)
    grexplim.SetMaximum(ymax)
  
  text = ["CMS"]
  textsize = 0.028; 
  ntxt = 0
  nleglines = 5.

  xstart = 0.50;
  ystart = 0.60; 
  ystartleg = 0.95 

  #theoryline = ""
  #if model == 'Graviton':
  #  theoryline = "Bulk KK graviton (#kappa/#bar{M_{Pl}} = 0.5)"
  #if model == 'Radion':
  #  theoryline = "Radion (#Lambda_{R} = 1 TeV)"
  
  legend = ROOT.TLegend(xstart, ystart, xstart+0.45, ystartleg)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)
  legend.SetTextSize(textsize)
  legend.SetColumnSeparation(0.0)
  legend.SetEntrySeparation(0.1)
  legend.SetMargin(0.2)
  legend.SetHeader("")
  #legend.AddEntry(grtheory , theoryline,"l") 
  legend.AddEntry(grexplim  , "Expected ","l")
  legend.AddEntry(grexp1sig , "1 s.d.","f")
  legend.AddEntry(grexp2sig , "2 s.d.","f")
  legend.AddEntry(grthlim, "#sigma_{th.}#times#bf{#it{#Beta}}^{2}, c=1, #bf{#it{#Beta}}(T #rightarrow tH)=100%", "l")
  legend.AddEntry(grRun2lim, "Expected projection (13 TeV)", "l")
  legend.Draw()
  
  ### Embellishment
  CMS_lumi.lumi_13TeV = ""
  CMS_lumi.writeExtraText = 1
  CMS_lumi.extraText = "Simulation Preliminary"
   
  iPos = 11 ###HTshape
  if( iPos==0 ): CMS_lumi.relPosX = 0.12
  CMS_lumi.CMS_lumi(pad, 4, iPos)
  
  latex = ROOT.TLatex()
  latex.SetNDC()
  latex.SetTextAlign(13)
  latex.SetTextSize(0.04)
  latex.SetTextFont(62);
  latex.DrawLatex(0.68, 0.95, "3000 fb^{-1} (14 TeV)")
  
  pad.RedrawAxis()
  
  pad.Update()
  ###
  
  for end in [".pdf",".png", ".root"]:
    canv.SaveAs("ExpLim_ECFA2016_14TeV_"+model+"_12Sept2016"+end)

masses = [1000, 1500, 2000, 2500, 3000]
run2_masses = [1000, 1500, 2000]
Tbj_xs = [ 1.26309*1.950*1000., 1.32586*0.408*1000.,  1.40697*0.102*1000.]
Ttj_xs = [ 1.3044*0.203*1000.,  1.37731*0.0540*1000., 1.4631*0.0162*1000.]
run2_Tbj_xs = [0.17378*1000., 0.062428*1000., 0.041277*1000.]
run2_Ttj_xs = [0.14993*1000., 0.053423*1000., 0.039589*1000.]
model = 'Tbj'
plotLimits(model, masses, run2_masses, Tbj_xs, run2_Tbj_xs)

model = 'Ttj'
plotLimits(model, masses, run2_masses, Ttj_xs, run2_Ttj_xs)
