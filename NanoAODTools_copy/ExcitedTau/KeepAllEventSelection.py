import pdb
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#need this for the collinear approximation function
import numpy as np
import math

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

class EventSelection(Module):
    def __init__(self, lep_minpt, lep_maxeta, photon_pt_cuts, photon_dr_cuts, photon_maxeta):
        self.lep_minpt = lep_minpt
        self.lep_maxeta = lep_maxeta
        self.photon_pt_cuts = photon_pt_cuts
        self.photon_dr_cuts = photon_dr_cuts
        self.photon_maxeta = photon_maxeta
        self.deepTauWP_e = ["VVVLoose","VVLoose","VLoose","Loose","Medium","Tight","VTight","VVTight"]
        self.deepTauWP_jet = ["VVVLoose","VVLoose","VLoose","Loose","Medium","Tight","VTight","VVTight"]
        self.deepTauWP_mu = ["VLoose","Loose","Medium","Tight"]
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("channel","b")
        self.out.branch("back_to_back","O")
        self.out.branch("lep0_vis_pt","D")
        self.out.branch("lep0_vis_eta","D")
        self.out.branch("lep0_vis_phi","D")
        self.out.branch("lep0_vis_mass","D")
        self.out.branch("lep0_tauGenPartFlav","b")
        self.out.branch("lep1_vis_pt","D")
        self.out.branch("lep1_vis_eta","D")
        self.out.branch("lep1_vis_phi","D")
        self.out.branch("lep1_vis_mass","D")
        self.out.branch("lep1_tauGenPartFlav","b")
        self.out.branch("ll_vis_pt","D")
        self.out.branch("ll_vis_mass","D")
        self.out.branch("ll_vis_dr","D")
        self.out.branch("gamlep0_vis_mass","D")
        self.out.branch("gamlep0_vis_dr","D")
        self.out.branch("gamlep1_vis_mass","D")
        self.out.branch("gamlep1_vis_dr","D")
        self.out.branch("photon_pt","D")
        self.out.branch("photon_eta","D")
        self.out.branch("photon_phi","D")
        self.out.branch("lep0_col_pt","D")
        self.out.branch("lep0_col_eta","D")
        self.out.branch("lep0_col_phi","D")
        self.out.branch("lep0_col_mass","D")
        self.out.branch("lep1_col_pt","D")
        self.out.branch("lep1_col_eta","D")
        self.out.branch("lep1_col_phi","D")
        self.out.branch("lep1_col_mass","D")
        self.out.branch("ll_col_mass","D")
        self.out.branch("ll_col_pt","D")
        self.out.branch("ll_col_dr","D")
        self.out.branch("gamlep0_col_mass","D")
        self.out.branch("gamlep0_col_dr","D")
        self.out.branch("gamlep1_col_mass","D")
        self.out.branch("gamlep1_col_dr","D")
        self.out.branch("photon_pt_cutFlag","b")
        self.out.branch("too_many_leptons_cutFlag","O")
        self.out.branch("passTrigger","O")
        self.out.branch("photon_dr_cutFlag","b")
        self.out.branch("phiCheck_cutFlag","O")
        self.out.branch("bjet_present","b")
        self.out.branch("q0q1_sign","B")
        self.out.branch("deepTauNominalWP_e","b")
        self.out.branch("deepTauNominalWP_mu","b")
        self.out.branch("deepTauNominalWP_jet","b")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        photons = Collection(event,"Photon")
        goodPhotons = [photons[i] for i in xrange(len(photons)) if (photons[i].pt > self.photon_pt_cuts[0] and abs(photons[i].eta) < self.photon_maxeta and photons[i].mvaID_WP90 and photons[i].electronVeto and (photons[i].isScEtaEB or photons[i].isScEtaEE))]
#        print("Number of photons:"+str(len(goodPhotons)))
        goodPhotons.sort(key=lambda x: x.pt,reverse=True)
        noPhoton = False
        if len(goodPhotons) < 1:
          noPhoton = True 
          self.out.fillBranch("photon_pt_cutFlag",0)
        else:
          photon = goodPhotons[0]
          photon_p4 = photon.p4()
          photon_pt_ind = 1
          for ind,pt in enumerate(self.photon_pt_cuts):
            if photon.pt < pt:
              break  
            photon_pt_ind = ind+1
          self.out.fillBranch("photon_pt_cutFlag",2**photon_pt_ind-1)

        #Anything classified as a tau should end up in this collection. That means all decay modes (el,mu,had)
        taus = Collection(event,"Tau")
        if len(taus) < 2:
          return False # the event did not classify enough things as taus originally so skip the event
        
        

        goodLeptons = []
        lepType = []

        #Good Electron Definition
        electronColl = Collection(event,"Electron")
#        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP80 or electronColl[i].mvaFall17V1noIso_WP80]
        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP80]
        goodElectrons = [goodElectrons[i] for i in xrange(len(goodElectrons)) if goodElectrons[i].pt > self.lep_minpt[0] and abs(goodElectrons[i].eta) < self.lep_maxeta[0]]
        goodLeptons.extend(sorted(goodElectrons,key=lambda x: x.pt, reverse=True))
        lepType.extend([1]*len(goodElectrons))

        #Good Muon Definition
        muonColl = Collection(event,"Muon")
        goodMuons = [muonColl[i] for i in xrange(len(muonColl)) if (muonColl[i].tightId and muonColl[i].pfIsoId >= 4)]#VLoose=1 to VVTight=6
        goodMuons = [goodMuons[i] for i in xrange(len(goodMuons)) if goodMuons[i].pt > self.lep_minpt[1] and abs(goodMuons[i].eta) < self.lep_maxeta[1]]
        goodLeptons.extend(sorted(goodMuons,key=lambda x: x.pt, reverse=True))
        lepType.extend([2]*len(goodMuons))

        #Good Hadronic Tau Definition
        hadColl = Collection(event,"Tau")
        #tight ID for all
        deepTauNominalWP_e_word = "Tight"
        deepTauNominalWP_mu_word = "Tight"
        deepTauNominalWP_jet_word = "Tight"
        deepTauNominalWP_e = 1 << self.deepTauWP_e.index(deepTauNominalWP_e_word)
        deepTauNominalWP_mu = 1 << self.deepTauWP_mu.index(deepTauNominalWP_mu_word)
        deepTauNominalWP_jet = 1 << self.deepTauWP_jet.index(deepTauNominalWP_jet_word)
        self.out.fillBranch("deepTauNominalWP_e",deepTauNominalWP_e)
        self.out.fillBranch("deepTauNominalWP_mu",deepTauNominalWP_mu)
        self.out.fillBranch("deepTauNominalWP_jet",deepTauNominalWP_jet)
        
        goodHads = [hadColl[i] for i in xrange(len(hadColl)) if (hadColl[i].idDeepTau2017v2p1VSe & deepTauNominalWP_e and hadColl[i].idDeepTau2017v2p1VSmu & deepTauNominalWP_mu and hadColl[i].idDeepTau2017v2p1VSjet & deepTauNominalWP_jet)]
        goodHads = [goodHads[i] for i in xrange(len(goodHads)) if goodHads[i].pt > self.lep_minpt[2] and abs(goodHads[i].eta) < self.lep_maxeta[2]]
        goodHads = [goodHads[i] for i in xrange(len(goodHads)) if goodHads[i].decayMode != 5 and goodHads[i].decayMode != 6]
        goodLeptons.extend(sorted(goodHads,key=lambda x: x.pt, reverse=True))
        lepType.extend([4]*len(goodHads))
              
#        pdb.set_trace()
        #Here we find the two leptons that we are interested in and make sure they match the desired q0q1
        lepton_p4 = [goodLeptons[i].p4() for i in xrange(len(goodLeptons))]
        pair_energy_check = [(lepton_p4[i]+lepton_p4[j]).E() if  (deltaR(goodLeptons[i],goodLeptons[j])>0.4 and i < j) else 0 for i in xrange(len(goodLeptons)) for j in xrange(len(goodLeptons))]
        #if we have more than one pair of leptons, this does not meet our event profile
        if sum([1 for i in xrange(len(pair_energy_check)) if pair_energy_check[i] > 0]) > 1:
          self.out.fillBranch("too_many_leptons_cutFlag",True)
        else:
          self.out.fillBranch("too_many_leptons_cutFlag",False)
        channel_type = [lepType[i] | lepType[j] if pair_energy_check[i*len(goodLeptons)+j] > 0 and i < j else 0 for i in xrange(len(goodLeptons)) for j in xrange(len(goodLeptons))]
        max_energy = max(pair_energy_check or [0])
        noPair = False
        if max_energy == 0:
          noPair = True #not enough non-overlapping leptons
        if not noPair:
          ind = pair_energy_check.index(max_energy)
          channel = channel_type[ind]
          if self.passTrigger(event,channel):
            self.out.fillBranch("passTrigger",True)
          else:
            self.out.fillBranch("passTrigger",False)
          ind0 = int(ind/len(goodLeptons))
          ind1 = ind - ind0*len(goodLeptons)
          lep0 = goodLeptons[ind0]
          lep0_p4 = lep0.p4()
          lep1 = goodLeptons[ind1]
          lep1_p4 = lep1.p4()
          self.out.fillBranch("q0q1_sign",lep0.charge*lep1.charge)
          
          if not noPhoton:
            #we want to eliminate FSR confusion which usually is very close to the radiating lepton
            deltaR_ind = 0
            for ind,dr in enumerate(self.photon_dr_cuts):
              if deltaR(lep0,photon) < dr or deltaR(lep1,photon) < dr:
                break
              deltaR_ind = ind + 1
            if deltaR_ind == 0:
              self.out.fillBranch("photon_dr_cutFlag",0)
            else:
              self.out.fillBranch("photon_dr_cutFlag",2**deltaR_ind-1)
          else:
            self.out.fillBranch("photon_dr_cutFlag",0)
  
          #MET should be between the two leptons for good collinear approximation reconstruction
          self.out.fillBranch("phiCheck_cutFlag",self.phiChecker(lep0.phi,lep1.phi,event.MET_phi)) 
  
          #b-tag rejection
          bjet_present = 0
          jetColl = Collection(event,"Jet")
          for jet in jetColl:
            if jet.DeltaR(lep0) < 0.4 or jet.DeltaR(lep1) < 0.4 :
              continue
            if (not noPhoton) and jet.DeltaR(photon) < 0.4:
              continue
            #b-tag recommendations at https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
            if jet.btagDeepB > 0.7264: #tight
              bjet_present = 7
              break
            else:
              if jet.btagDeepB > 0.2770 and bjet_present != 7:
                bjet_present = 3
              else:
                if jet.btagDeepB > 0.0494 and bjet_present < 1:
                  bjet_present = 1
          self.out.fillBranch("bjet_present",bjet_present)
  
  
  
  
          #returns the p4 of the two leptons after collinear approximation
          lep0_col_p4,lep1_col_p4, back_to_back = self.collinear_approx(lep0_p4,lep1_p4,event.MET_pt,event.MET_phi) 
          self.out.fillBranch("channel",channel)
          self.out.fillBranch("back_to_back",back_to_back)
          self.out.fillBranch("lep0_vis_pt",lep0.pt)
          self.out.fillBranch("lep0_vis_eta",lep0.eta)
          self.out.fillBranch("lep0_vis_phi",lep0.phi)
          self.out.fillBranch("lep0_vis_mass",lep0.mass)
          self.out.fillBranch("lep1_vis_pt",lep1.pt)
          self.out.fillBranch("lep1_vis_eta",lep1.eta)
          self.out.fillBranch("lep1_vis_phi",lep1.phi)
          self.out.fillBranch("lep1_vis_mass",lep1.mass)
          self.out.fillBranch("ll_vis_pt",(lep0_p4+lep1_p4).Pt())
          self.out.fillBranch("ll_vis_mass",(lep0_p4+lep1_p4).M())
          self.out.fillBranch("ll_vis_dr",deltaR(lep0,lep1))
          self.out.fillBranch("lep0_col_pt",lep0_col_p4.Pt())
          self.out.fillBranch("lep0_col_eta",lep0_col_p4.Eta())
          self.out.fillBranch("lep0_col_phi",lep0_col_p4.Phi())
          self.out.fillBranch("lep0_col_mass",lep0_col_p4.M())
          self.out.fillBranch("lep1_col_pt",lep1_col_p4.Pt())
          self.out.fillBranch("lep1_col_eta",lep1_col_p4.Eta())
          self.out.fillBranch("lep1_col_phi",lep1_col_p4.Phi())
          self.out.fillBranch("lep1_col_mass",lep1_col_p4.M())
          self.out.fillBranch("ll_col_mass",(lep0_col_p4+lep1_col_p4).M())
          self.out.fillBranch("ll_col_pt",(lep0_col_p4+lep1_col_p4).Pt())
          self.out.fillBranch("ll_col_dr",deltaR(lep0_col_p4.Eta(),lep0_col_p4.Phi(),lep1_col_p4.Eta(),lep1_col_p4.Phi()))
        else:
          self.out.fillBranch("channel",0)
          self.out.fillBranch("back_to_back",0)
          self.out.fillBranch("lep0_vis_pt",0)
          self.out.fillBranch("lep0_vis_eta",0)
          self.out.fillBranch("lep0_vis_phi",0)
          self.out.fillBranch("lep0_vis_mass",0)
          self.out.fillBranch("lep1_vis_pt",0)
          self.out.fillBranch("lep1_vis_eta",0)
          self.out.fillBranch("lep1_vis_phi",0)
          self.out.fillBranch("lep1_vis_mass",0)
          self.out.fillBranch("ll_vis_pt",0)
          self.out.fillBranch("ll_vis_mass",0)
          self.out.fillBranch("ll_vis_dr",0)
          self.out.fillBranch("lep0_col_pt",0)
          self.out.fillBranch("lep0_col_eta",0)
          self.out.fillBranch("lep0_col_phi",0)
          self.out.fillBranch("lep0_col_mass",0)
          self.out.fillBranch("lep1_col_pt",0)
          self.out.fillBranch("lep1_col_eta",0)
          self.out.fillBranch("lep1_col_phi",0)
          self.out.fillBranch("lep1_col_mass",0)
          self.out.fillBranch("ll_col_mass",0)
          self.out.fillBranch("ll_col_pt",0)
          self.out.fillBranch("ll_col_dr",0)
          self.out.fillBranch("q0q1_sign",0)
          self.out.fillBranch("photon_dr_cutFlag",0)
          self.out.fillBranch("phiCheck_cutFlag",0) 
          self.out.fillBranch("bjet_present",0)
          
        if noPhoton:
          self.out.fillBranch("photon_pt",0)
          self.out.fillBranch("photon_eta",0)
          self.out.fillBranch("photon_phi",0)
          self.out.fillBranch("gamlep0_vis_mass",0)
          self.out.fillBranch("gamlep0_vis_dr",0)
          self.out.fillBranch("gamlep1_vis_mass",0)
          self.out.fillBranch("gamlep1_vis_dr",0)
          self.out.fillBranch("gamlep0_col_mass",0)
          self.out.fillBranch("gamlep0_col_dr",0)
          self.out.fillBranch("gamlep1_col_mass",0)
          self.out.fillBranch("gamlep1_col_dr",0)
        else:
          self.out.fillBranch("photon_pt",photon.pt)
          self.out.fillBranch("photon_eta",photon.eta)
          self.out.fillBranch("photon_phi",photon.phi)
          if noPair:
            self.out.fillBranch("gamlep0_vis_mass",0)
            self.out.fillBranch("gamlep0_vis_dr",0)
            self.out.fillBranch("gamlep1_vis_mass",0)
            self.out.fillBranch("gamlep1_vis_dr",0)
            self.out.fillBranch("gamlep0_col_mass",0)
            self.out.fillBranch("gamlep0_col_dr",0)
            self.out.fillBranch("gamlep1_col_mass",0)
            self.out.fillBranch("gamlep1_col_dr",0)
          else:
            self.out.fillBranch("gamlep0_vis_mass",(photon_p4+lep0_p4).M())
            self.out.fillBranch("gamlep0_vis_dr",deltaR(lep0,photon))
            self.out.fillBranch("gamlep1_vis_mass",(photon_p4+lep1_p4).M())
            self.out.fillBranch("gamlep1_vis_dr",deltaR(lep1,photon))
            self.out.fillBranch("gamlep0_col_mass",(photon_p4+lep0_col_p4).M())
            self.out.fillBranch("gamlep0_col_dr",deltaR(photon.eta,photon.phi,lep0_col_p4.Eta(),lep0_col_p4.Phi()))
            self.out.fillBranch("gamlep1_col_mass",(photon_p4+lep1_col_p4).M())
            self.out.fillBranch("gamlep1_col_dr",deltaR(photon.eta,photon.phi,lep1_col_p4.Eta(),lep1_col_p4.Phi()))
        return True

    def collinear_approx(self,tau0,tau1,MET_pt,MET_phi):
        MET = ROOT.TLorentzVector()
        MET.SetPtEtaPhiM(MET_pt,0,MET_phi,0)
#       MET.SetPtEtaPhiM(event.GenMET_pt,0,event.GenMET_phi,0)
        tau0xydir = ROOT.TVector3(tau0.X(),tau0.Y(),0)
#        tau0xydir *= 1.1
        tau1xydir = ROOT.TVector3(tau1.X(),tau1.Y(),0)
#        tau1xydir *= 1.1
        #make array of tau directions to be used for MET decomposition; array elements are ordered first across rows
        METdecompArray = np.array([tau0xydir.X(),tau1xydir.X(),tau0xydir.Y(),tau1xydir.Y()]).reshape(2,2)
        try:
          METdecomp = np.dot(np.linalg.inv(METdecompArray),np.array([MET.X(),MET.Y()])[:,None])
          back_to_back = False
          #collinear approx
          MET0xy = float(METdecomp[0])*tau0xydir
          #collinear approx
          MET1xy = float(METdecomp[1])*tau1xydir
        except np.linalg.LinAlgError:
          #if the taus are back to back, choose the one that the MET is closest to and give it to that one
          back_to_back = True
          if MET.Angle(tau0xydir) < MET.Angle(tau1xydir):
            MET0xy = MET.Pt()*tau0xydir
            MET1xy = 0*tau1xydir
          else:
            MET0xy = 0*tau0xydir
            MET1xy = MET.Pt()*tau1xydir
        tau0_col = ROOT.TLorentzVector()
        tau1_col = ROOT.TLorentzVector()
        tau0_col.SetPtEtaPhiM(tau0.Pt() + MET0xy.Pt(),tau0.Eta(),tau0.Phi(),tau0.M())
        tau1_col.SetPtEtaPhiM(tau1.Pt() + MET1xy.Pt(),tau1.Eta(),tau1.Phi(),tau1.M())
        return tau0_col, tau1_col, back_to_back

    def phiChecker(self,phi1,phi2,phi_test):
        #make all angles in the range -pi to pi
        correct_range = lambda x: math.atan2(math.sin(x),math.cos(x))
        phi1 = correct_range(phi1)
        phi2 = correct_range(phi2)
        phi_test = correct_range(phi_test)
        if abs(abs(phi1-phi2)-math.pi) < 5*np.finfo(float).eps: return "Bounds separated by pi"
        if not abs(phi1-phi2) < math.pi:
          if phi1 < phi2: phi1 += 2*math.pi
          else: phi2 += 2*math.pi
        phis = sorted([phi1,phi2,phi_test])
        if phis[1] == phi_test: return True
        phis = sorted([phi1,phi2,phi_test+2*math.pi])
        if phis[1] == phi_test+2*math.pi: return True
        return False

    def passTrigger(self,event,channel):
        if channel == 6: 
          if not(event.HLT_IsoMu24 or event.HLT_IsoMu27): return False
          else return True
        if hasattr(event,"HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg"): return self.trigger2017(event,channel)
        if hasattr(event,"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg"): return self.triggerV6(event,channel) 
        if hasattr(event,"HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"): return self.triggerDataV7(event,channel)
        return self.triggerDefault(event,channel)

    def triggerV6(self,event,channel):
        if channel == 4:
          return event.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg
        if channel == 6:
          return event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1

    def triggerDataV7(self,event,channel):
        if channel == 4:
          return event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg
        if channel == 6:
          return event.HLT_IsoMu19_eta2p1_LooseCombinedIsoPFTau20

    def trigger2017(self,event,channel):
        if channel == 4:
          return event.HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg
        if channel == 6:
          return event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1

    def triggerDefault(self,event,channel):
        if channel == 4:
          return event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg
        if channel == 6:
          return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

event_selection_all = lambda : EventSelection([32,27,20],[2.5,2.4,2.3],[20,50,80,100,120,150,175],[0.1,0.4,0.7,1.0],2.5)

