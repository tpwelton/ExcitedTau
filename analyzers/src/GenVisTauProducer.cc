// system include files
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// new includes
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::PtEtaPhiMLorentzVectorD PolarLorentzVector;
#include <TTree.h>
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"

class GenVisTauProducer : public edm::EDProducer {
public:
	explicit GenVisTauProducer(const edm::ParameterSet&);
private:
   void produce(edm::Event&, const edm::EventSetup&) override;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genParticleTok_;
   TTree * tree;
   double leadvis_pt, leadvis_eta, leadvis_phi, leadvis_mass;
   double leadinv_pt, leadinv_eta, leadinv_phi, leadinv_mass;
   double sublvis_pt, sublvis_eta, sublvis_phi, sublvis_mass;
   double sublinv_pt, sublinv_eta, sublinv_phi, sublinv_mass;
   int visPlus_n, invPlus_n, visMinus_n, invMinus_n;
   double photon_pt, photon_eta, photon_phi;
   int leadvis_pdgid, sublvis_pdgid;
   int dm;
   double vismass, mass;
   double visvisdr, leadvisphotondr, subleadvisphotondr;
   //signal
   double leadphotondr, subleadphotondr;
};

GenVisTauProducer::GenVisTauProducer(const edm::ParameterSet& iConfig)
{
   edm::InputTag genParticleTag_ = iConfig.getParameter<edm::InputTag>("genParticleCollection");
   genParticleTok_ = consumes<std::vector<reco::GenParticle>>(genParticleTag_);
   produces<pat::CompositeCandidateCollection>("genVisTaus");
   produces<pat::CompositeCandidateCollection>("genInvTaus");

   edm::Service<TFileService> fs;
   tree = fs->make<TTree>("tree", "tree");
   // lead (visible) daughter
   tree->Branch("leadvis_pt", &leadvis_pt, "leadvis_pt/D");
   tree->Branch("leadvis_eta", &leadvis_eta, "leadvis_eta/D");
   tree->Branch("leadvis_phi", &leadvis_phi, "leadvis_phi/D");
   tree->Branch("leadvis_pdgid", &leadvis_pdgid, "leadvis_pdgid/I");
   tree->Branch("leadinv_pt", &leadinv_pt, "leadinv_pt/D");
   tree->Branch("leadinv_eta", &leadinv_eta, "leadinv_eta/D");
   tree->Branch("leadinv_phi", &leadinv_phi, "leadinv_phi/D");
   // sublead (visible) daughter
   tree->Branch("sublvis_pt", &sublvis_pt, "sublvis_pt/D");
   tree->Branch("sublvis_eta", &sublvis_eta, "sublvis_eta/D");
   tree->Branch("sublvis_phi", &sublvis_phi, "sublvis_phi/D");
   tree->Branch("sublvis_pdgid", &sublvis_pdgid, "sublvis_pdgid/I");
   tree->Branch("sublinv_pt", &sublinv_pt, "sublinv_pt/D");
   tree->Branch("sublinv_eta", &sublinv_eta, "sublinv_eta/D");
   tree->Branch("sublinv_phi", &sublinv_phi, "sublinv_phi/D");
   // else
   tree->Branch("dm", &dm, "dm/I"); 
   tree->Branch("vismass", &vismass, "vismass/D");
   tree->Branch("mass", &mass, "mass/D");
   tree->Branch("visvisdr", &visvisdr, "visvisdr/D");
   tree->Branch("leadvisphotondr", &leadvisphotondr, "leadvisphotondr/D");
   tree->Branch("subleadvisphotondr", &subleadvisphotondr, "subleadvisphotondr/D");
   tree->Branch("visPlus_n", &visPlus_n, "visPlus_n/I");
   tree->Branch("invPlus_n", &invPlus_n, "invPlus_n/I");
   tree->Branch("visMinus_n", &visMinus_n, "visMinus_n/I");
   tree->Branch("invMinus_n", &invMinus_n, "invMinus_n/I"); 
   // photon
   tree->Branch("photon_pt", &photon_pt, "photon_pt/D");
   tree->Branch("photon_eta", &photon_eta, "photon_eta/D");
   tree->Branch("photon_phi", &photon_phi, "photon_phi/D");
}

void GenVisTauProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   pat::CompositeCandidate visPlus;
   PolarLorentzVector visPlus_(0., 0., 0., 0.);
   bool elePlus = false;
   bool muoPlus = false;

   pat::CompositeCandidate visMinus;
   PolarLorentzVector visMinus_(0., 0., 0., 0.);
   bool eleMinus = false;
   bool muoMinus = false;

   pat::CompositeCandidate invPlus;
   PolarLorentzVector invPlus_(0., 0., 0., 0.);

   pat::CompositeCandidate invMinus;
   PolarLorentzVector invMinus_(0., 0., 0., 0.);

   edm::Handle<std::vector<reco::GenParticle>> genParticles;
   iEvent.getByToken(genParticleTok_, genParticles);
 
   photon_pt = photon_eta = 0.;
   for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
      if (i->pdgId()==22 && i->mother()) {
         if (std::abs(i->mother()->pdgId())==4000015) {
            photon_pt = i->pt();
            photon_eta = i->eta();
            photon_phi = i->phi();
         }
      }
   }

   invMinus_n = visMinus_n = invPlus_n = visPlus_n = 0;
   for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
      const int id = std::abs(i->pdgId());
      bool goodid = id==12||id==14||id==16||id==11||id==13||id==22||id==211||id==111||id==321;
      goodid = goodid || 323; // hack
      if (goodid && i->mother()) {
         if (std::abs(i->mother()->pdgId())==15) {
            if (i->mother()->charge()<0) {
               if (id==12||id==14||id==16) {
                  invMinus.addDaughter(*i);
                  invMinus_ += i->polarP4();
                  ++invMinus_n;
               } else {
                  visMinus.addDaughter(*i);
                  visMinus_ += i->polarP4();
                  ++visMinus_n;
               }
               if (id==11) eleMinus=true;
               if (id==13) muoMinus=true;
            }
            if (i->mother()->charge()>0) {
               if (id==12||id==14||id==16) {
                  invPlus.addDaughter(*i);
                  visPlus_ += i->polarP4();
                  ++invPlus_n;
               } else {
                  visPlus.addDaughter(*i);
                  visPlus_ += i->polarP4();
                  ++visPlus_n;
               }
               if (id==11) elePlus=true;
               if (id==13) muoPlus=true;
            }
         }
      }
   }

   visMinus.setP4(visMinus_);
   visPlus.setP4(visPlus_);
   invMinus.setP4(invMinus_);
   invPlus.setP4(invPlus_);

   visvisdr = reco::deltaR(visMinus, visPlus);

   //(condition) ? (if_true) : (if_false)

   if (eleMinus) {
      visMinus.setName("electron");
      invMinus.setName("electron");
      visMinus.setPdgId(11);
      invMinus.setPdgId(11);
   } else if (muoMinus) {
      visMinus.setName("muon");
      invMinus.setName("muon");
      visMinus.setPdgId(13);
      invMinus.setPdgId(13);
   } else {
      visMinus.setName("hadronic");
      invMinus.setName("hadronic");
      visMinus.setPdgId(15);
      invMinus.setPdgId(15);
   }
   if (elePlus) {
      visPlus.setName("electron");
      invPlus.setName("electron");
      visPlus.setPdgId(11);
      invPlus.setPdgId(11);
   } else if (muoPlus) {
      visPlus.setName("muon");
      invPlus.setName("muon");
      visPlus.setPdgId(13);
      invPlus.setPdgId(13);
   } else {
      visPlus.setName("hadronic");
      invPlus.setName("hadronic");
      visPlus.setPdgId(15);
      invPlus.setPdgId(15); 
  }

   mass =    (visPlus_+visMinus_+invPlus_+invMinus_).mass();
   vismass = (visPlus_+visMinus_).mass();

   auto genVisTaus = std::make_unique<pat::CompositeCandidateCollection>();
   auto genInvTaus = std::make_unique<pat::CompositeCandidateCollection>(); 

   const PolarLorentzVector photon(photon_pt, photon_eta, photon_phi, 0.);

   // tau : electron : muon   
   if (visPlus.pt()>=visMinus.pt()) {

      leadvis_pt = visPlus.pt();
      leadvis_eta = visPlus.eta();
      leadvis_phi = visPlus.phi();
      leadvis_pdgid = visPlus.pdgId();
      leadinv_pt = invPlus.pt();
      leadinv_eta = invPlus.eta();
      leadinv_phi = invPlus.phi();

      sublvis_pt = visMinus.pt();
      sublvis_eta = visMinus.eta();
      sublvis_phi = visMinus.phi();
      sublvis_pdgid = visMinus.pdgId();
      sublinv_pt = invMinus.pt();
      sublinv_eta = invMinus.eta();
      sublinv_phi = invMinus.phi();

      leadvisphotondr = reco::deltaR(visPlus, photon);
      subleadvisphotondr = reco::deltaR(visMinus, photon);

      genVisTaus->push_back(visPlus);
      genVisTaus->push_back(visMinus);
      genInvTaus->push_back(invPlus);
      genInvTaus->push_back(invMinus);
   } else {
      leadvis_pt = visMinus.pt();
      leadvis_eta = visMinus.eta();
      leadvis_phi = visMinus.phi();
      leadvis_pdgid = visMinus.pdgId();
      leadinv_pt = invMinus.pt();
      leadinv_eta = invMinus.eta();
      leadinv_phi = invMinus.phi();

      sublvis_pt = visPlus.pt();
      sublvis_eta = visPlus.eta();
      sublvis_phi = visPlus.phi();
      sublvis_pdgid = visPlus.pdgId();
      sublinv_pt = invPlus.pt();
      sublinv_eta = invPlus.eta();
      sublinv_phi = invPlus.phi();

      leadvisphotondr = reco::deltaR(visMinus, photon);
      subleadvisphotondr = reco::deltaR(visPlus, photon);

      genVisTaus->push_back(visMinus);
      genVisTaus->push_back(visPlus);
      genInvTaus->push_back(invMinus);
      genInvTaus->push_back(invPlus);
   }

   // *** dm ***
   dm = 0;
   bool isel[2] = {false, false};
   bool ismu[2] = {false, false};
   for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
      if (i->mother()) {
         const int mid = i->mother()->pdgId();
         const int id = i->pdgId();
         if ((mid==15||mid==-24) && id==11) isel[0] = true;
         if ((mid==15||mid==-24) && id==13) ismu[0] = true;
         if ((mid==-15||mid==24) && id==-11) isel[1] = true;
         if ((mid==-15||mid==24) && id==-13) ismu[1] = true; 
      }
      // mu+mu->1; e+e->2; e+mu->3; mu+had->4; e+had->5; hadhad->6;
      //mu+mu
      if (ismu[0] && ismu[1]) dm = 1;
      //e+e
      if (isel[0] && isel[1]) dm = 2;
      //e+mu
      if ( (isel[0]&&ismu[1]) || (ismu[0]&&isel[1]) ) dm = 3;
      //mu+had
      if ( (ismu[0]&&!isel[1]&&!ismu[1]) || (!isel[0]&&!ismu[0]&&ismu[1]) ) dm = 4;
      //e+had
      if ( (isel[0]&&!isel[1]&&!ismu[1]) || (!isel[0]&&!ismu[0]&&isel[1]) ) dm = 5;
      //had+had
      if ( !ismu[0] && !isel[0] && !ismu[1] && !isel[1] ) dm = 6;
   }

   tree->Fill();

   iEvent.put(std::move(genVisTaus), std::string("genVisTaus"));
   iEvent.put(std::move(genInvTaus), std::string("genInvTaus"));
}

//define this as a plug-in
DEFINE_FWK_MODULE(GenVisTauProducer);

