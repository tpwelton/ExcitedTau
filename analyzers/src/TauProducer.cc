// system include files
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
// new includes
#include "DataFormats/PatCandidates/interface/Tau.h"

class TauProducer : public edm::stream::EDFilter<> { // what is stream?
   public:
      explicit TauProducer(const edm::ParameterSet&);
   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<std::vector<pat::Tau>> tauToken;
      bool applyFilter;
      double minpt, maxeta;
};

TauProducer::TauProducer(const edm::ParameterSet& iConfig)
{
   produces<std::vector<pat::Tau>>("goodTaus");
   tauToken = consumes<std::vector<pat::Tau>>(iConfig.getParameter<edm::InputTag>("tauCollection")); 
   applyFilter = iConfig.getParameter<bool>("applyFilter");
   maxeta = iConfig.getParameter<double>("maxeta");
   minpt = iConfig.getParameter<double>("minpt");
}

bool TauProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   auto goodTaus = std::make_unique<std::vector<pat::Tau>>();

   edm::Handle<std::vector<pat::Tau>> taus;
   iEvent.getByToken(tauToken, taus);

   //https://twiki.cern.ch/CMS/TauIDRecommendation13TeV
   for (auto i = taus->begin(); i != taus->end(); ++i) {
      if (i->pt()>=minpt && std::abs(i->eta())<maxeta) {
         //if (i->tauID("againstElectronVLooseMVA6") && i->tauID("againstMuonLoose3")) {
         //   if (i->tauID("byVLooseIsolationMVArun2v1DBoldDMwLT") && i->tauID("decayModeFinding")) {
         if (i->tauID("byMediumDeepTau2017v2p1VSjet") && i->tauID("decayModeFindingNewDMs")) {
            if (i->tauID("byVVVLooseDeepTau2017v2p1VSe") && i->tauID("byVLooseDeepTau2017v2p1VSmu")) {
               goodTaus->push_back(*i);
            }
         }
      }
   }

   const size_t nTaus = goodTaus->size();
   iEvent.put(std::move(goodTaus), std::string("goodTaus")); 
   if (applyFilter) return nTaus;
   return true;
}

DEFINE_FWK_MODULE(TauProducer);
