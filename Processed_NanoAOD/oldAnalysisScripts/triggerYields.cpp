#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"

void triggerYields(const char* file){

TFile *file0 = TFile::Open(file);
TTree *events = (TTree*)file0->Get("Events");

int num_events = events->GetEntries();

int num_ele = events->Draw("HLT_Ele32_WPTight_Gsf>>hist_ele", "HLT_Ele32_WPTight_Gsf > 0","goff");

int num_mu = events->Draw("HLT_IsoMu24>>hist_mu", "HLT_IsoMu24 > 0","goff");

int num_tau = events->Draw("HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1>>hist_tau", "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1 > 0","goff");

int num_photon = events->Draw("HLT_Photon200>>hist_photon", "HLT_Photon200 > 0", "goff");

int num_mutau = events->Draw("HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1>>hist_mutau", " HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1 > 0","goff");

int num_eletau = events->Draw("HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1>>hist_eletau", " HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1 > 0","goff");

int num_tautau = events->Draw("HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg>>hist_tautau", " HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg > 0","goff");

std::cout << num_events << " " << num_ele << " " << num_mu << " " << num_tau << " " << num_photon << " " << num_mutau << " " << num_eletau << " " << num_tautau << std::endl;
}
