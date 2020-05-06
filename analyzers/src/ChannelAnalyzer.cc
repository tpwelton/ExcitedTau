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
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include <TTree.h>
#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::PtEtaPhiMLorentzVectorD PolarLorentzVector;
#include <TLorentzVector.h>
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"

double dphi(double phi1, double phi2)
{
   const double pi = 3.14159265359;
   if (phi1<2.*pi) phi1 = (phi1+2.*pi);
   if (phi2<2.*pi) phi2 = (phi2+2.*pi);
   double dphi_ = std::abs(phi2-phi1);
   if (dphi_>=pi) dphi_ = 2.*pi - dphi_;
   return dphi_;
}

class ChannelAnalyzer : public edm::EDAnalyzer {
public:
	explicit ChannelAnalyzer(const edm::ParameterSet&);
private:
   virtual void analyze(const edm::Event&, const edm::EventSetup&);
   edm::EDGetTokenT<edm::View<reco::Candidate>> photonToken_;
   edm::EDGetTokenT<edm::View<reco::Candidate>> tauToken_;
   edm::EDGetTokenT<edm::View<reco::Candidate>> leptonToken_;
   edm::EDGetTokenT<std::vector<pat::MET>> metToken_;
   double minpt_lepton, maxeta_lepton;
   double minpt_tau, maxeta_tau;
   double minpt_photon, maxeta_photon;
   int q1q2;

   TTree * tree;
   double lepton_pt, lepton_eta, lepton_phi, lepton_mass;
   double tau_pt, tau_eta, tau_phi, tau_mass;
   double ll_pt, ll_mass, ll_dr;
   double photon_pt, photon_eta, photon_phi;
   bool havePair, havePhoton, haveTriplet;
   //collinear
   double ll_cmass, ll_cpt;
   double gtau_cmass, glepton_cmass;
   double tau_cmass, lepton_cmass;
};

ChannelAnalyzer::ChannelAnalyzer(const edm::ParameterSet& iConfig)
{
   tauToken_ = consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("tauCollection"));
   leptonToken_ = consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("leptonCollection"));
   photonToken_ = consumes<edm::View<reco::Candidate>>(iConfig.getParameter<edm::InputTag>("photonCollection"));
   metToken_ = consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("metCollection"));

   minpt_lepton = iConfig.getParameter<double>("minpt_lepton");
   maxeta_lepton = iConfig.getParameter<double>("maxeta_lepton");
   minpt_tau = iConfig.getParameter<double>("minpt_tau");
   maxeta_tau = iConfig.getParameter<double>("maxeta_tau");
   minpt_photon = iConfig.getParameter<double>("minpt_photon");
   maxeta_photon = iConfig.getParameter<double>("maxeta_photon");
   q1q2 = iConfig.getParameter<int>("q1q2");
   
   edm::Service<TFileService> fs;
   tree = fs->make<TTree>("tree", "tree"); 
   tree->Branch("lepton_pt", &lepton_pt, "lepton_pt/D");
   tree->Branch("lepton_eta", &lepton_eta, "lepton_eta/D");
   tree->Branch("lepton_phi", &lepton_phi, "lepton_phi/D");
   tree->Branch("lepton_mass", &lepton_mass, "lepton_mass/D");
   tree->Branch("tau_pt", &tau_pt, "sublead_pt/D");
   tree->Branch("tau_eta", &tau_eta, "tau_eta/D");
   tree->Branch("tau_phi", &tau_phi, "tau_phi/D");
   tree->Branch("tau_mass", &tau_mass, "tau_mass/D");
   tree->Branch("ll_pt", &ll_pt, "ll_pt/D");
   tree->Branch("ll_mass", &ll_mass, "ll_mass/D"); 
   tree->Branch("ll_dr", &ll_dr, "ll_dr/D");
   tree->Branch("photon_pt", &photon_pt, "photon_pt/D");
   tree->Branch("photon_eta", &photon_eta, "photon_eta/D");
   tree->Branch("photon_phi", &photon_phi, "photon_phi/D");  
   tree->Branch("havePair", &havePair, "havePair/O");
   tree->Branch("havePhoton", &havePhoton, "havePhoton/O");
   tree->Branch("haveTriplet", &haveTriplet, "haveTriplet/O");
   // collinear
   tree->Branch("ll_cmass", &ll_cmass, "ll_cmass/D");
   tree->Branch("ll_cpt", &ll_cpt, "ll_cpt/D");
   tree->Branch("tau_cmass", &tau_cmass, "tau_cmass/D");
   tree->Branch("lepton_cmass", &lepton_cmass, "lepton_cmass/D");
   tree->Branch("gtau_cmass", &gtau_cmass, "gtau_cmass/D");
   tree->Branch("glepton_cmass", &glepton_cmass, "glepton_cmass/D");
}

void ChannelAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<edm::View<reco::Candidate>> taus;
   iEvent.getByToken(tauToken_, taus);

   edm::Handle<edm::View<reco::Candidate>> leptons;
   iEvent.getByToken(leptonToken_, leptons);
 
   edm::Handle<edm::View<reco::Candidate>> photons;
   iEvent.getByToken(photonToken_, photons);
 
   pat::PackedCandidate tau_vis;
   pat::PackedCandidate lepton_vis;
   pat::PackedCandidate photon;

   haveTriplet = havePair = havePhoton = false;
   for (auto i = taus->begin(); i != taus->end(); ++i) {
      if (i->pt()>=minpt_tau && std::abs(i->eta())<maxeta_tau) {
         for (auto j = leptons->begin(); j != leptons->end(); ++j) {
            if (j->pt()>=minpt_lepton && std::abs(j->eta())<maxeta_lepton) {
               if (i->charge()*j->charge()==q1q2) {
                  for (auto k = photons->begin(); k != photons->end(); ++k) {
                     if (k->pt()>=minpt_photon && std::abs(k->eta())<maxeta_photon) {
                        if (reco::deltaR(*i, *j)>=0.4 && reco::deltaR(*i, *k)>=0.4 && reco::deltaR(*j, *k)>=0.4) {
                           tau_vis.setP4(i->p4());
                           tau_vis.setCharge(i->charge());
                           tau_vis.setPdgId(i->pdgId());
                           lepton_vis.setP4(j->p4());
                           lepton_vis.setCharge(j->charge());
                           lepton_vis.setPdgId(j->pdgId());
                           photon.setP4(k->p4());
                           photon.setCharge(k->charge());
                           photon.setPdgId(k->pdgId());
                           haveTriplet = true;
                           havePair = true;
                           havePhoton = true;
                           break;
                        }
                     }
                  }
               }
            }
         }
      }
   }
   
   if (!haveTriplet) {
      for (auto i = taus->begin(); i != taus->end(); ++i) {
         if (i->pt()>=minpt_tau && std::abs(i->eta())<maxeta_tau) {
            for (auto j = leptons->begin(); j != leptons->end(); ++j) {
               if (j->pt()>=minpt_lepton && std::abs(j->eta())<maxeta_lepton) {
                  if (i->charge()*j->charge()==q1q2) {
                     if (reco::deltaR(*i, *j)>=0.4) {
                        tau_vis.setP4(i->p4());
                        tau_vis.setCharge(i->charge());
                        tau_vis.setPdgId(i->pdgId());
                        lepton_vis.setP4(j->p4());
                        lepton_vis.setCharge(j->charge());
                        lepton_vis.setPdgId(j->pdgId());
                        havePair = true;
                        break;
                     }
                  }
               }
            }
         }
      }
      for (auto i = photons->begin(); i != photons->end(); ++i) {
         if (i->pt()>=minpt_photon && std::abs(i->eta())<maxeta_photon) {  
            photon.setP4(i->p4());
            photon.setCharge(i->charge());
            photon.setPdgId(i->pdgId()); 
            havePhoton = true;
            break;
         }
      }
   }

   if (havePair) {
      tau_pt = tau_vis.pt();
      tau_eta = tau_vis.eta();
      tau_phi = tau_vis.phi();
      tau_mass = tau_vis.mass();
      lepton_pt = lepton_vis.pt();
      lepton_eta = lepton_vis.eta();
      lepton_phi = lepton_vis.phi();
      lepton_mass = lepton_vis.mass();
      ll_pt = (tau_vis.p4()+lepton_vis.p4()).pt();
      ll_mass = (tau_vis.p4()+lepton_vis.p4()).mass();
      ll_dr = reco::deltaR(tau_vis, lepton_vis);
   }
   if (havePhoton) {
      photon_pt = photon.pt();
      photon_eta = photon.eta();
      photon_phi = photon.phi();
   }

   if (havePair) {
      
      edm::Handle<std::vector<pat::MET>> met;
      iEvent.getByToken(metToken_, met);
      PolarLorentzVector MET;
      MET.SetPt(met->at(0).pt());
      MET.SetEta(met->at(0).eta());
      MET.SetPhi(met->at(0).phi());
      MET.SetM(met->at(0).mass());

      const double cos0M = cos(dphi(tau_vis.phi(), met->at(0).phi()));
      const double cos1M = cos(dphi(lepton_vis.phi(), met->at(0).phi()));
      const double cos01 = cos(dphi(tau_vis.phi(), lepton_vis.phi()));

      const double nu0mag = MET.pt() * (cos0M-cos1M*cos01) / (1.-cos01*cos01);
      const double nu1mag = (MET.pt()*cos1M) - (nu0mag*cos01);
 
      //It has been verified analytically that the expressions above are the same as the
      //expressions below by trig function manipulation
      //const double nu0mag = METpt*sin(METphi-lepton_vis.phi())/sin(tau_vis.phi()-lepton_vis.phi());
      //const double nu1mag = METpt*sin(METphi-tau_vis.phi())/sin(lepton_vis.phi()-tau_vis.phi());

      reco::LeafCandidate tau_inv = reco::LeafCandidate(0, PolarLorentzVector(0., 0., 0., 0.));
      PolarLorentzVector nu0_v;
      nu0_v.SetEta(tau_vis.eta());
      nu0_v.SetPhi(tau_vis.phi());
      nu0_v.SetPt(std::abs(nu0mag)); // abs hack to avoid nu0mag<0
      nu0_v.SetM(0.);
      tau_inv.setP4(nu0_v);
   
      pat::CompositeCandidate tau_col;
      tau_col.addDaughter(tau_vis);
      tau_col.addDaughter(tau_inv);
      const PolarLorentzVector tau_v = tau_vis.polarP4()+tau_inv.polarP4();
      tau_col.setP4(tau_v);
      tau_cmass = tau_col.mass();
 
      reco::LeafCandidate lepton_inv = reco::LeafCandidate(0, PolarLorentzVector(0., 0., 0., 0.));
      PolarLorentzVector nu1_v;
      nu1_v.SetEta(lepton_vis.eta());
      nu1_v.SetPhi(lepton_vis.phi());
      nu1_v.SetPt(std::abs(nu1mag)); // abs hack to avoid nu1mag<0
      nu1_v.SetM(0.);
      lepton_inv.setP4(nu1_v);
   
      pat::CompositeCandidate lepton_col;
      lepton_col.addDaughter(lepton_vis);
      lepton_col.addDaughter(lepton_inv);
      const PolarLorentzVector lepton_v = lepton_vis.polarP4()+lepton_inv.polarP4();
      lepton_col.setP4(lepton_v);
      lepton_cmass = lepton_col.mass();

      ll_cpt = (tau_col.p4()+lepton_col.p4()).pt();
      ll_cmass = (tau_col.p4()+lepton_col.p4()).mass();

      if (havePhoton) {
         gtau_cmass = (tau_col.p4()+photon.p4()).mass();
         glepton_cmass = (lepton_col.p4()+photon.p4()).mass(); 
      }
   }

   tree->Fill();
}

//define this as a plug-in
DEFINE_FWK_MODULE(ChannelAnalyzer);

