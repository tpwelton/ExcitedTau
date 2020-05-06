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
#include "DataFormats/PatCandidates/interface/Muon.h"

class MuonProducer : public edm::stream::EDFilter<> {
   public:
      explicit MuonProducer(const edm::ParameterSet&);
   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      edm::EDGetTokenT<std::vector<pat::Muon>> muonToken;
      double minpt, maxeta;
      bool applyFilter;
};

MuonProducer::MuonProducer(const edm::ParameterSet& iConfig)
{
   produces<std::vector<pat::Muon>>("goodMuons");
   muonToken = consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("muonCollection")); 
   applyFilter = iConfig.getParameter<bool>("applyFilter");
   maxeta = iConfig.getParameter<double>("maxeta");
   minpt = iConfig.getParameter<double>("minpt"); 
}

bool MuonProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   auto goodMuons = std::make_unique<std::vector<pat::Muon>>();

   edm::Handle<std::vector<pat::Muon>> muons;
   iEvent.getByToken(muonToken, muons);
 
   //https://twiki.cern.ch/CMS/SWGuideMuonIdRun2
   for (auto i = muons->begin(); i != muons->end(); ++i) {
      if (i->pt()>=minpt && std::abs(i->eta())<maxeta) {
         if (i->passed(reco::Muon::CutBasedIdTight)) {
            if (i->passed(reco::Muon::PFIsoMedium)) {
               goodMuons->push_back(*i);
            }
         }
      }
   }

   const size_t nMuons = goodMuons->size();
   iEvent.put(std::move(goodMuons), std::string("goodMuons"));
   if (applyFilter) return nMuons;
   return true;
}

DEFINE_FWK_MODULE(MuonProducer);
