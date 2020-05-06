#include <cmath>
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/GetterOfProducts.h"
#include "FWCore/Framework/interface/ProcessMatch.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// new includes 
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include <TTree.h>
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::PtEtaPhiMLorentzVectorD PolarLorentzVector;
#include <TLorentzVector.h>

const reco::Candidate * stable_copy(const reco::Candidate * part){
  if (part->status() < 3) return part;
  const reco::Candidate * part2 = 0;
  for (unsigned int i = 0; i < part->numberOfDaughters(); i++){
    if (part->pdgId() == part->daughter(i)->pdgId()){
      part2 = stable_copy(part->daughter(i));
      break;
    }
  }
  if (part2 == nullptr) part2 = part; 
  return part2;
}

class GenSignalAnalyzer : public edm::EDAnalyzer {
public:
   explicit GenSignalAnalyzer(const edm::ParameterSet&);
private:
   void analyze(const edm::Event&, const edm::EventSetup&);
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genParticleToken_;
   edm::EDGetTokenT<std::vector<pat::MET>> metToken_;
   TTree * tree;
   double photon_pt, photon_eta, photon_phi;
   double excited_pt, excited_eta, excited_phi, excited_mass;
   double deexcited_pt, deexcited_eta, deexcited_phi, deexcited_mass;
   double deexcitedvis_pt, deexcitedvis_eta, deexcitedvis_phi, deexcitedvis_mass;
   double spectator_pt, spectator_eta, spectator_phi, spectator_mass;
   double spectatorvis_pt, spectatorvis_eta, spectatorvis_phi, spectatorvis_mass;
   unsigned int deexcited_dm, spectator_dm;
   double MET_pt, MET_eta, MET_phi, MET_mass;
   double photon_rest_p, photon_rest_pt;
};

GenSignalAnalyzer::GenSignalAnalyzer(const edm::ParameterSet& iConfig)
{
   genParticleToken_ = consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genParticleCollection"));
   metToken_ = consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("metCollection"));

   edm::Service<TFileService> fs;
   tree = fs->make<TTree>("tree", "tree");
   // excited tau
   tree->Branch("excited_pt", &excited_pt, "excited_pt/D");
   tree->Branch("excited_eta", &excited_eta, "excited_eta/D");
   tree->Branch("excited_phi", &excited_phi, "excited_phi/D");
   tree->Branch("excited_mass", &excited_mass, "excited_mass/D");
    // photon
   tree->Branch("photon_pt", &photon_pt, "photon_pt/D");
   tree->Branch("photon_eta", &photon_eta, "photon_eta/D");
   tree->Branch("photon_phi", &photon_phi, "photon_phi/D");
   tree->Branch("photon_rest_p", &photon_rest_p, "photon_rest_p/D");
   tree->Branch("photon_rest_pt", &photon_rest_pt, "photon_rest_pt/D");
   // deexcited tau
   tree->Branch("deexcited_pt", &deexcited_pt, "deexcited_pt/D");
   tree->Branch("deexcited_eta", &deexcited_eta, "deexcited_eta/D");
   tree->Branch("deexcited_phi", &deexcited_phi, "deexcited_phi/D");
   tree->Branch("deexcited_mass", &deexcited_mass, "deexcited_mass/D");
   // deexcited visible tau
   tree->Branch("deexcitedvis_pt", &deexcitedvis_pt, "deexcitedvis_pt/D");
   tree->Branch("deexcitedvis_eta", &deexcitedvis_eta, "deexcitedvis_eta/D");
   tree->Branch("deexcitedvis_phi", &deexcitedvis_phi, "deexcitedvis_phi/D");
   tree->Branch("deexcitedvis_mass", &deexcitedvis_mass, "deexcitedvis_mass/D");
   tree->Branch("deexcited_dm", &deexcited_dm, "deexcited_dm/b");
   // spectator tau
   tree->Branch("spectator_pt", &spectator_pt, "spectator_pt/D");
   tree->Branch("spectator_eta", &spectator_eta, "spectator_eta/D");
   tree->Branch("spectator_phi", &spectator_phi, "spectator_phi/D");
   tree->Branch("spectator_mass", &spectator_mass, "spectator_mass/D");
   // spectator visible tau
   tree->Branch("spectatorvis_pt", &spectatorvis_pt, "spectatorvis_pt/D");
   tree->Branch("spectatorvis_eta", &spectatorvis_eta, "spectatorvis_eta/D");
   tree->Branch("spectatorvis_phi", &spectatorvis_phi, "spectatorvis_phi/D");
   tree->Branch("spectatorvis_mass", &spectatorvis_mass, "spectatorvis_mass/D");
   tree->Branch("spectator_dm", &spectator_dm, "spectator_dm/b");
   // MET
   tree->Branch("MET_pt", &MET_pt, "MET_pt/D");
   tree->Branch("MET_eta", &MET_eta, "MET_eta/D");
   tree->Branch("MET_phi", &MET_phi, "MET_phi/D");
   tree->Branch("MET_mass", &MET_mass, "MET_mass/D");
}

void GenSignalAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<std::vector<reco::GenParticle>> genParticles;
   iEvent.getByToken(genParticleToken_, genParticles);
   
   PolarLorentzVector photon(0., 0., 0., 0.);
   PolarLorentzVector excited(0., 0., 0., 0.);
   PolarLorentzVector deexcited(0., 0., 0., 0.);
   PolarLorentzVector spectator(0., 0., 0., 0.);
// for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
//    const unsigned int id = std::abs(i->pdgId());
//    if (id==4000015) excited = i->p4();
//    if (i->mother()) {
//       const unsigned int mid = std::abs(i->mother()->pdgId());
//       if (id==22 && mid==4000015) photon = i->p4();
//       if (id==15 && mid==4000015) deexcited = i->p4();
//       if (id==15 && mid!=4000015 && mid!=15) spectator = i->p4();
//    }
// }
  const reco::Candidate * mother = 0; 
  for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
    const unsigned int id = std::abs(i->pdgId());
    if (id!=4000015) continue;
    if (mother == nullptr) mother = i->mother();
    if (!i->isLastCopy()) continue;
    excited = i->p4();
    int numDaughters = i->numberOfDaughters();
    for (int j = 0; j < numDaughters; j++){
      const reco::Candidate * d = i->daughter(j);
      int did = std::abs(d->pdgId());
      if (did == 15){
        const reco::Candidate * stable_deexcited = stable_copy(d);
        deexcited = stable_deexcited->p4();
      }
      if (did == 22){
        const reco::Candidate * stable_photon = stable_copy(d);
        photon = stable_photon->p4();
      }
    }
  }
  for (auto i = genParticles->begin(); i != genParticles->end(); ++i){
    if (i->mother() != mother) continue;
    if (std::abs(i->pdgId()) != 15) continue;
    if (i->numberOfDaughters() > 0){
      const reco::Candidate * stable_spectator = stable_copy(i->daughter(0)->mother());
      spectator = stable_spectator->p4();
    }
    else{
      spectator = i->p4();
    }
  }
   

   PolarLorentzVector deexcitedvis(0., 0., 0., 0.);
   PolarLorentzVector spectatorvis(0., 0., 0., 0.);
   for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {

   }

   // photon
   photon_pt = photon.pt();
   photon_eta = photon.eta();
   photon_phi = photon.phi(); 
   // excited tau
   excited_pt = excited.pt();
   excited_eta = excited.eta();
   excited_phi = excited.phi();
   excited_mass = excited.mass();
   // deexcited tau
   deexcited_pt = deexcited.pt();
   deexcited_eta = deexcited.eta();
   deexcited_phi = deexcited.phi();
   deexcited_mass = deexcited.mass();
   // deexcited visible tau
   deexcitedvis_pt = deexcitedvis.pt();
   deexcitedvis_eta = deexcitedvis.eta();
   deexcitedvis_phi = deexcitedvis.phi();
   deexcitedvis_mass = deexcitedvis.mass();
   // spectator tau
   spectator_pt = spectator.pt();
   spectator_eta = spectator.eta();
   spectator_phi = spectator.phi();
   spectator_mass = spectator.mass();
   // spectator visible tau
   spectatorvis_pt = spectatorvis.pt();
   spectatorvis_eta = spectatorvis.eta();
   spectatorvis_phi = spectatorvis.phi();
   spectatorvis_mass = spectatorvis.mass();

   edm::Handle<std::vector<pat::MET>> met;
   iEvent.getByToken(metToken_, met);
   MET_pt = met->at(0).genMET()->pt();
   MET_eta = met->at(0).genMET()->eta();
   MET_phi = met->at(0).genMET()->phi();
   MET_mass = met->at(0).genMET()->mass();

   // photon in rest frame of excited tau
   TLorentzVector photon_tlv;
   photon_tlv.SetPtEtaPhiM(photon_pt, photon_eta, photon_phi, 0.);
   TLorentzVector excited_tlv;
   excited_tlv.SetPtEtaPhiM(excited_pt, excited_eta, excited_phi, excited_mass);
   const TVector3 excited_frame = -1*excited_tlv.BoostVector();
   photon_tlv.Boost(excited_frame);
   photon_rest_p = photon_tlv.P();
   photon_rest_pt = photon_tlv.Pt();

   tree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenSignalAnalyzer);
