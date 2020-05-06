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
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

class JetHTAnalyzer : public edm::EDAnalyzer {
public:
   explicit JetHTAnalyzer(const edm::ParameterSet&);
private:
   void analyze(const edm::Event&, const edm::EventSetup&);
   TH1D *h_genHT, *h_genjetPt;
   TH1D *h_HT, *h_jetPt;
   TH1D *h_quarkHT, *h_quarkPt;
   edm::EDGetTokenT<std::vector<reco::GenJet>> genjetToken_;
   edm::EDGetTokenT<std::vector<pat::Jet>> jetToken_;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genParticleToken_;
};

JetHTAnalyzer::JetHTAnalyzer(const edm::ParameterSet& iConfig)
{
   edm::Service<TFileService> fs;
   const int n = 10;
   const double x[n+1] = {0., 50., 100., 200., 300., 500., 700., 1000., 1500., 2000., 3000.};
   h_genHT = fs->make<TH1D>("h_genHT", ";HT [GeV, truth];events / bin", n, x);
   h_genjetPt = fs->make<TH1D>("h_genjetPt", ";jet p_{T} [GeV, truth];events / 20 GeV", 25, 0., 500.);
   h_HT = fs->make<TH1D>("h_HT", ";HT [GeV];events / bin", n, x);
   h_jetPt = fs->make<TH1D>("h_jetPt", ";jet p_{T} [GeV];events / 20 GeV", 25, 0., 500.);
   h_quarkHT = fs->make<TH1D>("h_quarkHT", ";HT [GeV, truth];events / bin", n, x);
   h_quarkPt = fs->make<TH1D>("h_quarkPt", ";quark p_{T} [GeV, truth];events / 20 GeV", 25, 0., 500.);
   genjetToken_ = consumes<std::vector<reco::GenJet>>(iConfig.getParameter<edm::InputTag>("genjetCollection"));
   jetToken_ = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));
   genParticleToken_ = consumes<std::vector<reco::GenParticle>>(iConfig.getParameter<edm::InputTag>("genParticleCollection"));
}

void JetHTAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   double genHT = 0.;
   edm::Handle<std::vector<reco::GenJet>> genjets;
   iEvent.getByToken(genjetToken_, genjets);
   for (auto i = genjets->begin(); i != genjets->end(); ++i) {
      genHT += i->pt();
      h_genjetPt->Fill(i->pt());
   }
   h_genHT->Fill(genHT);

   double HT = 0.;
   edm::Handle<std::vector<pat::Jet>> jets;
   iEvent.getByToken(jetToken_, jets);
   for (auto i = jets->begin(); i != jets->end(); ++i) {
      HT += i->pt();
      h_jetPt->Fill(i->pt());
   }
   h_HT->Fill(HT);

   double quarkHT = 0.;
   edm::Handle<std::vector<reco::GenParticle>> genParticles;
   iEvent.getByToken(genParticleToken_, genParticles);
   for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
      const int id = std::abs(i->pdgId());
      if ((id<=6||id==21) && i->status()==23) {
         quarkHT += i->pt();
         h_quarkPt->Fill(i->pt());
      }
   }
   h_quarkHT->Fill(quarkHT);
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetHTAnalyzer);
