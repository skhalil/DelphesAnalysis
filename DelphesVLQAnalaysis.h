#include <iostream>
#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <vector>
#include <string>
#include <TString.h>
#include <utility>
#include <fstream>

// Header file for the classes stored in the TTree if any.
#include "TClonesArray.h"
#include "TObject.h"
#include "TLorentzVector.h"
#include "TRef.h"
#include "TRefArray.h"
#include "TClass.h"
#include "TSystem.h"

using namespace std;

//R__ADD_INCLUDE_PATH(delphes)
#ifdef __CLING__
R__LOAD_LIBRARY(delphes/libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootTreeWriter.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#include "external/ExRootAnalysis/ExRootTreeBranch.h"

#else
class ExRootTreeReader;
class ExRootResult;
#endif

class DelphesVLQAnalysis {
public:
   TString inputString;
   ifstream fileList;
   const char *inputFile;
   TChain *inChain = new TChain();
   //TFileCollection* fl = new TFileCollection("Infile", "", ;

   Long64_t allEntries;

   ExRootTreeReader *treeReader;
   
   Long64_t entry;
   
   const MissingET *met;
   const Electron *elec, *ele1;
   const Muon *muon, *mu1;
   const Jet *jet, *corrJet, *jet1, *bjet, *ak8jet;
   const GenParticle *partLep, *partEle, *partMu, *partJet;   
  
   TClonesArray *branchEvent;
   TClonesArray *branchElectron;
   TClonesArray *branchMuonTight;
   TClonesArray *branchJet;
   TClonesArray *branchJetAK8;
   TClonesArray *branchScalarHT;
   TClonesArray *branchMissingET;
   TClonesArray *branchParticle;
   TClonesArray *branchGenJet;

   vector<const Electron*>   *electrons = new vector<const Electron*>();
   vector<const Muon*>           *muons = new vector<const Muon*>();
   vector<const Jet*>         *goodjets = new vector<const Jet*>();
   vector<const Jet*>             *jets = new vector<const Jet*>();
   vector<const Jet*>            *bjets = new vector<const Jet*>();
   vector<const Jet*>            *fjets = new vector<const Jet*>();
   vector<const Jet*>          *ak8jets = new vector<const Jet*>();

   

   DelphesVLQAnalysis();
   ~DelphesVLQAnalysis();

   virtual void Init(const char *inString, const char *outFileName);
   virtual void LoadChain();
   virtual void Loop();
   template<typename T>
   void CollectionFilter(const TClonesArray& inColl, vector<T*>& outColl, Double_t ptMin, Double_t etaMax, Double_t isoMax);
   template<typename T>
   Bool_t Overlaps(const Jet& jet, const vector<T*>& lepColl, Double_t drMax);
   template<typename T>
   //SKBool_t Overlaps2D(vector<const Jet*>* jets, const T* lep, Double_t drMax, Double_t ptrelMin);
   Bool_t Overlaps2D(vector<const Jet*> &jets, const T* lep, Double_t drMax, Double_t ptrelMin);
   template<typename T>
   TLorentzVector OverlapConstituents(const Jet& jet, const vector<T*>& lepColl, Double_t drMax);

   bool SolveNuPz(const TLorentzVector &vlep, const TLorentzVector &vnu, double wmass, double& nuz1, double& nuz2);
   void AdjustEnergyForMass(TLorentzVector& v, double mass);

   TLorentzVector leptonP4, mostForwardJetP4, nearestJetP4, jetP4Raw, jetP4,
                  nuP4; 
   
   //book histo
   void bookHisto(); 
   std::map<TString, TH1F*> hName;
   std::map<TString, TH2F*> hName2D;
   std::map<TString, TProfile*> prName;
   
   void h1D(const char* name,   const char* title,
            const char* xTitle, const char* yTitle,
            Int_t       nBinsX, Double_t    xLow, Double_t xUp);
   void h1D(const char* name,   const char* title,
            const char* xTitle, const char* yTitle,
            Int_t       nBinsX, const Float_t* xBins);
   void h2D(const char* name,   const char* title,
            const char* xTitle, const char* yTitle,
            Int_t nBinsX, Double_t xLow, Double_t xUp,
            Int_t nBinsY,Double_t yLow, Double_t yUp);
   void h1P(const char* name,     const char* title,
            const char* xTitle,   const char* yTitle,
            Int_t       nBinsX,   Double_t    xLow, Double_t xUp);

   //output file
   TFile *outFile;
   void writeHisto();

};

DelphesVLQAnalysis::DelphesVLQAnalysis(){
   // Init();
   //Loop();  
};

DelphesVLQAnalysis::~DelphesVLQAnalysis(){};


void DelphesVLQAnalysis::Init(const char *inString, const char *outFileName){
   inputString = inString;
   inChain->SetName("Delphes");
   //inChain->Add("/uscms_data/d2/skhalil/Delphes/macro/tt-4p-0-600-v1510_14TEV_100645887_PhaseII_Substructure_200PU_seed100645888_1of1.root");
   
   LoadChain();
   
   treeReader = new ExRootTreeReader(inChain);
   
   allEntries = treeReader->GetEntries();
   cout << "** Chain contains " << allEntries << " events" << endl;
   
   branchEvent                 = treeReader->UseBranch("Event");
   branchElectron              = treeReader->UseBranch("Electron");
   branchMuonTight             = treeReader->UseBranch("MuonTight");
   branchJet                   = treeReader->UseBranch("JetPUPPI");
   branchJetAK8                = treeReader->UseBranch("JetAK8");
   branchScalarHT              = treeReader->UseBranch("ScalarHT");
   branchMissingET             = treeReader->UseBranch("MissingET");
   branchParticle              = treeReader->UseBranch("Particle");
   branchGenJet                = treeReader->UseBranch("GenJet");
   
   bookHisto();

   TString str = outFileName + std::string(".root");
   char * outName = (char*) str.Data();
   outFile = new TFile(outName, "RECREATE");
   
   cout << "INITIALIZED!" << endl;    
   return;
}

void DelphesVLQAnalysis::LoadChain(){
   cout << endl << "ADDING FILES:" << endl;
   char* inString = (char*) inputString.Data();
   
   if(inputString.Contains(".root", TString::kIgnoreCase)){
      cout << inputString << endl;
      inChain->Add(inputString);
   }
   else if(inputString.Contains(".txt", TString::kIgnoreCase)){
      fileList = ifstream(inputString);
      std::string line;
      while(std::getline(fileList, line)){
         if (line.length()==0) continue;
         cout << line << endl;
         inChain->Add(TString(line));
      }
   }
   else if(gSystem->OpenDirectory(inputString)){
      
      char* dir = gSystem->ExpandPathName(inString);
      void* dirp = gSystem->OpenDirectory(dir);
      
      const char* entry;
      const char* filename;
      TString str;
      
      while((entry = (char*)gSystem->GetDirEntry(dirp))) {
         str = entry;
         if (str.Contains(".root", TString::kIgnoreCase)){
            cout << inputString + "/" + str << endl;
            inChain->Add(inputString + "/" + str);
         }
      }
   }
   return;
}

template<typename T>
void DelphesVLQAnalysis::CollectionFilter(const TClonesArray& inColl ,vector<T*>& outColl, Double_t ptMin, Double_t etaMax, Double_t isoMax){
   const TObject *object;
   for (Int_t i = 0; i < inColl.GetEntriesFast(); i++){
      object = inColl.At(i);
      const T *t = static_cast<const T*>(object);
      if(t->P4().Pt() < ptMin) continue;
      if(TMath::Abs(t->P4().Eta()) > etaMax) continue;
      if(t->IsolationVarRhoCorr > isoMax) continue;
      outColl.push_back(t);
   }
}

template<typename T>
Bool_t DelphesVLQAnalysis::Overlaps(const Jet& jet, const vector<T*>& lepColl, Double_t drMax)
{
   Int_t i;
   Bool_t overlaps = false;
   Float_t dr;

   const TObject *object;
   // loop over filtered electrons
   for(i = 0; i < lepColl.size(); i++){
     object = lepColl.at(i);
 
     const T *t = static_cast<const T*>(object);
     dr = jet.P4().DeltaR(t->P4());
     if(dr < drMax) overlaps = true;
   }

   return overlaps;
}

template<typename T>
Bool_t DelphesVLQAnalysis::Overlaps2D(vector<const Jet*> &jets, const T* lep, Double_t drMax, Double_t ptrelMin)
{
   Int_t i;
   Bool_t overlaps = false;
   const T *t = static_cast<const T*>(lep);

   // loop over all jets
   for(i = 0; i < jets.size(); i++){

     Float_t dr = jets.at(i)->P4().DeltaR(t->P4());
     TVector3 jetp3 = (jets.at(i)->P4()).Vect();
     TVector3 lepp3 = (t->P4()).Vect();
     Float_t dPtRel = (jetp3.Cross( lepp3 )).Mag()/ jetp3.Mag();
    
     if(dr < drMax && dPtRel < ptrelMin) overlaps = true;    
     break;

   }
   return overlaps;
}

template<typename T>
TLorentzVector DelphesVLQAnalysis::OverlapConstituents(const Jet& jet, const vector<T*>& lepColl, Double_t drMax){

  jetP4  = jet.P4();
  const TObject *object, *jobject;

  // loop over filtered lepton(s)
  for(int i = 0; i < lepColl.size(); i++){
    object = lepColl.at(i);

    if(object == 0) continue;
    const T *t = static_cast<const T*>(object);
    double lepID = t->GetUniqueID();
    //partLep = (GenParticle*) t->Particle.GetObject();

    // Loop over all jet's constituents 
    Float_t dr(999.), jetID(0.);
    for(int j = 0; j < jet.Constituents.GetEntriesFast(); ++j){
      jobject = jet.Constituents.At(j);

      if(jobject == 0) continue;      
      jetID = jobject->GetUniqueID();
      /*
         if(jobject->IsA() == GenParticle::Class()){
         partJet = (GenParticle*) jobject;
         dr = partJet->P4().DeltaR(partLep->P4());
         }       
         else if(object->IsA() == Track::Class()){
         track = (Track*) object;

         dr = track->P4().DeltaR(partLep->P4());
         }
         else if(object->IsA() == Tower::Class()){
         tower = (Tower*) object;
         dr = tower->P4().DeltaR(partLep->P4());
         }
         */
      // pick those which matches to lepton
      //if(dr < drMax) { 
      if(lepID == jetID){  
        //cout << "before: "<< jetP4.Pt() <<endl;   
        if (t->P4().E() >= jetP4.E()){ // force to zero if lepton energy is more than or equal to jet energy
          jetP4.SetPxPyPzE(0.,0.,0.,0.);
        }
        else {
          jetP4 -= t->P4(); // else correct jet P4
        }
        //cout << "after: "<< jetP4.Pt() <<endl;
        break;
      }

    }//for constituents
    break;// assuming only one lepton
    }
    return jetP4;
  }

  bool DelphesVLQAnalysis::SolveNuPz(const TLorentzVector &vlep, const TLorentzVector &vnu, double wmass, double& nuz1, double& nuz2){
    bool discrimFlag = true;
    double x = vlep.X()*vnu.X() + vlep.Y()*vnu.Y() + wmass*wmass/2;
    double a = vlep.Z()*vlep.Z() - vlep.E()*vlep.E();
    double b = 2*x*vlep.Z();
    double c = x*x - vnu.Perp2() * vlep.E()*vlep.E();
    double d = b*b - 4*a*c;

    if (d < 0){
      d = 0; discrimFlag = false;
    }
    nuz1 = (-b + sqrt(d))/2/a;
    nuz2 = (-b - sqrt(d))/2/a;
    if (abs(nuz1) > abs(nuz2)){
      swap (nuz1, nuz2);
    }
    return discrimFlag;
  }

  // Adjust the energy component of V (leaving the 3-vector part unchanged).
  void DelphesVLQAnalysis::AdjustEnergyForMass(TLorentzVector& v, double mass){
    v.SetE(sqrt(v.Vect().Mag2() + mass*mass));
  }

  void DelphesVLQAnalysis::h1D(const char* name, const char* title,
      const char* xTitle, const char* yTitle,
      Int_t       nBinsX, Double_t    xLow, Double_t xUp){
    TH1F* h = new TH1F(name, title, nBinsX, xLow, xUp);
    h->GetXaxis()->SetTitle(xTitle);
    h->GetYaxis()->SetTitle(yTitle);
    h->Sumw2();
    hName[name] = h;
  }

  void DelphesVLQAnalysis::h1D(const char* name, const char* title,
      const char* xTitle, const char* yTitle,
      Int_t       nBinsX, const Float_t* xBins)
  {
    TH1F* h = new TH1F(name, title, nBinsX, xBins);
    h->GetXaxis()->SetTitle(xTitle);
    h->GetYaxis()->SetTitle(yTitle);
    h->Sumw2();
    hName[name] = h;
  }

  void DelphesVLQAnalysis::h2D(const char* name,   const char* title,
      const char* xTitle, const char* yTitle,
      Int_t nBinsX, Double_t xLow, Double_t xUp,
      Int_t nBinsY,Double_t yLow, Double_t yUp){
    TH2F* h = new TH2F(name, title, nBinsX, xLow, xUp, nBinsY, yLow, yUp);
    h->GetXaxis()->SetTitle(xTitle);
    h->GetYaxis()->SetTitle(yTitle);
    h->Sumw2();
    hName2D[name] = h;
  }

  void DelphesVLQAnalysis::h1P(const char* name,   const char* title,
      const char* xTitle, const char* yTitle,
      Int_t       nBinsX, Double_t    xLow, Double_t xUp){
    TProfile* pr = new TProfile(name, title, nBinsX, xLow, xUp);
    pr->GetXaxis()->SetTitle(xTitle);
    pr->GetYaxis()->SetTitle(yTitle);
    prName[name] = pr;
  }

  void DelphesVLQAnalysis::writeHisto(){
    outFile->cd();
    for (std::map<TString,TH1F*>::iterator it=hName.begin(); it!=hName.end(); it++) {
      hName[it->first]->Write();
    }
    for (std::map<TString,TH2F*>::iterator it=hName2D.begin(); it!=hName2D.end(); it++){
      hName2D[it->first]->Write();
    }
    for (std::map<TString, TProfile*>::iterator it=prName.begin(); it!=prName.end(); it++){
      prName[it->first]->Write();
    }
    outFile->Close();
    delete outFile;
  }


