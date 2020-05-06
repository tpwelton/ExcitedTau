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

class TauFilter : public edm::stream::EDFilter<> { // what is stream?
   public:
      explicit TauFilter(const edm::ParameterSet&);
   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<std::vector<pat::Tau>> tauToken;
      double minpt, maxeta;
};

TauFilter::TauFilter(const edm::ParameterSet& iConfig)
{
   tauToken = consumes<std::vector<pat::Tau>>(iConfig.getParameter<edm::InputTag>("tauCollection")); 
   maxeta = iConfig.getParameter<double>("maxeta");
   minpt = iConfig.getParameter<double>("minpt");
}

bool TauFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<std::vector<pat::Tau>> taus;
   iEvent.getByToken(tauToken, taus);
   //https://twiki.cern.ch/CMS/TauIDRecommendation13TeV
   for (auto i = taus->begin(); i != taus->end(); ++i) {
      if (i->pt()>=minpt && std::abs(i->eta())<maxeta) {
         return true;
      }
   }
   return false;
}

DEFINE_FWK_MODULE(TauFilter);

