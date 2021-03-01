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
    def __init__(self, lep_minpt, lep_maxeta, photon_minpt, photon_maxeta, q0q1):
        self.lep_minpt = lep_minpt
        self.lep_maxeta = lep_maxeta
        self.photon_minpt = photon_minpt
        self.photon_maxeta = photon_maxeta
        self.q0q1 = q0q1 #sign between lepton charge pair
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
        self.out.branch("lep1_vis_pt","D")
        self.out.branch("lep1_vis_eta","D")
        self.out.branch("lep1_vis_phi","D")
        self.out.branch("lep1_vis_mass","D")
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
        self.out.branch("havePair","O")
        self.out.branch("havePhoton","O")
        self.out.branch("haveTriplet","O")
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
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        photons = Collection(event,"Photon")
        goodPhotons = [photons[i] for i in xrange(len(photons)) if (photons[i].pt > self.photon_minpt and photons[i].eta < self.photon_maxeta and photons[i].mvaID_WP90 and photons[i].electronVeto and (photons[i].isScEtaEB or photons[i].isScEtaEE))]
#        print("Number of photons:"+str(len(goodPhotons)))
        goodPhotons.sort(key=lambda x: x.pt,reverse=True)
        if len(goodPhotons) < 1:
          return False #no photon is a no-go
        else:
          self.out.fillBranch("havePhoton",True)

        #Anything classified as a tau should end up in this collection. That means all decay modes (el,mu,had)
        taus = Collection(event,"Tau")
        if len(taus) < 2:
          return False # the event did not classify enough things as taus originally so skip the event
        
        #b-tag rejection
        jetColl = Collection(event,"Jet")
        #b-tag recommendations at https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
        for jet in jetColl:
          if jet.btagDeepB > 0.7264: #tight
            return False #b-tags are only from background
        

        goodLeptons = []
        lepType = []

        #Good Electron Definition
        electronColl = Collection(event,"Electron")
#        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP80 or electronColl[i].mvaFall17V1noIso_WP80]
        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP80]
        goodElectrons = [goodElectrons[i] for i in xrange(len(goodElectrons)) if goodElectrons[i].pt > self.lep_minpt[0] and goodElectrons[i].eta < self.lep_maxeta[0]]
        goodLeptons.extend(sorted(goodElectrons,key=lambda x: x.pt, reverse=True))
        lepType.extend([1]*len(goodElectrons))

        #Good Muon Definition
        muonColl = Collection(event,"Muon")
        goodMuons = [muonColl[i] for i in xrange(len(muonColl)) if (muonColl[i].tightId and muonColl[i].pfIsoId >= 4)]#VLoose to VVTight
        goodMuons = [goodMuons[i] for i in xrange(len(goodMuons)) if goodMuons[i].pt > self.lep_minpt[1] and goodMuons[i].eta < self.lep_maxeta[1]]
        goodLeptons.extend(sorted(goodMuons,key=lambda x: x.pt, reverse=True))
        lepType.extend([2]*len(goodMuons))

        #Good Hadronic Tau Definition
        hadColl = Collection(event,"Tau")
        #tight ID for all
        goodHads = [hadColl[i] for i in xrange(len(hadColl)) if (hadColl[i].idDeepTau2017v2p1VSe & (1 << 5) and hadColl[i].idDeepTau2017v2p1VSmu & (1 << 3) and hadColl[i].idDeepTau2017v2p1VSjet & (1 << 5))]# electron bit mask VVVLoose to VVTight; muon bit mask VLoose to Tight; jet bit mask VVVLoose to VVTight
        goodHads = [goodHads[i] for i in xrange(len(goodHads)) if goodHads[i].pt > self.lep_minpt[2] and goodHads[i].eta < self.lep_maxeta[2]]
        goodHads = [goodHads[i] for i in xrange(len(goodHads)) if goodHads[i].decayMode != 5 and goodHads[i].decayMode != 6]
        goodLeptons.extend(sorted(goodHads,key=lambda x: x.pt, reverse=True))
        lepType.extend([4]*len(goodHads))
              
#        pdb.set_trace()
        #Here we find the two leptons that we are interested in and make sure they match the desired q0q1
        lepton_p4 = [goodLeptons[i].p4() for i in xrange(len(goodLeptons))]
        pair_energy_check = [(lepton_p4[i]+lepton_p4[j]).E() if (goodLeptons[i].charge*goodLeptons[j].charge == self.q0q1 and deltaR(goodLeptons[i],goodLeptons[j])>0.4 and i < j) else 0 for i in xrange(len(goodLeptons)) for j in xrange(len(goodLeptons))]
        if sum([1 for i in xrange(len(pair_energy_check)) if pair_energy_check[i] > 0]) > 1:
          return False #if we have more than one pair of leptons, this does not meet our event profile
        channel_type = [lepType[i] | lepType[j] if pair_energy_check[i*len(goodLeptons)+j] > 0 and i < j else 0 for i in xrange(len(goodLeptons)) for j in xrange(len(goodLeptons))]
        max_energy = max(pair_energy_check or [0])
        if max_energy == 0:
          self.out.fillBranch("havePair",False)
          havePair = False
          return False
        ind = pair_energy_check.index(max_energy)
        channel = channel_type[ind]
        self.passTrigger(event,channel)
        ind0 = int(ind/len(goodLeptons))
        ind1 = ind - ind0*len(goodLeptons)
        lep0 = goodLeptons[ind0]
        lep0_p4 = lep0.p4()
        lep1 = goodLeptons[ind1]
        lep1_p4 = lep1.p4()
        photon = goodPhotons[0]
        photon_p4 = photon.p4()
        self.out.fillBranch("havePair",True)
        if deltaR(lep0,photon) < 0.7 or deltaR(lep1,photon) < 0.7:
          return False #we want to eliminate FSR confusion which usually is very close to the radiating lepton
        if not self.phiChecker(lep0.phi,lep1.phi,event.MET_phi): 
          return False #MET should be between the two leptons for good collinear approximation reconstruction



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
        self.out.fillBranch("photon_pt",photon.pt)
        self.out.fillBranch("photon_eta",photon.eta)
        self.out.fillBranch("photon_phi",photon.phi)
        self.out.fillBranch("gamlep0_vis_mass",(photon_p4+lep0_p4).M())
        self.out.fillBranch("gamlep0_vis_dr",deltaR(lep0,photon))
        self.out.fillBranch("gamlep1_vis_mass",(photon_p4+lep1_p4).M())
        self.out.fillBranch("gamlep1_vis_dr",deltaR(lep1,photon))
        self.out.fillBranch("gamlep0_col_mass",(photon_p4+lep0_col_p4).M())
        self.out.fillBranch("gamlep0_col_dr",deltaR(photon.eta,photon.phi,lep0_col_p4.Eta(),lep0_col_p4.Phi()))
        self.out.fillBranch("gamlep1_col_mass",(photon_p4+lep1_col_p4).M())
        self.out.fillBranch("gamlep1_col_dr",deltaR(photon.eta,photon.phi,lep1_col_p4.Eta(),lep1_col_p4.Phi()))
        self.out.fillBranch("haveTriplet",True)
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


        

class SignalCollinearCheck(Module):
    def __init__(self):#, channel_code, lep0_minpt, lep0_maxeta, lep1_minpt, lep1_maxeta, photon_minpt, photon_maxeta, q0q1):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("missingPtBetween_Reco","O")
        self.out.branch("missingPtBetween_Gen","O")
        self.out.branch("missingPtBetween_Nu","O")
        self.out.branch("METvsGenMET","D")
        self.out.branch("METvsNuSum","D")
        self.out.branch("genMETvsNuSum","D")
        self.out.branch("genVisPVsRecoP0","D")
        self.out.branch("genColPVsRecoP0","D")
        self.out.branch("genVisPVsRecoP1","D")
        self.out.branch("genColPVsRecoP1","D")
        self.out.branch("deltaR0_truth","D")
        self.out.branch("deltaR1_truth","D")
        self.out.branch("deltaR0_nu","D")
        self.out.branch("deltaR1_nu","D")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #this module can only be run after EventSelection has been run
        if not hasattr(event,"lep0_vis_phi"):
          raise Exception("SignalCollinearCheck can only be run after EventSelection")
        genMET = ROOT.TLorentzVector()
        genMET.SetPtEtaPhiM(event.GenMET_pt,0,event.GenMET_phi,0)
        MET = ROOT.TLorentzVector()
        MET.SetPtEtaPhiM(event.MET_pt,0,event.MET_phi,0)
        self.out.fillBranch("METvsGenMET",deltaR(MET.Eta(),MET.Phi(),genMET.Eta(),genMET.Phi()))
        self.out.fillBranch("missingPtBetween_Reco",self.phiChecker(event.lep0_vis_phi,event.lep1_vis_phi,event.MET_phi))
        genParts = Collection(event,"GenPart")
        nuList = [genParts[i] for i in range(len(genParts)) if abs(genParts[i].pdgId) == 16] 
        tauList = [genParts[nuList[i].genPartIdxMother] for i in range(len(nuList))]
        if len(nuList) > 1:
          deltaR0_nu = deltaR(nuList[0],tauList[0])
          deltaR1_nu = deltaR(nuList[1],tauList[1])
          missingNu = nuList[0].p4()+nuList[1].p4()
          missingNuPerp = ROOT.TLorentzVector()
          missingNuPerp.SetPtEtaPhiM(missingNu.Pt(),0,missingNu.Phi(),missingNu.M())
          momentumMag = lambda pt,eta: pt/math.sin(math.atan(2*math.exp(-eta)))
          if deltaR(tauList[0].eta,tauList[0].phi,event.lep0_vis_eta,event.lep0_vis_phi) < deltaR(tauList[0].eta,tauList[0].phi,event.lep1_vis_eta,event.lep1_vis_phi):
            genVisPVsRecoP0 = momentumMag(tauList[0].pt,tauList[0].eta) - momentumMag(event.lep0_vis_pt,event.lep0_vis_eta)
            genColPVsRecoP0 = momentumMag(tauList[0].pt,tauList[0].eta) - momentumMag(event.lep0_col_pt,event.lep0_col_eta)
            genVisPVsRecoP1 = momentumMag(tauList[1].pt,tauList[1].eta) - momentumMag(event.lep1_vis_pt,event.lep1_vis_eta)
            genColPVsRecoP1 = momentumMag(tauList[1].pt,tauList[1].eta) - momentumMag(event.lep1_col_pt,event.lep1_col_eta)
            deltaR0_truth = deltaR(tauList[0].eta,tauList[0].phi,event.lep0_vis_eta,event.lep0_vis_phi)
            deltaR1_truth = deltaR(tauList[1].eta,tauList[1].phi,event.lep1_vis_eta,event.lep1_vis_phi)
          else:
            genVisPVsRecoP0 = momentumMag(tauList[0].pt,tauList[0].eta) - momentumMag(event.lep1_vis_pt,event.lep1_vis_eta)
            genColPVsRecoP0 = momentumMag(tauList[0].pt,tauList[0].eta) - momentumMag(event.lep1_col_pt,event.lep1_col_eta)
            genVisPVsRecoP1 = momentumMag(tauList[1].pt,tauList[1].eta) - momentumMag(event.lep0_vis_pt,event.lep0_vis_eta)
            genColPVsRecoP1 = momentumMag(tauList[1].pt,tauList[1].eta) - momentumMag(event.lep0_col_pt,event.lep0_col_eta)
            deltaR0_truth = deltaR(tauList[0].eta,tauList[0].phi,event.lep1_vis_eta,event.lep1_vis_phi)
            deltaR1_truth = deltaR(tauList[1].eta,tauList[1].phi,event.lep0_vis_eta,event.lep0_vis_phi)

          self.out.fillBranch("genMETvsNuSum",deltaR(genMET.Eta(),genMET.Phi(),missingNuPerp.Eta(),missingNuPerp.Phi()))
          self.out.fillBranch("METvsNuSum",deltaR(MET.Eta(),MET.Phi(),missingNuPerp.Eta(),missingNuPerp.Phi()))
          self.out.fillBranch("missingPtBetween_Nu",self.phiChecker(tauList[0].phi,tauList[1].phi,missingNuPerp.Phi()))
          self.out.fillBranch("missingPtBetween_Gen",self.phiChecker(tauList[0].phi,tauList[1].phi,genMET.Phi()))
          self.out.fillBranch("genVisPVsRecoP0",genVisPVsRecoP0)
          self.out.fillBranch("genColPVsRecoP0",genColPVsRecoP0)
          self.out.fillBranch("genVisPVsRecoP1",genVisPVsRecoP1)
          self.out.fillBranch("genColPVsRecoP1",genColPVsRecoP1)
          self.out.fillBranch("deltaR0_truth",deltaR0_truth)
          self.out.fillBranch("deltaR1_truth",deltaR1_truth)
          self.out.fillBranch("deltaR0_nu",deltaR0_nu)
          self.out.fillBranch("deltaR1_nu",deltaR1_nu)
        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

event_selection_min = lambda : EventSelection([32,27,20],[2.5,2.4,2.3],100,2.5,-1)
signalCollinearCheck = lambda : SignalCollinearCheck()
