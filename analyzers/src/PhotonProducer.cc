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
#include "DataFormats/PatCandidates/interface/Photon.h"

class PhotonProducer : public edm::stream::EDFilter<> {
   public:
      explicit PhotonProducer(const edm::ParameterSet&);
   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<std::vector<pat::Photon>> photonToken_;
      bool applyFilter;
      double maxeta, minpt;
};

PhotonProducer::PhotonProducer(const edm::ParameterSet& iConfig)
{
   produces<std::vector<pat::Photon>>("goodPhotons");
   photonToken_ = consumes<std::vector<pat::Photon>>(iConfig.getParameter<edm::InputTag>("photonCollection")); 
   applyFilter = iConfig.getParameter<bool>("applyFilter");
   maxeta = iConfig.getParameter<double>("maxeta");
   minpt = iConfig.getParameter<double>("minpt");
}

bool PhotonProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   auto goodPhotons = std::make_unique<std::vector<pat::Photon>>();

   edm::Handle<std::vector<pat::Photon>> photons;
   iEvent.getByToken(photonToken_, photons);

   //https://twiki.cern.ch/CMS/EgammaIDRecipesRun2
   for (auto i = photons->begin(); i != photons->end(); ++i) {
      const double eta = std::abs(i->eta());
      //const double eta = std::abs(i->superCluster().eta());
      if (i->pt()>=minpt && eta<maxeta) {
         //if (eta<1.479||eta>=1.653) {
            if (i->passElectronVeto()) {
               if (i->photonID("mvaPhoID-RunIIFall17-v1p1-wp80")) {
                  goodPhotons->push_back(*i);
               }
            }
         //}
      }
   }

   const size_t nPhotons = goodPhotons->size();
   iEvent.put(std::move(goodPhotons), std::string("goodPhotons"));  
   if (applyFilter) return nPhotons;
   return true;
}

//define this as a plug-in
DEFINE_FWK_MODULE(PhotonProducer);
