#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
//#include <vector>
//#include <TChain.h>
//#include <TFileCollection.h>
//#include <TString.h>
//#include <TFile.h>
//#include <TTree.h>
//#include <TH1F.h>
//#include "TCanvas.h"
//#include "THStack.h"
#include "DelphesVLQAnalaysis.h"


void DelphesVLQAnalysis::Loop(){
   Int_t i = 0, j = 0, ncut = 0, ntot = 0;
   Double_t lepIso(-10.0);
   for(entry=0; entry < allEntries; ++entry){
      
      if(entry%1000 == 0) cout << entry << endl;
      ntot++;
      //if(ntot>210) break;
      ncut = 0;
      treeReader->ReadEntry(entry);
      
      HepMCEvent *event = (HepMCEvent*)  branchEvent->At(0);
      double evtwt = event->Weight;

      electrons -> clear();
      muons     -> clear();
      goodjets  -> clear();
      jets      -> clear();
      bjets     -> clear();
      fjets     -> clear();
      ak8jets   -> clear();
      
       // 1 - fill all events
      ncut++;
      hName["hEff"] -> Fill (ncut, evtwt);
      
      // access MissingET
      met = (MissingET*)branchMissingET->At(0);
      
      // Select leptons with pT > 50 GeV,|eta| < 4.0 and iso < 100
      CollectionFilter(*branchElectron,  *electrons , 30.0 , 4.0, 100.);//0.1
      CollectionFilter(*branchMuonTight, *muons     , 30.0 , 4.0, 100.);//0.1
      
      // 2 - N ele or muon >= 1
      if (electrons->size() + muons->size() != 1) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
     
      // Lepton P4
      if(electrons->size() > 0) {
         leptonP4 = electrons->at(0)->P4();
         ele1 = electrons->at(0);
         lepIso = ele1->IsolationVar;   
      }
      else {
         leptonP4 = muons->at(0)->P4();
         mu1 = muons->at(0);
         lepIso = mu1->IsolationVar;
      }
      
      Float_t dR(-100.0),dRMin(999.0);
      Float_t eta(999.0);
      
      // Apply jet cleaning (jets also contain non-isolated leptons at this level)
      for(i = 0; i < branchJet->GetEntriesFast(); i++){
         jet = (Jet*)branchJet->At(i);
         eta = jet->P4().Eta();
         if(jet->P4().Pt() < 30.0)             continue;
         if(TMath::Abs(eta) > 5.0)             continue;
         
        //traditional jet cleaning for non-isolated jets
         if(Overlaps(*jet, *electrons, 0.4))   continue;
         if(Overlaps(*jet, *muons, 0.4))       continue;
      
         //find the min_dR(l,j)
         dR = jet->P4().DeltaR(leptonP4);
         if (dR < dRMin){
            nearestJetP4 = jet->P4();
            dRMin = dR;
         }
         goodjets->push_back(jet);
      }
      
      // - Store 2d isolation variables 
      Float_t ptRel = nearestJetP4.Perp( leptonP4.Vect() );
      hName["hPtRel"]->Fill(ptRel, evtwt);
      hName["hDRMin"]->Fill(dRMin, evtwt); 
      prName["prPtRelDRMin"]->Fill(ptRel, dRMin, evtwt);
      hName2D["h2DPtRelDRMin"]->Fill(ptRel, dRMin, evtwt);

      // 3 - ptRel >= 40
      if (ptRel < 40.) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt); 
      hName["hLepIso"]->Fill(lepIso, evtwt);
      hName["hLepPt"]-> Fill (leptonP4.Pt(), evtwt);
      hName["hLepEta"]-> Fill (leptonP4.Eta(), evtwt);

      // separate the jets into central and forward jet collections
      Float_t eta1(999.0), etaMax(0.0);
      for(j = 0; j < goodjets->size(); ++j){
         jet1 = goodjets->at(j);
         eta1 = jet1->P4().Eta();
         if(TMath::Abs(eta1) < 2.4) {
            jets->push_back(jet1);
         }
         else {
            fjets->push_back(jet1);
            if (TMath::Abs(eta1) > TMath::Abs(etaMax)){
               mostForwardJetP4 = jet1->P4();
               etaMax = eta1;
            }
         }
      } //good jet loop
      
      if(etaMax != 0){
         hName["hForwardJetPt"]->Fill( mostForwardJetP4.Pt(), evtwt);
         hName["hForwardJetEta"]->Fill( etaMax, evtwt);
      }
      hName["hNFJets"]->Fill(fjets->size(), evtwt);
     
      // 4 - Require at least one forward jet:
      if (fjets->size() < 1) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
 
      hName["hNJets"]->Fill(jets->size(), evtwt);
      
      // 5 - Require Njets >= 3 central
      if(jets->size() < 3) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
     
      Float_t jet1Pt = jets->at(0)->P4().Pt();
      hName["hLeadingJetPt"]->Fill(jet1Pt, evtwt);

      // 6 - Require leading jet pt > 100 GeV
      if(jet1Pt <= 100) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);

      // 7 - Require second leading jet pt > 50 GeV
      Float_t jet2Pt = jets->at(1)->P4().Pt();
      hName["hSecLeadingJetPt"]->Fill(jet2Pt, evtwt);
      if(jet2Pt <= 50) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);

      // Require Nbjets >= 1 according to tight working point (bit 0 = L / bit 1 = M / bit 2 = T)
      Int_t nb = 0;
      for(i = 0; i < goodjets->size(); ++i){
         jet1 = goodjets->at(i);
         Bool_t BtagOk_medium = ( jet1->BTag & (1 << 2) );
         if(BtagOk_medium) {
            nb++;
            bjets->push_back(jet1);
            hName["hbJetPt"]->Fill(jet1->P4().Pt(), evtwt);
            hName["hbJetEta"]->Fill(jet1->P4().Eta(), evtwt);
         }
      }
      hName["hNbjets"]->Fill(nb, evtwt);

      // 8 - Require Nbjets >= 1
      if(nb == 0) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
      
      //==================
      //preselection done, fill some histograms
      //==================  

  
      
   }//event loop
   writeHisto();
}

//
void DelphesVLQAnalysis::bookHisto(){
   cout << "Book Histograms for sample = " << endl;
   h1D("hEff", "hEff", "cutFlow", "Event", 10, 0.5,10.5);
   const int nCuts = 10;
   const char *cuts[nCuts] = {"Total", 
                              "== 1 lep", 
                              "p_{T,rel} > 40",
                              "N(fwd jet) #geq 1", 
                              "N(jet) #geq 3", 
                              "leading jet pt > 100", 
                              "2nd jet pt > 50",
                              "N(b jet) #geq 1", 
                              "MET #geq 30", 
                              "S_{T} #geq 600"};
   for (int i=1;i<=nCuts;i++) hName["hEff"]->GetXaxis()->SetBinLabel(i,cuts[i-1]);

   h1D("hLepIso", "LepIso", "LepIso", "Events", 200, 0, 5);
   h1D("hLepPt", "hLepPt", "p_{T}(e/#mu)", "p_{T}(e/#mu) [GeV]", 50, 0.0,400.0);
   h1D("hLepEta", "hLepEta", "#eta(e/#mu)", "#eta(e/#mu)", 40, -5.0,5.0);
   h1D("hDRMin", "hDRMin", "#Delta R_{MIN}", "#Delta R_{MIN}(l,j)", 30, 0.0,3.0);
   h1D("hPtRel", "hPtRel", "p_{T}^{REL}","p_{T}^{REL} [GeV]", 50, 0, 100);
   h1P("prPtRelDRMin", "prPtRelDRMin", "p_{T}^{REL} [GeV]", "#Delta R_{MIN}(l,j)", 50, 0, 100); 
   h2D("h2DPtRelDRMin", "h2DPtRelDRMin", "p_{T}^{REL} [GeV]", "#Delta R_{MIN}(l,j)", 50, 0, 100, 50, 0.0,5.0);
   h1D("hForwardJetPt", "hForwardJetPt", "FwdJetPt", "FwdJetPt [GeV}", 60, 0, 600);
   h1D("hForwardJetEta","hForwardJetEta", "#eta(MostFwdjet)", "#eta(MostFwdjet)", 50, -5.0, 5.0);
   h1D("hNFJets", "hNFJets", "nfFwdJets", "nfFwdJets", 4, 0.5, 4.5);
   h1D("hNJets", "hNJets", "nJets", "nJets", 10, 0.5, 10.5);
   h1D("hLeadingJetPt", "hLeadingJetPt", "Jet1Pt", "Jet1Pt [GeV]", 80, 0, 800);
   h1D("hSecLeadingJetPt", "hSecLeadingJetPt", "Jet2Pt", "Jet2Pt [GeV]", 60, 0, 600);
   h1D("hNbjets", "hNbjets", "nbjets", "nbjets", 6, 0.5, 6.5);
   h1D("hbJetPt", "hbJetPt", "bJetPt", "bJetPt [GeV]", 80, 0, 800);
   h1D("hbJetEta", "hbJetEta", "#eta(bjets)", "#eta(bjets)", 50, -5.0, 5.0);
   h1D("hHT","H_{T}","H_{T} [GeV]","Events/ 200 GeV", 70, 0, 1400);
   
}
