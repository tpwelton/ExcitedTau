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
#include "DataFormats/PatCandidates/interface/Electron.h"

class ElectronProducer : public edm::stream::EDFilter<> {
   public:
      explicit ElectronProducer(const edm::ParameterSet&);
   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<std::vector<pat::Electron>> electronToken;
      bool applyFilter;
      double maxeta, minpt;
};

ElectronProducer::ElectronProducer(const edm::ParameterSet& iConfig)
{
   produces<std::vector<pat::Electron>>("goodElectrons");
   electronToken = consumes<std::vector<pat::Electron>>(iConfig.getParameter<edm::InputTag>("electronCollection")); 
   applyFilter = iConfig.getParameter<bool>("applyFilter");
   maxeta = iConfig.getParameter<double>("maxeta");
   minpt = iConfig.getParameter<double>("minpt");
}

bool ElectronProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   auto goodElectrons = std::make_unique<std::vector<pat::Electron>>();

   edm::Handle<std::vector<pat::Electron>> electrons;
   iEvent.getByToken(electronToken, electrons);

   //https://twiki.cern.ch/CMS/EgammaIDRecipesRun2
   for (auto i = electrons->begin(); i != electrons->end(); ++i) {
      const double eta = std::abs(i->eta());
      //const double eta = std::abs(i->superCluster.eta());
      if (i->pt()>=minpt && eta<maxeta) {
         //if (eta<1.479||eta>=1.653) {
            if (i->electronID("mvaEleID-Fall17-iso-V1-wp80")) {
               goodElectrons->push_back(*i);
            }
         //}
      }
   }

   int nElectrons = goodElectrons->size();
   iEvent.put(std::move(goodElectrons), std::string("goodElectrons"));
   if (applyFilter) return nElectrons;
   return true;
}

DEFINE_FWK_MODULE(ElectronProducer);
