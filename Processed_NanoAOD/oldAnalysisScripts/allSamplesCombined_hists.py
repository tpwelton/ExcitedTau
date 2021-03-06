#!/usr/bin/env python
import os, sys
import pdb
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class HistMaker(Module):
    def __init__(self):
	self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
      Module.beginJob(self,histFile,histDirName)
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
      self.h_MinMassVsMaxMass=ROOT.TH2F("minMassVsMaxMass","minMassVsMaxMass",200,0,2000,100,0,2000)
      self.addObject(self.h_MinMassVsMaxMass)
      self.h_MinMassVsMaxMass_phiCheck=ROOT.TH2F("minMassVsMaxMass_phiCheck","minMassVsMaxMass_phiCheck",200,0,2000,200,0,2000)
      self.addObject(self.h_MinMassVsMaxMass_phiCheck)
#        self.out.branch("gamlep0_col_mass","D")
#        self.out.branch("gamlep0_col_dr","D")
#        self.out.branch("gamlep1_col_mass","D")
#        self.out.branch("gamlep1_col_dr","D")

    def analyze(self, event):
        if event.photon_pt < 100: return False
        if not (event.channel == 4):
          return False
        self.h_ll_vis_mass.Fill(event.ll_vis_mass)
        self.h_ll_col_mass.Fill(event.ll_col_mass)
        if event.gamlep0_col_mass < event.gamlep1_col_mass:
          self.h_MinMassVsMaxMass.Fill(event.gamlep0_col_mass,event.gamlep1_col_mass)
          if event.missingPtBetween_Reco:
            self.h_MinMassVsMaxMass_phiCheck.Fill(event.gamlep0_col_mass,event.gamlep1_col_mass)
        else:
          self.h_MinMassVsMaxMass.Fill(event.gamlep1_col_mass,event.gamlep0_col_mass)
          if event.missingPtBetween_Reco:
            self.h_MinMassVsMaxMass_phiCheck.Fill(event.gamlep1_col_mass,event.gamlep0_col_mass)
        return True


#preselection="Jet_pt[0] > 250"
#preselection="channel == 6"
preselection=""
#files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
#files=["MuTau2018D/" + files.strip() for files in open("MuTau2018D/MuTau2018D_processed.txt").readlines()]
#files=[files.strip() for files in open("WGToLNuG_NanoAODv7_local.txt").readlines()]
files=["ZGTo2LG_NanoAODv7_processed/" + files.strip() for files in open("ZGTo2LG_NanoAODv7_local.txt").readlines()]
#files=["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD_chan0_allCuts_phiCheck.root"]
#files=["test_1_chan0_allCuts.root"]
#files=["test_1_chan0_allCuts_phiCheck.root"]

p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[HistMaker()],noOut=True,histFileName="ZGTo2LG_TauTau_photon100_hists_slim.root",histDirName="plots",maxEntries=None)
p.run()

