#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "DelphesVLQAnalaysis.h"


void DelphesVLQAnalysis::Loop(){
   Int_t i = 0, j = 0, ncut = 0, ntot = 0;
   Double_t lepIso(-10.0);
   for(entry=0; entry < allEntries; ++entry){
      
      if(entry%1000 == 0) cout << entry << endl;
      ntot++;
      //if (ntot > 1000) break;
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
      
      // Select leptons with pT, |eta|, and Iso cuts
      CollectionFilter(*branchElectron,  *electrons , 30.0 , 4.0, 100);//100.
      CollectionFilter(*branchMuonTight, *muons     , 30.0 , 4.0, 100);//100.
      
      // 2 - N ele or muon >= 1
      if (electrons->size() + muons->size() != 1) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
     
      // Lepton P4
      if(electrons->size() > 0) {
         leptonP4 = electrons->at(0)->P4();
         ele1 = electrons->at(0);
         lepIso = ele1->IsolationVarRhoCorr;   
      }
      else {
         leptonP4 = muons->at(0)->P4();
         mu1 = muons->at(0);
         lepIso = mu1->IsolationVarRhoCorr;
      }
      
      Float_t dR(-100.0),dRMin(999.0);
      Float_t eta(999.0);
      
      // Apply jet cleaning 
      for(i = 0; i < branchJet->GetEntriesFast(); i++){
         jet = (Jet*)branchJet->At(i);
         jetP4 = jet->P4();  
         eta = jetP4.Eta();
         /*
         // -------------------- under development ------------------------
         // if reconstructed jet and lepton are close by, go deep to see if 
         // the jet consitutuents match with lepton and correct the jet P4
         // --------------------------------------------------------------- 

         if(electrons->size() > 0  && (Overlaps(*jet, *electrons, 0.4)) ){
            jetP4Raw = OverlapConstituents(*jet, *electrons, 0.4);
         }
         else if (muons->size() > 0  && (Overlaps(*jet, *muons, 0.4)) ){
            jetP4Raw = OverlapConstituents(*jet, *muons, 0.4);
         }
         else{
            jetP4Raw.SetPtEtaPhiE(jetP4.Pt(),jetP4.Eta(),jetP4.Phi(),jetP4.E());
         }
         
         if (jetP4Raw.Pt() == 0) continue;

         //reset jet P4 
         //cout<< "before " << jetP4.Pt() <<","<<jetP4.Eta()<<","<<jetP4.Phi()<<","<<jetP4.E()<<endl;         
         jetP4.SetPtEtaPhiE(jetP4Raw.Pt(), jetP4Raw.Eta(), jetP4Raw.Phi(), jetP4Raw.E());
         //cout<< "after " << jetP4.Pt() <<","<<jetP4.Eta()<<","<<jetP4.Phi()<<","<<jetP4.E() <<endl;
         // do sort out jets w.r.t pt later? 

         // ---------------------------------------------------------------
         */
         if(jetP4.Pt() < 30.0)                 continue;
         if(TMath::Abs(eta) > 5.0)             continue;
        
         //traditional jet cleaning for isolated jets
         //DMif(Overlaps(*jet, *electrons, 0.4))   continue;
         //DMif(Overlaps(*jet, *muons, 0.4))       continue;


         //find the min_dR(l,j)
         dR = jetP4.DeltaR(leptonP4);
         if (dR < dRMin){
            nearestJetP4 = jetP4;
            dRMin = dR;
         } 
         goodjets->push_back(jet);
      }
      
      // - Store 2d isolation variables 
      Float_t ptRel = nearestJetP4.Perp( leptonP4.Vect() );
      TVector3 nearestJet_v3 = nearestJetP4.Vect();
      TVector3 lepton_v3 = leptonP4.Vect();
      Float_t dPtRel = (nearestJet_v3.Cross( lepton_v3 )).Mag()/ nearestJet_v3.Mag();
      hName["hPtRel"]->Fill(ptRel, evtwt);
      hName["hDPtRel"]->Fill(dPtRel, evtwt);
      hName["hDRMin"]->Fill(dRMin, evtwt); 
      prName["prPtRelDRMin"]->Fill(ptRel, dRMin, evtwt);
      hName2D["h2DdPtRelDRMin"]->Fill(dRMin, dPtRel, evtwt);

      if(Overlaps2D(goodjets, ele1, 0.4, 30.)) continue;
      if(Overlaps2D(goodjets, mu1 , 0.4, 30.)) continue;

      // 3 - dPtRel >= 40? May be too tight?
      //DMif (dPtRel < 10. && dRMin < 0.1) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt); 

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
      
      hName["hMet"]-> Fill (met->P4().Pt()); 
     
      // 9 - Require MET > 30 GeV
      if(met->P4().Pt() < 30) continue;
      ncut++; 
      hName["hEff"]->Fill(ncut, evtwt);       
     
      hName["hLepIso"]->Fill(lepIso, evtwt);
      hName["hLepPt"]-> Fill (leptonP4.Pt(), evtwt);
      hName["hLepEta"]-> Fill (leptonP4.Eta(), evtwt);

      // - HT and ST variables:
      //HT = (ScalarHT*)  branchScalarHT->At(0);
      Float_t HT(0.), ST(0.);
      for(i = 0; i < jets->size(); ++i){
         HT += jets->at(i)->P4().Pt();
      }
   
      hName["hHT"]->Fill(HT);
      ST = HT + leptonP4.Pt() + met->P4().Pt();
      hName["hST"]->Fill(ST);
      
      // 9 - Require ST > 600 GeV
      if(ST <= 600) continue;
      ncut++;
      hName["hEff"]->Fill(ncut);

      // ----------------------------------------------
      // Top mass reconstruction for semileptonic case
      // ----------------------------------------------
      // first find the neutrino pz given that a real soloution exist
      nuP4 = met->P4();
      double sol1 = 0, sol2 = 0;
      bool isNuPz = SolveNuPz(leptonP4, nuP4, 80.4, sol1, sol2);
      //now reset the P4 of neutrino
      if (isNuPz){
         nuP4.SetPz(sol1);
         AdjustEnergyForMass(nuP4, 0.);
      }
      
  
      //cout << "next event " << endl;   
   }//event loop
   writeHisto();

   
   cout<<"------------------------------------"<<endl;
   cout<<""<<endl;
   cout<<"1) All events            :  "<<hName["hEff"]->GetBinContent(1)<<endl;
   cout<<"2) Exactly 1 lepton      :  "<<hName["hEff"]->GetBinContent(2)<<endl;
   cout<<"3) #Delta p_{T,rel}      :  "<<hName["hEff"]->GetBinContent(3)<<endl;
   cout<<"4) >= 1 fwd jet          :  "<<hName["hEff"]->GetBinContent(4)<<endl;
   cout<<"5) >= 3 cent jets        :  "<<hName["hEff"]->GetBinContent(5)<<endl;
   cout<<"6) 1st jet pt            :  "<<hName["hEff"]->GetBinContent(6)<<endl;
   cout<<"7) 2nd jet pt            :  "<<hName["hEff"]->GetBinContent(7)<<endl; 
   cout<<"8) >= 1 b-jet            :  "<<hName["hEff"]->GetBinContent(8)<<endl;
   cout<<"9) MET > 30 GeV          :  "<<hName["hEff"]->GetBinContent(9)<<endl;
   cout<<"10) ST > 600 GeV         :  "<<hName["hEff"]->GetBinContent(10)<<endl;
  
   cout<<""<<endl;
   cout<<"------------------------------------"<<endl;
   
}

//
void DelphesVLQAnalysis::bookHisto(){
   cout << "Book Histograms for sample = " << endl;
   h1D("hEff", "hEff", "cutFlow", "Event", 10, 0.5,10.5);
   const int nCuts = 10;
   const char *cuts[nCuts] = {"Total", 
                              "== 1 lep", 
                              "#Delta p_{T,rel} > 10",
                              "N(fwd jet) #geq 1", 
                              "N(jet) #geq 3", 
                              "leading jet pt > 100", 
                              "2nd jet pt > 50",
                              "N(b jet) #geq 1", 
                              "MET #geq 30", 
                              "S_{T} #geq 600"};
   for (int i=1;i<=nCuts;i++) hName["hEff"]->GetXaxis()->SetBinLabel(i,cuts[i-1]);

   h1D("hLepIso", "LepIso", "LepIso", "Events", 200, 0, 5);
   h1D("hLepPt", "p_{T}(e/#mu)", "p_{T}(e/#mu) [GeV]", "Events/20 GeV", 50, 0.0,400.0);
   h1D("hLepEta", "#eta(e/#mu)", "#eta(e/#mu)", "Events", 40, -5.0,5.0);
   h1D("hDRMin", "#Delta R_{MIN}", "#Delta R_{MIN}(l,j)", "Events", 30, 0.0,3.0);
   h1D("hPtRel", "p_{T}^{REL}","p_{T}^{REL} [GeV]", "Events/20 GeV", 50, 0, 100);
   h1D("hDPtRel", "#Delta p_{T}^{REL}","#Delta p_{T}^{REL} [GeV]", "Events/20 GeV", 50, 0, 100);
   h1P("prPtRelDRMin", "p_{T}^{REL}", "p_{T}^{REL} (#Delta R_{MIN}(l,j) ) [GeV]", "Events/2 [GeV]", 50, 0, 100); 
   h2D("h2DdPtRelDRMin", "h2DdPtRelDRMin", "#Delta R_{MIN}(l,j)", "#Delta p_{T}^{REL} [GeV]", 50, 0.0, 1.0, 25., 0., 500.);
   h1D("hForwardJetPt", "FwdJetPt", "FwdJetPt [GeV}", "Events/100 GeV", 60, 0, 600);
   h1D("hForwardJetEta","hForwardJetEta", "#eta(MostFwdjet)", "#eta(MostFwdjet)", 50, -5.0, 5.0);
   h1D("hNFJets", "hNFJets", "nfFwdJets", "nfFwdJets", 4, 0.5, 4.5);
   h1D("hNJets", "nJets", "nJets", "Events", 10, 0.5, 10.5);
   h1D("hLeadingJetPt", "Jet1Pt", "Jet1Pt [GeV]", "Events/100 GeV", 80, 0, 800);
   h1D("hSecLeadingJetPt", "Jet2Pt", "Jet2Pt [GeV]", "Events/100 GeV", 60, 0, 600);
   h1D("hNbjets", "nbjets", "nbjets", "Events", 6, 0.5, 6.5);
   h1D("hbJetPt", "bJetPt", "bJetPt [GeV]", "Events/100 GeV", 80, 0, 800);
   h1D("hbJetEta", "#eta(bjets)", "#eta(bjets)", "Events", 50, -5.0, 5.0);
   h1D("hMet", "hMet", "E_{T}^{miss} [GeV]", "Events/40 GeV", 50, 0,200);
   h1D("hHT","H_{T}","H_{T} [GeV]","Events/200 GeV", 70, 0, 1400);
   h1D("hST", "S_{T}", "S_{T} [GeV]", "Events/200 GeV", 100, 0, 2000); 
   
}
