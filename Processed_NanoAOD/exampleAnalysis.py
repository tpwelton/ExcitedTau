#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class HistMaker(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
      Module.beginJob(self,histFile,histDirName)
      self.h_vpt=ROOT.TH1F('sumpt',   'sumpt',   100, 0, 1000)
      self.addObject(self.h_vpt )
#        self.out.branch("channel","b")
#        self.out.branch("back_to_back","O")
#        self.out.branch("lep0_vis_pt","D")
#        self.out.branch("lep0_vis_eta","D")
#        self.out.branch("lep0_vis_phi","D")
#        self.out.branch("lep0_vis_mass","D")
#        self.out.branch("lep1_vis_pt","D")
#        self.out.branch("lep1_vis_eta","D")
#        self.out.branch("lep1_vis_phi","D")
#        self.out.branch("lep1_vis_mass","D")
#        self.out.branch("ll_vis_pt","D")
      self.h_ll_vis_mass=ROOT.TH1F("ll_vis_mass","ll_vis_mass",50,0,500)
      self.addObject(self.h_ll_vis_mass)
#        self.out.branch("ll_vis_dr","D")
#        self.out.branch("gamlep0_vis_mass","D")
#        self.out.branch("gamlep0_vis_dr","D")
#        self.out.branch("gamlep1_vis_mass","D")
#        self.out.branch("gamlep1_vis_dr","D")
#        self.out.branch("photon_pt","D")
#        self.out.branch("photon_eta","D")
#        self.out.branch("photon_phi","D")
#        self.out.branch("havePair","O")
#        self.out.branch("havePhoton","O")
#        self.out.branch("haveTriplet","O")
#        self.out.branch("lep0_col_pt","D")
#        self.out.branch("lep0_col_eta","D")
#        self.out.branch("lep0_col_phi","D")
#        self.out.branch("lep0_col_mass","D")
#        self.out.branch("lep1_col_pt","D")
#        self.out.branch("lep1_col_eta","D")
#        self.out.branch("lep1_col_phi","D")
#        self.out.branch("lep1_col_mass","D")
      self.h_ll_col_mass=ROOT.TH1F("ll_col_mass","ll_col_mass",50,0,500)
      self.addObject(self.h_ll_col_mass)
#        self.out.branch("ll_col_pt","D")
#        self.out.branch("ll_col_dr","D")
#        self.out.branch("gamlep0_col_mass","D")
#        self.out.branch("gamlep0_col_dr","D")
#        self.out.branch("gamlep1_col_mass","D")
#        self.out.branch("gamlep1_col_dr","D")

    def analyze(self, event):
      if not event.channel == 6:
        return False
      if event.channel == 6:
        if not (event.HLT_IsoMu24 or event.HLT_IsoMu27 or event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1):
          return False
      self.h_ll_vis_mass.Fill(event.ll_vis_mass)
      self.h_ll_col_mass.Fill(event.ll_col_mass)


#preselection="Jet_pt[0] > 250"
preselection=""
#files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
files=["MuTau2018D/" + files.strip() for files in open("MuTau2018D/MuTau2018D_processed.txt").readlines()]
files=["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[HistMaker()],noOut=True,histFileName="MuTauSignal1000_photon100.root")
p.run()
