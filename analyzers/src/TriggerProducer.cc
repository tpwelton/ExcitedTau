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
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include <TTree.h>
#include <iostream>

class TriggerProducer : public edm::stream::EDFilter<> {
   public:
      explicit TriggerProducer(const edm::ParameterSet&);
   private:
      virtual bool filter(edm::Event&, const edm::EventSetup&) override;
      bool applyFilter;
      edm::EDGetTokenT<edm::TriggerResults> triggerBits_;
      edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescales_;
      std::vector<std::string> triggerList;
      std::vector<std::string> triggerList_HT;
      std::vector<std::string> triggerList_HTMHT;
      std::vector<std::string> triggerList_MET;
 
      TTree * tree;
      std::vector<std::string> triggerName;
      std::vector<int> triggerFire;
      std::vector<int> triggerPrescale;
      bool HLT_HT, HLT_HT_p;
      bool HLT_HTMHT, HLT_HTMHT_p;
      bool HLT_MET, HLT_MET_p;
};

TriggerProducer::TriggerProducer(const edm::ParameterSet& iConfig)
{
   triggerBits_ = consumes<edm::TriggerResults>(iConfig.getParameter<edm::InputTag>("bits"));
   triggerPrescales_ = consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("prescales"));
   triggerList = iConfig.getParameter<std::vector<std::string>>("triggerList");
   triggerList_HT = iConfig.getParameter<std::vector<std::string>>("triggerList_HT");
   triggerList_HTMHT = iConfig.getParameter<std::vector<std::string>>("triggerList_HTMHT");
   triggerList_MET = iConfig.getParameter<std::vector<std::string>>("triggerList_MET");

   edm::Service<TFileService> fs; 
   tree = fs->make<TTree>("tree", "tree");
   tree->Branch("triggerName", &triggerName);
   tree->Branch("triggerFire", &triggerFire);
   tree->Branch("triggerPrescale", &triggerPrescale);
   tree->Branch("HLT_HT", &HLT_HT, "HLT_HT/O");
   tree->Branch("HLT_HT_p", &HLT_HT_p, "HLT_HT_p/O");
   tree->Branch("HLT_HTMHT", &HLT_HTMHT, "HLT_HTMHT/O");
   tree->Branch("HLT_HTMHT_p", &HLT_HTMHT_p, "HLT_HTMHT_p/O");
   tree->Branch("HLT_MET", &HLT_MET, "HLT_MET/O");
   tree->Branch("HLT_MET_p", &HLT_MET_p, "HLT_MET_p/O"); 
}

bool TriggerProducer::filter(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<edm::TriggerResults> triggerBits;
   iEvent.getByToken(triggerBits_, triggerBits);
   const edm::TriggerNames &names = iEvent.triggerNames(*triggerBits);

   edm::Handle<pat::PackedTriggerPrescales> triggerPrescales;
   iEvent.getByToken(triggerPrescales_, triggerPrescales);

   std::vector<std::string> triggerName_;
   std::vector<int> triggerFire_;
   std::vector<int> triggerPrescale_;
   
   //for (unsigned int i = 0; i < triggerBits->size(); ++i) {
   //   const std::string name = names.triggerName(i);
      //const bool accept = triggerBits->accept(i);
   //   const int prescale = triggerPrescales->getPrescaleForIndex(i);
   //   std::cout << "trigger " << i << ", name " << name << ", prescale " << prescale << std::endl;
   //}

   bool pass = false;
   for (auto i = triggerList.begin(); i != triggerList.end(); ++i) {
      const std::string name1 = *i;
      triggerName_.push_back(name1);
      int temppass = -1;
      int tempprescale = -1;
      for (unsigned int j = 0; j < triggerBits->size(); ++j) {
         const std::string name2 = names.triggerName(j);
         if (name2.find(name1) != std::string::npos) {
            temppass = triggerBits->accept(j);
            tempprescale = triggerPrescales->getPrescaleForIndex(j);
            break;
         }
      }
      //if (temppass==-1) std::cout << "missing trigger: " << name1 << std::endl;
      triggerFire_.push_back(temppass);
      pass = pass || (temppass==1);
      triggerPrescale_.push_back(tempprescale);
   }

   HLT_HT = HLT_HT_p = false;
   for (auto i = triggerList_HT.begin(); i != triggerList_HT.end(); ++i) {
      const std::string name1 = *i;
      for (unsigned int j = 0; j < triggerBits->size(); ++j) {
         const std::string name2 = names.triggerName(j);
         if (name2.find(name1) != std::string::npos) {
            if (triggerPrescales->getPrescaleForIndex(j)==1) {
               HLT_HT = HLT_HT || triggerBits->accept(j);
               break;
            } else {
               HLT_HT_p = HLT_HT_p || triggerBits->accept(j);
               break;
            }
         }
      }
   }

   HLT_HTMHT = HLT_HTMHT_p = false;
   for (auto i = triggerList_HTMHT.begin(); i != triggerList_HTMHT.end(); ++i) {
      const std::string name1 = *i;
      for (unsigned int j = 0; j < triggerBits->size(); ++j) {
         const std::string name2 = names.triggerName(j);
         if (name2.find(name1) != std::string::npos) {
            if (triggerPrescales->getPrescaleForIndex(j)==1) {
               HLT_HTMHT = HLT_HTMHT || triggerBits->accept(j);
               break;
            } else {
               HLT_HTMHT_p = HLT_HTMHT_p || triggerBits->accept(j);
               break;
            }
         }
      }
   }  

   HLT_MET = HLT_MET_p = false;
   for (auto i = triggerList_MET.begin(); i != triggerList_MET.end(); ++i) {
      const std::string name1 = *i;
      for (unsigned int j = 0; j < triggerBits->size(); ++j) {
         const std::string name2 = names.triggerName(j);
         if (name2.find(name1) != std::string::npos) {
            if (triggerPrescales->getPrescaleForIndex(j)==1) {
               HLT_MET = HLT_MET || triggerBits->accept(j);
               break;
            } else {
               HLT_MET_p = HLT_MET_p || triggerBits->accept(j);
               break;
            }
         }
      }
   }  

   if (applyFilter) {
      if (!(pass||HLT_HT||HLT_HT_p||HLT_HTMHT||HLT_HTMHT_p||HLT_MET||HLT_MET_p)) {
          return false;
      }
   }

   triggerFire = triggerFire_;
   triggerName = triggerName_;
   triggerPrescale = triggerPrescale_;

   tree->Fill();
   return true;
}

DEFINE_FWK_MODULE(TriggerProducer);
