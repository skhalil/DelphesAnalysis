#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>
#include "DelphesVLQAnalaysis.h"
#include "BTagEfficiencyMediumOP.h"


void DelphesVLQAnalysis::Loop(){
   Int_t i = 0, j = 0, ncut = 0, ntot = 0;
   Double_t lepIso(-10.0);
   for(entry=0; entry < allEntries; ++entry){
      
      if(entry%1000 == 0) cout << entry << endl;
      ntot++;
      //if (ntot > 20000) break;
      ncut = 0;
      treeReader->ReadEntry(entry);
      
      HepMCEvent *event = (HepMCEvent*)  branchEvent->At(0);
      double evtwt = event->Weight;
       
      hName["hNGenEvents"]->Fill(1);

      electrons -> clear();
      muons     -> clear();
      goodjets  -> clear();
      jets      -> clear();
      bjets     -> clear();
      fjets     -> clear();
      ak8jets   -> clear();
      bpartons  -> clear();
      higgsjets -> clear();
      
       // 1 - fill all events
      ncut++;
      hName["hEff"] -> Fill (ncut, evtwt);
      
      // access MissingET
      met = (MissingET*)branchMissingET->At(0);
      
      // Select leptons with pT, |eta|, and Iso cuts
      CollectionFilter(*branchElectron,  *electrons , 40.0 , 4.0, 100);//100.
      CollectionFilter(*branchMuonTight, *muons     , 40.0 , 4.0, 100);//100.
      
      // 2 - N ele or muon >= 1
      if (electrons->size() + muons->size() != 1) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
     
      // Lepton P4
      if(electrons->size() > 0) {
         leptonP4 = electrons->at(0)->P4();
         ele1 = electrons->at(0);
         lepIso = ele1->IsolationVarRhoCorr; 
         partLep = (GenParticle*) ele1->Particle.GetObject();  
      }
      else {
         leptonP4 = muons->at(0)->P4();
         mu1 = muons->at(0);
         lepIso = mu1->IsolationVarRhoCorr;
         partLep = (GenParticle*) mu1->Particle.GetObject();
      }
       
      // Apply jet cleaning 
      Float_t dR(900.0), dRMin(999.0), delPtRel(999.0);
      Float_t eta(999.0);
      TVector3 jetp3, lepp3;
      
      for(i = 0; i < branchJet->GetEntriesFast(); i++){
         jet = (Jet*)branchJet->At(i);
         jetP4 = jet->P4();  
         eta = jetP4.Eta();

         if(jetP4.Pt() < 30.0)                 continue;
         if(TMath::Abs(eta) > 5.0)             continue;
           
         dR = jetP4.DeltaR(leptonP4);
         hName["hDR"]->Fill(dR, evtwt);

         jetp3 = (jet->P4()).Vect();
         lepp3 = leptonP4.Vect(); 
         delPtRel = (jetp3.Cross( lepp3 )).Mag()/ jetp3.Mag();
         hName["hDelPtRel"]->Fill(delPtRel, evtwt);
         hName2D["h2DdPtReldR"]->Fill(dR, delPtRel, evtwt);

         //find the min_dR(l,j)
         if (dR < dRMin){
            nearestJetP4 = jetP4;
            dRMin = dR;
         } 
         goodjets->push_back(jet);
      }
      /*
      //make a list of b-partons in an event:
      for(j = 0; j < branchParticle->GetEntriesFast(); ++j){
         genb = (GenParticle*) branchParticle->At(j);
         if (genb->PID == 5 || genb->PID == -5){
            bpartons->push_back(genb);
         }
      }
      */
      
      for(i = 0; i < branchJetAK8->GetEntriesFast(); i++){
         ak8jet = (Jet*)branchJetAK8->At(i);
         jetP4AK8 = ak8jet->P4(); 
       
         // quality cuts      
         if(jetP4AK8.Pt() < 300.0)                continue;
         if(TMath::Abs(jetP4AK8.Eta()) > 2.4)     continue;
         //if(electrons->size()>0 && Overlaps2D(*ak8jets, ele1, 0.4, 40.)) {cout << "hello " << endl; continue;}
         //if(muons->size()>0     && Overlaps2D(*ak8jets, mu1 , 0.4, 40.)) {cout << "hello2 " << endl; continue;}
         if(ak8jet->Tau[1]/ak8jet->Tau[0] > 0.6)  continue;
         if(ak8jet->NSubJetsSoftDropped != 2 )    continue;
         if(jetP4AK8.DeltaR(leptonP4) <= 1.0)     continue;
         if(ak8jet->SoftDroppedP4[0].M() > 160 || ak8jet->SoftDroppedP4[0].M() < 90) continue;

         /*
         //loop over gen particles and match b-partons with the subjets: SK
         double dRp1(-100.), dRp2(-100.);
         for(j = 0; j < bpartons->size(); ++j){
            b1partonP4 =  bpartons->at(j)->P4();
            dRp1 = ak8jet->SoftDroppedP4[1].DeltaR(b1partonP4);//match 1st hard subjet with a b-parton
            for(k = 0; k < bpartons->size(); ++k){
               if(j == k) continue;  
               b2partonP4 =  bpartons->at(k)->P4();
               dRp2 = ak8jet->SoftDroppedP4[2].DeltaR(b2partonP4);//match 2nd hard subjet with another b-parton
            }
         }
         if (dRp1 != -100. && dRp2 != -100.){
            cout << "dR(s1,b): " << dRp1 <<": dR(s2,b): " << dRp2 << endl;
         }
         */
         
         // fill the jets as Higgs jets
         higgsjets->push_back(ak8jet);
        
      }
      // - Store 2d isolation variables 
      Float_t ptRel = nearestJetP4.Perp( leptonP4.Vect() );
      TVector3 nearestJet_v3 = nearestJetP4.Vect();
      TVector3 lepton_v3 = leptonP4.Vect();
      Float_t dPtRel = (nearestJet_v3.Cross( lepton_v3 )).Mag()/ nearestJet_v3.Mag();
      hName["hPtRel"]->Fill(ptRel, evtwt);
      //if (dRMin>0.4){
      hName["hDPtRel"]->Fill(dPtRel, evtwt);
         //}
      hName["hDRMin"]->Fill(dRMin, evtwt); 
      //prName["prPtRelDRMin"]->Fill(ptRel, dRMin, evtwt);
      hName2D["h2DdPtRelDRMin"]->Fill(dRMin, dPtRel, evtwt);
      hName["hLepIso"]->Fill(lepIso, evtwt);
      hName["hLepPt"]-> Fill (leptonP4.Pt(), evtwt);
      hName["hLepEta"]-> Fill (leptonP4.Eta(), evtwt);

      // 3 - dPtRel >= 30 || dRMin > 0.4
      if(electrons->size()>0 && Overlaps2D(*goodjets, ele1, 0.4, 40.)) continue;
      if(muons->size()>0     && Overlaps2D(*goodjets, mu1 , 0.4, 40.)) continue;
      //if(lepIso > 0.1) continue;
      //if (dPtRel < 30. && dRMin < 0.4) continue;
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
      hName["hNJets"]->Fill(jets->size(), evtwt);
      hName["hMet"]-> Fill (met->P4().Pt(), evtwt); 

      // 4 - Require at least one forward jet:
      if (fjets->size() < 1) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
                
      // 5 - Require Njets >= 2 central
      if(jets->size() < 2) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
     
      // 6 - Require leading jet pt > 200 GeV
      Float_t jet1Pt = jets->at(0)->P4().Pt();
      Float_t jet1Eta = jets->at(0)->P4().Eta();
      hName["hLeadingJetPt"]->Fill(jet1Pt, evtwt);
      hName["hLeadingJetEta"]->Fill(jet1Eta, evtwt);
 
      if(jet1Pt <= 200) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);

      // 7 - Require second leading jet pt > 80 GeV
      Float_t jet2Pt = jets->at(1)->P4().Pt();
      Float_t jet2Eta = jets->at(1)->P4().Eta();
      hName["hSecLeadingJetPt"]->Fill(jet2Pt, evtwt);
      hName["hSecLeadingJetEta"]->Fill(jet2Eta, evtwt);

      if(jet2Pt <= 80) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);

      // b-tagging according to tight working point (bit 0 = L / bit 1 = M / bit 2 = T)
      Int_t nb = 0;
      for(i = 0; i < goodjets->size(); ++i){
         jet1 = goodjets->at(i);
         Bool_t BtagOk_medium = ( jet1->BTag & (1 << 1) );
         if(BtagOk_medium) {
            nb++;
            bjets->push_back(jet1);
         }
      }

      // 8 - Require Nbjets >= 1
      if(nb == 0) continue;
      ncut++;
      hName["hEff"]->Fill(ncut, evtwt);
       
      double btagwtup(1.), btagwtdown(1.); ////DM
      BTagEffWtMediumOP(goodjets, btagwtup, btagwtdown) ; 

      Float_t bjet1Pt = bjets->at(0)->P4().Pt();
      Float_t bjet1Eta= bjets->at(0)->P4().Eta(); 
     
      // 9 - Require MET > 20 GeV
      if(met->P4().Pt() < 20) continue;
      ncut++; 
      hName["hEff"]->Fill(ncut, evtwt);    

      // dR (jet, MET)
      Float_t dR_jet1MET = jets->at(0)->P4().DeltaR(met->P4());

      // - HT and ST variables:
      Float_t HT(0.), ST(0.);
      for(i = 0; i < jets->size(); ++i){
         HT += jets->at(i)->P4().Pt();
      }     
      ST = HT + leptonP4.Pt() + met->P4().Pt();

      //--------- Preselection done ---------------
      for(j = 0; j < higgsjets->size(); ++j){
         jetak8_1 = higgsjets->at(j);
         hName["hSoftMass"]-> Fill(jetak8_1->SoftDroppedP4[0].M(), evtwt); 
         hName["hSoftPt"]-> Fill(jetak8_1->SoftDroppedP4[0].Pt(), evtwt);
      }
      
      hName["hNbjets"]->Fill(nb, evtwt); 
      hName["hLeadingbJetPt"]->Fill(bjet1Pt, evtwt);
      hName["hLeadingbJetEta"]->Fill(bjet1Eta, evtwt);
      
      hName["hDelRJet1Met"]-> Fill (dR_jet1MET , evtwt); 
      hName["hHT"]->Fill(HT, evtwt);
      hName["hST"]->Fill(ST, evtwt);
      
      // ----------------------------------------------
      // Top mass reconstruction for semileptonic case
      // ----------------------------------------------

      // first find the neutrino pz given that a real soloution exist
      nuP4 = met->P4();
      double sol1 = 0, sol2 = 0;
      bool isNuPz = SolveNuPz(leptonP4, nuP4, 80.4, sol1, sol2);

      // take the minimum of the two soloutions, and reset the P4 of neutrino
      nuP4.SetPz(sol1);
      AdjustEnergyForMass(nuP4, 0.);

      //=================================================
      // do the magic 
      //=================================================
      double topMass = 174., higgsMass = 125., dR_Ht = 0.;
      double topMBoost(0.), higgsMBoost(0.), WMBoost(0.), TpMBoost(0.), topPtBoost(0.), higgsPtBoost(0.), WPtBoost(0.), TpPtBoost(0.);
      double topM(0.), higgsM(0.), WM(0.), TpM(0.), topPt(0.), higgsPt(0.), WPt(0.), TpPt(0.);
   
      // for boosted case:
      if (higgsjets->size() > 0 ){
         
         // 10 - boosted Higgs
         ncut++;
         hName["hEff"]->Fill(ncut, evtwt);

         DoMassRecoBoost(*jets, *higgsjets, leptonP4, nuP4, higgsMass, topMass, chi2_dR_boost, chi2_higgs_boost, chi2_top_boost);

         if (chi2_dR_boost.first != 100000.){ //read the output if event as >=2 jets 
            hName["hChi2Boost"]->Fill(chi2_dR_boost.first, evtwt);
            hName["hdR_HtBoost"]->Fill(chi2_dR_boost.second, evtwt);

            if (chi2_dR_boost.second > 2.0){
               higgsMBoost  = chi2_higgs_boost.second.M();                  
               higgsPtBoost = chi2_higgs_boost.second.Pt(); 
               topMBoost    = chi2_top_boost.second.M();                    
               topPtBoost   = chi2_top_boost.second.Pt();            
               WMBoost      = (leptonP4 + nuP4).M();                        
               WPtBoost     = (leptonP4 + nuP4).Pt();
               TpMBoost     = (chi2_higgs_boost.second + chi2_top_boost.second).M();  
               TpPtBoost    = (chi2_higgs_boost.second + chi2_top_boost.second).Pt();

               hName["hTPrimePtBoost"]->Fill(TpPtBoost, evtwt); 
               if (TpPtBoost > 100.){
                  hName["hHiggsMRecoBoost"]->Fill(higgsMBoost, evtwt);
                  hName["hHiggsPtBoost"]->Fill(higgsPtBoost, evtwt);
                  hName["hTopMRecoBoost"]->Fill(topMBoost, evtwt);
                  hName["hTopPtBoost"]->Fill(topPtBoost, evtwt);
                  hName["hWMRecoBoost"]->Fill(WMBoost, evtwt);
                  hName["hWPtRecoBoost"]->Fill(WPtBoost, evtwt);
                  hName["hTPrimeMRecoBoost"]->Fill(TpMBoost, evtwt);
                  hName["hSTBoost"]->Fill(ST, evtwt); 
               }//top pt
            }//dR cut
         }
      }
      else{//resolved case 
         DoMassReco(*jets, leptonP4, nuP4, higgsMass, topMass, chi2_dR, chi2_higgs, chi2_top);
         
         if (chi2_dR.first != 100000.){//read the output if event as >=4 jets 
            hName["hChi2"]->Fill(chi2_dR.first, evtwt);
            hName["hdR_Ht"]->Fill(chi2_dR.second, evtwt);
            if (chi2_dR.second > 2.0) {  
               higgsM  = chi2_higgs.second.M();  
               higgsPt = chi2_higgs.second.Pt();            
               topM    = chi2_top.second.M();                       
               topPt   = chi2_top.second.Pt();           
               WM      = (leptonP4 + nuP4).M();                      
               WPt     = (leptonP4 + nuP4).Pt();
               TpM     = (chi2_higgs.second + chi2_top.second).M();  
               TpPt    = (chi2_higgs.second + chi2_top.second).Pt();
               hName["hTPrimePt"]->Fill(TpPt, evtwt);
               if (TpPt > 100.){
                  hName["hHiggsMReco"]->Fill(higgsM, evtwt);
                  hName["hHiggsPt"]->Fill(higgsPt, evtwt);
                  hName["hTopMReco"]->Fill(topM, evtwt);
                  hName["hTopPt"]->Fill(topPt, evtwt);
                  hName["hWMReco"]->Fill(WM, evtwt);
                  hName["hWPtReco"]->Fill(WPt, evtwt);
                  hName["hTPrimeMReco"]->Fill(TpM, evtwt);              
                  if(nb==1) {hName["hTPrimeMReco_1bjet"]->Fill(TpM, evtwt);}
                  else      {hName["hTPrimeMReco_2bjet"]->Fill(TpM, evtwt);}
                  hName["hSTResolved"]->Fill(ST, evtwt);
               }
            }
            //qualityCutsResolved = (chi2_higgs.second.DeltaR(leptonP4) > 1.0) || (higgsM < 160 && higgsM > 90); 
         }
      //cout << "chi2: " << chi2_dR.first << ", dR: " << chi2_dR.second << ", higgs mass: " 
      //     << higgsM <<", top mass: " << TpM << ", T' mass: " << TpM << ", W mass: "<< WM << endl;
      }      


      hName["hLepIso_sig"]->Fill(lepIso, evtwt);
      hName["hLepPt_sig"]-> Fill (leptonP4.Pt(), evtwt);
      hName["hLepEta_sig"]-> Fill (leptonP4.Eta(), evtwt);
      if(etaMax != 0){
         hName["hForwardJetPt_sig"]->Fill( mostForwardJetP4.Pt(), evtwt);
         hName["hForwardJetEta_sig"]->Fill( etaMax, evtwt);
      }
      hName["hNFJets_sig"]->Fill(fjets->size(), evtwt);
      hName["hNJets_sig"]->Fill(jets->size(), evtwt);
      hName["hLeadingJetPt_sig"]->Fill(jet1Pt, evtwt);
      hName["hLeadingJetEta_sig"]->Fill(jet1Eta, evtwt); 
      hName["hSecLeadingJetPt_sig"]->Fill(jet2Pt, evtwt);
      hName["hSecLeadingJetEta_sig"]->Fill(jet2Eta, evtwt); 
      hName["hNbjets_sig"]->Fill(nb, evtwt); 
      hName["hLeadingbJetPt_sig"]->Fill(bjet1Pt, evtwt);
      hName["hLeadingbJetEta_sig"]->Fill(bjet1Eta, evtwt);
      hName["hMet_sig"]-> Fill (met->P4().Pt(), evtwt); 
      hName["hDelRJet1Met_sig"]-> Fill (dR_jet1MET , evtwt); 
      hName["hHT_sig"]->Fill(HT, evtwt);
      hName["hST_sig"]->Fill(ST, evtwt);
     
   }//event loop
   writeHisto();
   
   
   cout<<"------------------------------------"<<endl;
   cout<<""<<endl;
   cout<<"1) All events            :  "<<hName["hEff"]->GetBinContent(1)<<endl;
   cout<<"2) Exactly 1 lepton      :  "<<hName["hEff"]->GetBinContent(2)<<endl;
   cout<<"3) 2D cut                :  "<<hName["hEff"]->GetBinContent(3)<<endl;
   cout<<"4) >= 1 fwd jet          :  "<<hName["hEff"]->GetBinContent(4)<<endl;
   cout<<"5) >= 3 cent jets        :  "<<hName["hEff"]->GetBinContent(5)<<endl;
   cout<<"6) 1st jet pt            :  "<<hName["hEff"]->GetBinContent(6)<<endl;
   cout<<"7) 2nd jet pt            :  "<<hName["hEff"]->GetBinContent(7)<<endl; 
   cout<<"8) >= 1 b-jet            :  "<<hName["hEff"]->GetBinContent(8)<<endl;
   cout<<"9) MET > 20 GeV          :  "<<hName["hEff"]->GetBinContent(9)<<endl;
   cout<<"10) >= 1 higgs           :  "<<hName["hEff"]->GetBinContent(10)<<endl;
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
                              "#Delta p_{T,rel} > 30 && #Delta R(l, jet) > 0.4",
                              "N(fjet) #geq 1", 
                              "N(jet) #geq 2", 
                              "leading jet pt > 200", 
                              "2nd jet pt > 80", 
                              "N(b jet) #geq 1",
                              "MET #geq 20",                             
                              "N(Higgs) #geq 1"};
   for (int i=1;i<=nCuts;i++) hName["hEff"]->GetXaxis()->SetBinLabel(i,cuts[i-1]);

   std::vector<std::string> cat; 
   cat.push_back("_sig"); 
   cat.push_back("");

   for (int i=0; i<cat.size(); i++){
      h1D(("hLepIso"+cat[i]).c_str(), "LepIso", "LepIso", "Events", 200, 0, 5);
      h1D(("hLepPt"+cat[i]).c_str(), "p_{T}(e/#mu)", "p_{T}(e/#mu) [GeV]", "Events/20 GeV", 50, 0.0,400.0);
      h1D(("hLepEta"+cat[i]).c_str(), "#eta(e/#mu)", "#eta(e/#mu)", "Events", 40, -5.0,5.0);
      h1D(("hForwardJetPt"+cat[i]).c_str(), "FwdJetPt", "FwdJetPt [GeV}", "Events/100 GeV", 60, 0, 600);
      h1D(("hForwardJetEta"+cat[i]).c_str(),"hForwardJetEta", "#eta(MostFwdjet)", "#eta(MostFwdjet)", 50, -5.0, 5.0);
      h1D(("hNFJets"+cat[i]).c_str(), "hNFJets", "nfFwdJets", "nfFwdJets", 4, 0.5, 4.5);
      h1D(("hNJets"+cat[i]).c_str(), "nJets", "nJets", "Events", 10, 0.5, 10.5);
      h1D(("hLeadingJetPt"+cat[i]).c_str(), "Jet1Pt", "Jet1Pt [GeV]", "Events/15 GeV", 80, 0, 2000);
      h1D(("hLeadingJetEta"+cat[i]).c_str(), "#eta(jet1)", "#eta(jet1)", "Events", 50, -5.0, 5.0);
      h1D(("hSecLeadingJetPt"+cat[i]).c_str(), "Jet2Pt", "Jet2Pt [GeV]", "Events/20 GeV", 80, 0, 1600);
      h1D(("hSecLeadingJetEta"+cat[i]).c_str(), "#eta(jet2)", "#eta(jet2)", "Events", 50, -5.0, 5.0);
      h1D(("hNbjets"+cat[i]).c_str(), "nbjets", "nbjets", "Events", 6, 0.5, 6.5);
      h1D(("hLeadingbJetPt"+cat[i]).c_str(), "bJet1Pt", "bJet1Pt [GeV]", "Events/15 GeV", 80, 0, 2000);
      h1D(("hLeadingbJetEta"+cat[i]).c_str(), "#eta(bjet1)", "#eta(bjet1)", "Events", 50, -5.0, 5.0);
      h1D(("hMet"+cat[i]).c_str(), "hMet", "E_{T}^{miss} [GeV]", "Events/10 GeV", 50, 0, 500);
      h1D(("hDelRJet1Met"+cat[i]).c_str(), "hDelRJet1Met", "#DeltaR(jet, MET)", "Events/0.25 bin", 40, -2, 8);
      h1D(("hHT"+cat[i]).c_str(),"H_{T}","H_{T} [GeV]","Events/50 GeV", 80, 0, 4000);
      h1D(("hST"+cat[i]).c_str(), "S_{T}", "S_{T} [GeV]", "Events/50 GeV", 80, 0, 4000);
   }
  
   h1D("hNGenEvents", "total events", "total events", "Events", 2, 0.5, 2.5) ;
   h1D("hDRMin", "#Delta R_{MIN}(l, jet)", "#Delta R_{MIN}(l,jet)", "Events", 30, 0.0,3.0);
   h1D("hDR", "#DeltaR(l, jet)", "#Delta R(l,jet)", "Events", 30, 0.0,3.0);
   h1D("hPtRel", "p_{T}^{REL}","p_{T}^{REL} [GeV]", "Events/20 GeV", 50, 0, 100);
   h1D("hDPtRel", "#Delta p_{T}^{REL}","#Delta p_{T}^{REL} [GeV]", "Events/20 GeV", 50, 0, 100);
   h1D("hDelPtRel", "#Delta p_{T}^{REL}","#Delta p_{T}^{REL} [GeV]", "Events/20 GeV", 50, 0, 100);
   //h1P("prPtRelDRMin", "p_{T}^{REL}", "p_{T}^{REL} (#Delta R_{MIN}(l,j) ) [GeV]", "Events/2 [GeV]", 50, 0, 100);
   h2D("h2DdPtRelDRMin", "h2DdPtRelDRMin", "#Delta R_{MIN}(l,j)", "#Delta p_{T}^{REL} [GeV]", 50, 0.0, 1.0, 20., 0., 200.);
   h2D("h2DdPtReldR", "h2DdPtReldR", "#Delta R(l,j)", "#Delta p_{T}^{REL} [GeV]", 50, 0.0, 1.0, 20., 0., 200.);
   h1D("hSoftMass", "M_{softdrop}", "M_{softdrop} [GeV]", "Events/9 GeV", 50, 50.0, 500);
   h1D("hSoftPt", "Pt_{softdrop}", "Pt_{softdrop} [GeV]", "Events/40 GeV", 100, 0, 4000);
   // for boosted case
   h1D("hChi2Boost", "Chi2Boost", "#chi_{2}", "Events/10 bins", 50, 0.0, 500);
   h1D("hHiggsMRecoBoost", "Boosted M_{H,reco}", "M_{H,reco} [GeV]", "Events/9 GeV", 50, 50.0, 500);
   h1D("hHiggsPtBoost", "Boosted Higgs pt", "Higgs p_{T} [GeV]", "Events/ 20 GeV", 80, 0, 1600);
   h1D("hTopMRecoBoost", "Boosted M_{t,reco}", "M_{t,reco} [GeV]", "Events/10 GeV", 55, 50.0, 600); 
   h1D("hTopPtBoost", "Boosted Top pt", "Top p_{T} [GeV]", "Events/ 20 GeV", 80, 0, 1600);
   h1D("hWMRecoBoost", "Boosted W_{W,reco}", "M_{W,reco} [GeV]", "Events/3 GeV", 150, 50.0,500);
   h1D("hWPtRecoBoost", "Boosted W pt", "W p_{T} [GeV]", "Events/ 20 GeV", 50, 0, 1000);
   h1D("hTPrimeMRecoBoost", "Boosted M_{T,reco}", "M_{T,reco} [GeV]", "Events/36 GeV ", 100, 60.0, 3660.);
   h1D("hTPrimePtBoost", "Boosted TPrime pt", "T p_{T} [GeV]", "Events/ 20 GeV", 50, 0, 1000);
   h1D("hdR_HtBoost", "Boosted #Delta R(t, H)_{reco}", "#Delta R(t, H)_{reco}", "Events",  25, 0, 5);
   h1D("hSTBoost", "S_{T}, boosted", "S_{T} [GeV]", "Events/50 GeV", 80, 0, 4000);

   // for resolved case  
   h1D("hChi2", "Chi2", "#chi_{2}", "Events/10 bins", 50, 0.0, 500);
   h1D("hHiggsMReco", "M_{H,reco}", "M_{H,reco} [GeV]", "Events/9 GeV", 50, 50.0, 500);
   h1D("hHiggsPt", "Higgs pt", "Higgs p_{T} [GeV]", "Events/ 20 GeV", 80, 0, 1600);
   h1D("hTopMReco", "M_{t,reco}", "M_{t,reco} [GeV]", "Events/10 GeV", 55, 50.0, 600);   
   h1D("hTopPt", "Top pt", "Top p_{T} [GeV]", "Events/ 20 GeV", 80, 0, 1600);
   h1D("hWMReco", "W_{W,reco}", "M_{W,reco} [GeV]", "Events/3 GeV", 150, 50.0,500);
   h1D("hWPtReco", "W pt", "W p_{T} [GeV]", "Events/ 20 GeV", 50, 0, 1000);
   h1D("hTPrimeMReco", "M_{T,reco}", "M_{T,reco} [GeV]", "Events/36 GeV ", 100, 60.0, 3660.);
   h1D("hTPrimeMReco_1bjet", "M_{T,reco}, 1bjet", "M_{T,reco} [GeV]", "Events/36 GeV ", 100, 60.0, 3660.);
   h1D("hTPrimeMReco_2bjet", "M_{T,reco}, 2bjet", "M_{T,reco} [GeV]", "Events/36 GeV ", 100, 60.0, 3660.);
   h1D("hTPrimePt", "TPrime pt", "T p_{T} [GeV]", "Events/ 20 GeV", 50, 0, 1000);
   h1D("hdR_Ht", "#Delta R(t, H)_{reco}", "#Delta R(t, H)_{reco}", "Events",  25, 0, 5);
   h1D("hSTResolved", "S_{T}, resolved", "S_{T} [GeV]", "Events/50 GeV", 80, 0, 4000);
}

void DelphesVLQAnalysis::BTagEffWtMediumOP(const Jets jets, double& btagwtup, double& btagwtdown) { 

  double varmediumoplight(0.01);
  double varmediumopcharm(0.02); 
  double varmediumopbottom(0.05);

  double effall(1.), effallup(1.), effalldown(1.);

  for(i = 0; i < goodjets->size(); ++i){

     jet1 = goodjets->at(i);
     Bool_t BtagOk_medium (jet1->BTag & (1 << 1));
     double pt(jet1->P4().Pt()), eta(fabs(jet1->P4().Eta())), flav(fabs(jet1->Flavor)); 
     double effjet = EfficiencyFormulaMediumOP(flav, pt, eta);
     double effjetup(effjet), effjetdown(effjet) ; 

     if      (flav <= 3 || flav == 21) effjetup   = effjet*(1+varmediumoplight);
     else if (flav == 4)               effjetup   = effjet*(1+varmediumopcharm);
     else if (flav == 5)               effjetup   = effjet*(1+varmediumopbottom);
     if      (flav <= 3 || flav == 21) effjetdown = effjet*(1-varmediumoplight);
     else if (flav == 4)               effjetdown = effjet*(1-varmediumopcharm);
     else if (flav == 5)               effjetdown = effjet*(1-varmediumopbottom);

     if(BtagOk_medium) {
        effall     *= effjet     ; 
        effallup   *= effjetup    ;
        effalldown *= effjetdown ;
     }
     else {
        effall     *= (1-effjet)     ; 
        effallup   *= (1-effjetup)    ; 
        effalldown *= (1-effjetdown) ; 
     }
  }

  btagwtup = effallup/effall;
  btagwtdown = effalldown/effall;

  return;

}
