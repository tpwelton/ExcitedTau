import pdb
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#need this for the collinear approximation function
import numpy as np
import math

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR


class ChannelAnalyzer(Module):
    def __init__(self, channel_code, lep0_minpt, lep0_maxeta, lep1_minpt, lep1_maxeta, photon_minpt, photon_maxeta, q0q1):
        self.channel_code = channel_code
        self.lep0_minpt = lep0_minpt
        self.lep0_maxeta = lep0_maxeta
        self.lep1_minpt = lep1_minpt
        self.lep1_maxeta = lep1_maxeta
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
        goodPhotons = [photons[i] for i in xrange(len(photons)) if (photons[i].pt > self.photon_minpt and photons[i].eta < self.photon_maxeta and photons[i].mvaID_WP90 and photons[i].electronVeto)]
#        print("Number of photons:"+str(len(goodPhotons)))
        goodPhotons.sort(key=lambda x: x.pt,reverse=True)
        if len(goodPhotons) < 1:
          return False #no photon is a no-go
          self.out.fillBranch("havePhoton",False)
          self.out.fillBranch("haveTriplet",False)
        else:
          self.out.fillBranch("havePhoton",True)

        #Anything classified as a tau should end up in this collection. That means all decay modes (el,mu,had)
        taus = Collection(event,"Tau")
#        if len(taus) < 2:
#          return False # the event did not classify enough things as taus originally so skip the event

        self.lep_coll0 = None
        self.lep_coll1 = None
        lep_dict = {}
        #Good Electron Definition
        electronColl = Collection(event,"Electron")
#        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP80]
        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP80 or electronColl[i].mvaFall17V1noIso_WP80]
#        goodElectrons = [electronColl[i] for i in xrange(len(electronColl)) if electronColl[i].mvaFall17V1Iso_WP90 or electronColl[i].mvaFall17V1noIso_WP90]
#        goodElectrons = electronColl #max acceptance check
        electronTauCompatible = []
        for elec in goodElectrons:
          tauCompatible = [elec for i in xrange(len(taus)) if deltaR(elec,taus[i]) < 0.1]
          if len(tauCompatible) > 0:
            electronTauCompatible.append(elec)
        electronTauCompatible = goodElectrons
        lep_dict["electrons"] = sorted(electronTauCompatible,key=lambda x: x.pt, reverse=True)

        #Good Muon Definition
        muonColl = Collection(event,"Muon")
        goodMuons = [muonColl[i] for i in xrange(len(muonColl)) if (muonColl[i].tightId and muonColl[i].pfIsoId >= 3)]#VLoose to VVTight
#        goodMuons = [muonColl[i] for i in xrange(len(muonColl)) if (muonColl[i].looseId)]
#        goodMuons = muonColl #max acceptance check
        muonTauCompatible = []
        for muon in goodMuons:
          tauCompatible = [muon for i in xrange(len(taus)) if deltaR(muon,taus[i]) < 0.1]
          if len(tauCompatible) > 0:
            muonTauCompatible.append(muon)
        muonTauCompatible = goodMuons
        lep_dict["muons"] = sorted(muonTauCompatible,key=lambda x: x.pt, reverse=True)

        #Good Hadronic Tau Definition
        hadColl = Collection(event,"Tau")
#        goodHads = [hadColl[i] for i in xrange(len(hadColl)) if (hadColl[i].idAntiEle & (1 << 3) and hadColl[i].idAntiMu & (1 << 2))]# electron bit mask VLoose to VTight; muon bit mask Loose or Tight
#        goodHads = [hadColl[i] for i in xrange(len(hadColl)) if (hadColl[i].idDeepTau2017v2p1VSe & (1 << 3) and hadColl[i].idDeepTau2017v2p1VSmu & (1 << 1) and hadColl[i].idDeepTau2017v2p1VSjet & (1 << 3))]# electron bit mask VVVLoose to VVTight; muon bit mask VLoose to Tight; jet bit mask VVVLoose to VVTight
        goodHads = [hadColl[i] for i in xrange(len(hadColl)) if (hadColl[i].idDeepTau2017v2p1VSe & (1 << 5) and hadColl[i].idDeepTau2017v2p1VSmu & (1 << 3) and hadColl[i].idDeepTau2017v2p1VSjet & (1 << 5))]# electron bit mask VVVLoose to VVTight; muon bit mask VLoose to Tight; jet bit mask VVVLoose to VVTight
#        goodHads = [hadColl[i] for i in xrange(len(hadColl)) if (hadColl[i].idDeepTau2017v2p1VSe & (1 << 0) and hadColl[i].idDeepTau2017v2p1VSmu & (1 << 0) and hadColl[i].idDeepTau2017v2p1VSjet & (1 << 0))]# DeepTau electron bit mask VVVLoose to VVTight; DeepTau muon bit mask VLoose to Tight; jet bit mask VVVLoose to VVTight
#        goodHads = hadColl #max acceptance check
        tauHadOnly = goodHads
#        tauHadOnly = []
#        pdb.set_trace()
#        for had in goodHads:
#          elecCompatible = [had for i in xrange(len(lep_dict.get("electrons"))) if deltaR(had,lep_dict.get("electrons")[i]) < 0.1]
#          muonCompatible = [had for i in xrange(len(lep_dict.get("muons"))) if deltaR(had,lep_dict.get("muons")[i]) < 0.1]
#          if len(elecCompatible) == 0 and len(muonCompatible) == 0:
#            tauHadOnly.append(had)
        lep_dict["hads"] = sorted(tauHadOnly,key=lambda x: x.pt, reverse=True)
        if not (self.channel_code & (1 << 0)): del lep_dict["electrons"] 
        if not (self.channel_code & (1 << 1)): del lep_dict["muons"]
        if not (self.channel_code & (1 << 2)): del lep_dict["hads"]
        if "electrons" in lep_dict: 
          electrons = lep_dict.get("electrons")
          self.lep_coll0 = [electrons[i] for i in xrange(len(electrons)) if electrons[i].pt > self.lep0_minpt and electrons[i].eta < self.lep0_maxeta]
          if len(self.lep_coll0) < 1:
            return False #No electron was good enough and one was expected so the event selection fails
          #if there is only one type of lepton in lep_dict, the other collection is also electrons
          if len(lep_dict) < 2:
            self.lep_coll1 = [electrons[i] for i in xrange(len(electrons)) if electrons[i].pt > self.lep1_minpt and electrons[i].eta < self.lep1_maxeta]
            if len(self.lep_coll1) < 1:
              return False #No electron was good enough for this cut, so the event selection failed
        if "muons" in lep_dict:
          muons = lep_dict.get("muons")
          if self.lep_coll0 is not None:
            self.lep_coll1 = [muons[i] for i in xrange(len(muons)) if muons[i].pt > self.lep1_minpt and muons[i].eta < self.lep1_maxeta]
            if len(self.lep_coll1) < 1:
              return False #no muon is good enough to pass event selection
          else:
            self.lep_coll0 = [muons[i] for i in xrange(len(muons)) if muons[i].pt > self.lep0_minpt and muons[i].eta < self.lep0_maxeta]
            if len(self.lep_coll0) < 1:
              return False #no muon passed selection and one was expected so discard event
            if len(lep_dict) < 2:
              self.lep_coll1 = [muons[i] for i in xrange(len(muons)) if muons[i].pt > self.lep1_minpt and muons[i].eta < self.lep1_maxeta]
              if len(self.lep_coll1) < 1:
                return False #no muon is good enough to pass event selection
        if "hads" in lep_dict:
          hads = lep_dict.get("hads")
          if self.lep_coll0 is not None:
            self.lep_coll1 = [hads[i] for i in xrange(len(hads)) if hads[i].pt > self.lep1_minpt and hads[i].eta < self.lep1_maxeta]
            if len(self.lep_coll1) < 1:
              return False #no had is good enough to pass event selection
          else:
            self.lep_coll0 = [hads[i] for i in xrange(len(hads)) if hads[i].pt > self.lep0_minpt and hads[i].eta < self.lep0_maxeta]
            if len(self.lep_coll0) < 1:
              return False #no had passed selection and one was expected so discard event
            if len(lep_dict) < 2:
              self.lep_coll1 = [hads[i] for i in xrange(len(hads)) if hads[i].pt > self.lep1_minpt and hads[i].eta < self.lep1_maxeta]
              if len(self.lep_coll1) < 1:
                return False #no had is good enough to pass event selection
              
#       pdb.set_trace()
        #Here we find the two leptons that we are interested in and make sure they match the desired q0q1
        ind0 = -1
        ind1 = -1
        max_max_energy = 0
        self.lep_coll1_p4 = [self.lep_coll1[i].p4() for i in xrange(len(self.lep_coll1))]
        for ind,lep in enumerate(self.lep_coll0):
          pair_energy_check = [(lep.p4()+self.lep_coll1_p4[i]).E() if (lep.charge*self.lep_coll1[i].charge == self.q0q1 and deltaR(lep,self.lep_coll1[i])>0.1) else 0 for i in xrange(len(self.lep_coll1_p4))]
          max_energy = max(pair_energy_check or [0])
          if max_energy > max_max_energy:
            max_max_energy = max_energy
            ind0 = ind
            ind1 = pair_energy_check.index(max_energy)
          else:
            #if it didn't update this time, then it is unlikely to update further down the list because it is momentum sorted 
            break
        if ind0 < 0 or ind1 < 0:
          self.out.fillBranch("havePair",False)
          havePair = False
          return False
        else:
          self.out.fillBranch("havePair",True)
          self.lep0 = self.lep_coll0[ind0]
          self.lep0_p4 = self.lep0.p4()
          self.lep1 = self.lep_coll1[ind1]
          self.lep1_p4 = self.lep1.p4()
        #returns the p4 of the two leptons after collinear approximation
#       pdb.set_trace()
        self.lep0_col_p4,self.lep1_col_p4, back_to_back = self.collinear_approx(self.lep0.p4(),self.lep1.p4(),event.MET_pt,event.MET_phi) 
        self.out.fillBranch("back_to_back",back_to_back)
        self.out.fillBranch("lep0_vis_pt",self.lep0.pt)
        self.out.fillBranch("lep0_vis_eta",self.lep0.eta)
        self.out.fillBranch("lep0_vis_phi",self.lep0.phi)
        self.out.fillBranch("lep0_vis_mass",self.lep0.mass)
        self.out.fillBranch("lep1_vis_pt",self.lep1.pt)
        self.out.fillBranch("lep1_vis_eta",self.lep1.eta)
        self.out.fillBranch("lep1_vis_phi",self.lep1.phi)
        self.out.fillBranch("lep1_vis_mass",self.lep1.mass)
        self.out.fillBranch("ll_vis_pt",(self.lep0_p4+self.lep1_p4).Pt())
        self.out.fillBranch("ll_vis_mass",(self.lep0_p4+self.lep1_p4).M())
        self.out.fillBranch("ll_vis_dr",deltaR(self.lep0,self.lep1))
        self.out.fillBranch("lep0_col_pt",self.lep0_col_p4.Pt())
        self.out.fillBranch("lep0_col_eta",self.lep0_col_p4.Eta())
        self.out.fillBranch("lep0_col_phi",self.lep0_col_p4.Phi())
        self.out.fillBranch("lep0_col_mass",self.lep0_col_p4.M())
        self.out.fillBranch("lep1_col_pt",self.lep1_col_p4.Pt())
        self.out.fillBranch("lep1_col_eta",self.lep1_col_p4.Eta())
        self.out.fillBranch("lep1_col_phi",self.lep1_col_p4.Phi())
        self.out.fillBranch("lep1_col_mass",self.lep1_col_p4.M())
        self.out.fillBranch("ll_col_mass",(self.lep0_col_p4+self.lep1_col_p4).M())
        self.out.fillBranch("ll_col_pt",(self.lep0_col_p4+self.lep1_col_p4).Pt())
        self.out.fillBranch("ll_col_dr",deltaR(self.lep0_col_p4.Eta(),self.lep0_col_p4.Phi(),self.lep1_col_p4.Eta(),self.lep1_col_p4.Phi()))
        self.photon = goodPhotons[0]
        self.photon_p4 = self.photon.p4()
        self.out.fillBranch("photon_pt",self.photon.pt)
        self.out.fillBranch("photon_eta",self.photon.eta)
        self.out.fillBranch("photon_phi",self.photon.phi)
        self.out.fillBranch("gamlep0_vis_mass",(self.photon_p4+self.lep0_p4).M())
        self.out.fillBranch("gamlep0_vis_dr",deltaR(self.lep0,self.photon))
        self.out.fillBranch("gamlep1_vis_mass",(self.photon_p4+self.lep1_p4).M())
        self.out.fillBranch("gamlep1_vis_dr",deltaR(self.lep1,self.photon))
        self.out.fillBranch("gamlep0_col_mass",(self.photon_p4+self.lep0_col_p4).M())
        self.out.fillBranch("gamlep0_col_dr",deltaR(self.photon.eta,self.photon.phi,self.lep0_col_p4.Eta(),self.lep0_col_p4.Phi()))
        self.out.fillBranch("gamlep1_col_mass",(self.photon_p4+self.lep1_col_p4).M())
        self.out.fillBranch("gamlep1_col_dr",deltaR(self.photon.eta,self.photon.phi,self.lep1_col_p4.Eta(),self.lep1_col_p4.Phi()))
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
        MET0 = ROOT.TLorentzVector()
        MET1 = ROOT.TLorentzVector()
        #make array of tau directions to be used for MET decomposition; array elements are ordered first across rows
        METdecompArray = np.array([tau0xydir.X(),tau1xydir.X(),tau0xydir.Y(),tau1xydir.Y()]).reshape(2,2)
        try:
          METdecomp = np.dot(np.linalg.inv(METdecompArray),np.array([MET.X(),MET.Y()])[:,None])
          back_to_back = False
          MET0xy = float(METdecomp[0])*tau0xydir
#          MET0xy = ROOT.TVector3(MET0xy[0],MET0xy[1],MET0xy[2])
          #collinear approx
          MET1xy = float(METdecomp[1])*tau1xydir
#          MET1xy = ROOT.TVector3(MET1xy[0],MET1xy[1],MET1xy[2])
          #collinear approx
        except np.linalg.LinAlgError:
          #if the taus are back to back, choose the one that the MET is closest to and give it to that one
          back_to_back = True
          if MET.Angle(tau0xydir) < MET.Angle(tau1xydir):
            MET0xy = MET.Pt()*tau0xydir
            MET1xy = 0*tau1xydir
          else:
            MET0xy = 0*tau0xydir
            MET1xy = MET.Pt()*tau1xydir
        MET0.SetPtEtaPhiM(MET0xy.Pt(),tau0.Eta(),MET0xy.Phi(),0)
        MET1.SetPtEtaPhiM(MET1xy.Pt(),tau1.Eta(),MET1xy.Phi(),0)
        tau0_col = tau0+MET0
        tau1_col = tau1+MET1
        return tau0_col, tau1_col, back_to_back
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

 
#channel_tautau = lambda : ChannelAnalyzer(4,20,2.3,180,2.1,50,2.5,-1)
channel_elel = lambda : ChannelAnalyzer(1,15,2.3,15,2.3,50,2.5,-1)
channel_mumu = lambda : ChannelAnalyzer(2,15,2.3,15,2.3,50,2.5,-1)
channel_elmu = lambda : ChannelAnalyzer(3,15,2.3,15,2.3,50,2.5,-1)
channel_tautau = lambda : ChannelAnalyzer(4,15,2.3,15,2.3,50,2.5,-1)
channel_eltau = lambda : ChannelAnalyzer(5,15,2.3,15,2.3,50,2.5,-1)
channel_mutau = lambda : ChannelAnalyzer(6,15,2.3,15,2.3,50,2.5,-1)
#channel_elel = lambda : ChannelAnalyzer(1,35,2.5,20,2.3,50,2.5,-1)
#channel_mumu = lambda : ChannelAnalyzer(2,27,2.4,20,2.3,50,2.5,-1)
#channel_elmu = lambda : ChannelAnalyzer(3,20,2.3,20,2.3,50,2.5,-1)
#channel_tautau = lambda : ChannelAnalyzer(4,20,2.3,20,2.3,50,2.5,-1)
#channel_eltau = lambda : ChannelAnalyzer(5,35,2.5,20,2.3,50,2.5,-1)
#channel_mutau = lambda : ChannelAnalyzer(6,27,2.4,20,2.3,50,2.5,-1)
