// system include files
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// new includes
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

class JetProducer : public edm::EDProducer {
   public:
      explicit JetProducer(const edm::ParameterSet&);
   private:
      virtual void produce(edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<std::vector<pat::Jet>> jetToken;
      double maxeta, minpt;
};

JetProducer::JetProducer(const edm::ParameterSet& iConfig)
{
   produces<std::vector<pat::Jet>>("goodJets");
   jetToken = consumes<std::vector<pat::Jet>>(iConfig.getParameter<edm::InputTag>("jetCollection"));
   maxeta = iConfig.getParameter<double>("maxeta");
   minpt = iConfig.getParameter<double>("minpt");
}

void JetProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   auto goodJets = std::make_unique<std::vector<pat::Jet>>();

   //https://twiki.cern.ch/CMS/JetID13TeVRun2018
   edm::Handle<std::vector<pat::Jet>> jets;
   iEvent.getByToken(jetToken, jets);
   for (auto i = jets->begin(); i != jets->end(); ++i) {
      if (i->pt()>=minpt && std::abs(i->eta())<maxeta) {
         const float NHF = i->neutralHadronEnergyFraction();
         const float NEMF = i->neutralEmEnergyFraction();
         const size_t NumConst = i->numberOfDaughters();
         //const float MUF = i->muonEnergyFraction();
         const float CHF = i->chargedHadronEnergyFraction();
         const int CHM = i->chargedMultiplicity();
         //const float CEMF = i->chargedEmEnergyFraction();
         //if (NHF<0.9 && NEMF<0.9 && NumConst>1 && MUF<0.8 && CHF>0. && CHM>0 && CEMF<0.8) { LepVeto
         if (NHF<0.9 && NEMF<0.9 && NumConst>1 && CHF>0. && CHM>0) {
            goodJets->push_back(*i);
         }
      }
   }
   iEvent.put(std::move(goodJets), std::string("goodJets"));
}

//define this as a plug-in
DEFINE_FWK_MODULE(JetProducer);
