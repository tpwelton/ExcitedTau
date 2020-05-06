// system include files
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// new includes
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include <TTree.h>
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

class EventAnalyzer : public edm::EDAnalyzer {
public:
	explicit EventAnalyzer(const edm::ParameterSet&);
private:
   virtual void analyze(const edm::Event&, const edm::EventSetup&);
   edm::EDGetTokenT<std::vector<pat::Photon>> photonToken_;
   edm::EDGetTokenT<std::vector<pat::Electron>> electronToken_;
   edm::EDGetTokenT<std::vector<pat::Muon>> muonToken_;
   edm::EDGetTokenT<std::vector<pat::Tau>> tauToken_;
   edm::EDGetTokenT<std::vector<reco::Vertex>> vertexToken_;
   edm::EDGetTokenT<std::vector<pat::MET>> metToken_;
   edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genParticleToken_;

   TTree * tree;
   unsigned int nPhotons;
   unsigned int nElectrons_p, nMuons_p, nTaus_p;
   unsigned int nElectrons_m, nMuons_m, nTaus_m;
   unsigned int nBJets[3], nBJets_exc[3], nJets;
   unsigned int nVertices;
   double MET_pt, MET_phi, metSignificance;
   //mc
   bool isMC;
   unsigned int nPhotons_gen, nElectrons_gen, nMuons_gen, nTaus_gen;
   double xsWeight;
};

EventAnalyzer::EventAnalyzer(const edm::ParameterSet& iConfig)
{
   photonToken_ = consumes<std::vector<pat::Photon>>(iConfig.getParameter<edm::InputTag>("photonCollection"));
   electronToken_ = consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("electronCollection"));
   muonToken_ = consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("muonCollection"));
   tauToken_ = consumes<std::vector<pat::Tau>>(iConfig.getParameter<edm::InputTag>("tauCollection"));
   vertexToken_ = consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("vertexCollection"));
   metToken_ = consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("metCollection"));
   jetToken_ = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));

   edm::Service<TFileService> fs;
   tree = fs->make<TTree>("tree", "tree");
   tree->Branch("nPhotons", &nPhotons, "nPhotons/b");
   tree->Branch("nElectrons_p", &nElectrons_p, "nElectrons_p/b");
   tree->Branch("nElectrons_m", &nElectrons_m, "nElectrons_m/b");
   tree->Branch("nMuons_p", &nMuons_p, "nMuons_p/b");
   tree->Branch("nMuons_m", &nMuons_m, "nMuons_m/b");
   tree->Branch("nTaus_p", &nTaus_p, "nTaus_p/b");
   tree->Branch("nTaus_m", &nTaus_m, "nTaus_m/b");
   tree->Branch("MET_pt", &MET_pt, "MET_pt/D");
   tree->Branch("MET_phi", &MET_phi, "MET_phi/D");
   tree->Branch("metSignificance", &metSignificance, "metSignificance/D");
   tree->Branch("nJets", &nJets, "nJets/I");
   tree->Branch("nBJets", nBJets, "nBJets[3]/I");
   tree->Branch("nBJets_exc", nBJets_exc, "nBJets_exc[3]/I");
   tree->Branch("nVertices", &nVertices, "nVertices/b");

   isMC = iConfig.getParameter<bool>("isMC");
   if (isMC) {
      genParticleToken_ = consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genParticleCollection"));
      tree->Branch("nPhotons_gen", &nPhotons_gen, "nPhotons_gen/b");
      tree->Branch("nElectrons_gen", &nElectrons_gen, "nElectrons_gen/b");
      tree->Branch("nMuons_gen", &nMuons_gen, "nMuons_gen/b");
      tree->Branch("nTaus_gen", &nTaus_gen, "nTaus_gen/b");
      xsWeight = iConfig.getParameter<double>("xsWeight");
      tree->Branch("xsWeight", &xsWeight, "xsWeight/D");
   }
}

void EventAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<std::vector<pat::Photon>> photons;
   iEvent.getByToken(photonToken_, photons);
   nPhotons = 0;
   for (auto i = photons->begin(); i != photons->end(); ++i) {
      ++nPhotons;
   }  
 
   edm::Handle<std::vector<pat::Electron>> electrons;
   iEvent.getByToken(electronToken_, electrons);
   nElectrons_p = nElectrons_m = 0;
   for (auto i = electrons->begin(); i != electrons->end(); ++i) {
      if (i->charge()>0) ++nElectrons_p;
      if (i->charge()<0) ++nElectrons_m;
   }
   
   edm::Handle<std::vector<pat::Muon>> muons;
   iEvent.getByToken(muonToken_, muons);
   nMuons_p = nMuons_m = 0;
   for (auto i = muons->begin(); i != muons->end(); ++i) {
      if (i->charge()>0) ++nMuons_p;
      if (i->charge()<0) ++nMuons_m;
   }

   edm::Handle<std::vector<pat::Tau>> taus;
   iEvent.getByToken(tauToken_, taus);
   nTaus_p = nTaus_m = 0;
   for (auto i = taus->begin(); i != taus->end(); ++i) {
      if (i->charge()>0) ++nTaus_p;
      if (i->charge()<0) ++nTaus_m;
   }

   edm::Handle<std::vector<reco::Vertex>> vertices;
   iEvent.getByToken(vertexToken_, vertices);
   nVertices = vertices->size();

   edm::Handle<std::vector<pat::MET>> met;
   iEvent.getByToken(metToken_, met);
   MET_pt = met->at(0).pt();
   MET_phi = met->at(0).phi();
   metSignificance = met->at(0).metSignificance();

   edm::Handle<std::vector<pat::Jet>> jets;
   iEvent.getByToken(jetToken_, jets);
   nJets = 0;
   nBJets[0] = nBJets[1] = nBJets[2] = 0;
   nBJets_exc[0] = nBJets_exc[1] = nBJets_exc[2] = 0;
   for (auto i = jets->begin(); i != jets->end(); ++i) {
      bool overlap = false;
      for (auto j = electrons->begin(); j != electrons->end(); ++j) {
         if (reco::deltaR(*i, *j)<0.4) overlap = true;
      }
      for (auto j = muons->begin(); j != muons->end(); ++j) {
         if (reco::deltaR(*i, *j)<0.4) overlap = true;
      }
      for (auto j = taus->begin(); j != taus->end(); ++j) {
         if (reco::deltaR(*i, *j)<0.4) overlap = true;
      }
      for (auto j = photons->begin(); j != photons->end(); ++j) {
         if (reco::deltaR(*i, *j)<0.4) overlap = true;
      }
      if (overlap) continue;
      ++nJets;  
      //https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
      const float disc = i->bDiscriminator("pfDeepCSVJetTags:probb")+i->bDiscriminator("pfDeepCSVJetTags:probbb");
      if (disc>=0.1241) ++nBJets[0];
      if (disc>=0.4184) ++nBJets[1];
      if (disc>=0.7527) ++nBJets[2];
      if (disc>=0.1241 && disc<0.4184) ++nBJets_exc[0];
      if (disc>=0.4184 && disc<0.7527) ++nBJets_exc[1];
      if (disc>=0.7527               ) ++nBJets_exc[2]; 
   }

    if (isMC) {
      nPhotons_gen = nElectrons_gen = nMuons_gen = nTaus_gen = 0;
      edm::Handle<std::vector<reco::GenParticle>> genParticles;
      iEvent.getByToken(genParticleToken_, genParticles);
      for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
         if (i->isLastCopy()) {
            const int id = std::abs(i->pdgId());
            if (id==11) ++nElectrons_gen;
            if (id==13) ++nMuons_gen;
            if (id==15) ++nTaus_gen;
            if (id==22) ++nPhotons_gen;
         }
      }
   }

   tree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(EventAnalyzer);

