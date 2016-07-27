#include "TROOT.h"
#include "TSystem.h"
//#include "TApplication.h"
#include <iostream>
#include "DelphesVLQAnalaysis.C"

void RunAnalyzer(const char *inputFile, const char *outputFile){
    // REMOVE THE LINE BELOW IF NOT RUNNING IN CMSSW ENVIRONMENT
    gSystem->AddIncludePath("-I" + TString(gSystem->Getenv("CMSSW_RELEASE_BASE")) + "/src"); 
    // Analysis macro
    //gROOT->LoadMacro("DelphesVLQAnalysis.C++");

    DelphesVLQAnalysis *vlq = new DelphesVLQAnalysis;
    vlq->Init(inputFile, outputFile);

    TStopwatch ts;
    ts.Start();

    vlq->Loop();

    ts.Stop();

    std::cout << "RealTime : " << ts.RealTime()/60.0 << " minutes" << std::endl;
    std::cout << "CPUTime  : " << ts.CpuTime()/60.0 << " minutes" << std::endl;
    
}
