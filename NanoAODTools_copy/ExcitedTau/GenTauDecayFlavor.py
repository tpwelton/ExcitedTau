import pdb
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

#need this for the collinear approximation function
import numpy as np
import math

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR


class GenTauDecayFlavor(Module):
    def __init__(self):#, channel_code, lep0_minpt, lep0_maxeta, lep1_minpt, lep1_maxeta, photon_minpt, photon_maxeta, q0q1):
#       self.channel_code = channel_code
#       self.lep0_minpt = lep0_minpt
#       self.lep0_maxeta = lep0_maxeta
#       self.lep1_minpt = lep1_minpt
#       self.lep1_maxeta = lep1_maxeta
#       self.photon_minpt = photon_minpt
#       self.photon_maxeta = photon_maxeta
#       self.q0q1 = q0q1 #sign between lepton charge pair
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("channel","b")
#       self.out.branch("back_to_back","O")
#       self.out.branch("lep0_vis_pt","D")
#       self.out.branch("lep0_vis_eta","D")
#       self.out.branch("lep0_vis_phi","D")
#       self.out.branch("lep0_vis_mass","D")
#       self.out.branch("lep1_vis_pt","D")
#       self.out.branch("lep1_vis_eta","D")
#       self.out.branch("lep1_vis_phi","D")
#       self.out.branch("lep1_vis_mass","D")
#       self.out.branch("ll_vis_pt","D")
#       self.out.branch("ll_vis_mass","D")
#       self.out.branch("ll_vis_dr","D")
#       self.out.branch("gamlep0_vis_mass","D")
#       self.out.branch("gamlep0_vis_dr","D")
#       self.out.branch("gamlep1_vis_mass","D")
#       self.out.branch("gamlep1_vis_dr","D")
#       self.out.branch("photon_pt","D")
#       self.out.branch("photon_eta","D")
#       self.out.branch("photon_phi","D")
#       self.out.branch("havePair","O")
#       self.out.branch("havePhoton","O")
#       self.out.branch("haveTriplet","O")
#       self.out.branch("lep0_col_pt","D")
#       self.out.branch("lep0_col_eta","D")
#       self.out.branch("lep0_col_phi","D")
#       self.out.branch("lep0_col_mass","D")
#       self.out.branch("lep1_col_pt","D")
#       self.out.branch("lep1_col_eta","D")
#       self.out.branch("lep1_col_phi","D")
#       self.out.branch("lep1_col_mass","D")
#       self.out.branch("ll_col_mass","D")
#       self.out.branch("ll_col_pt","D")
#       self.out.branch("ll_col_dr","D")
#       self.out.branch("gamlep0_col_mass","D")
#       self.out.branch("gamlep0_col_dr","D")
#       self.out.branch("gamlep1_col_mass","D")
#       self.out.branch("gamlep1_col_dr","D")
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        genParts = Collection(event,"GenPart")
        channel = 0
        numTaus = 0
        for ind in xrange(len(genParts)):
          if abs(genParts[ind].pdgId) == 16:
            numTaus += 1
            genPartId = genParts[ind+1].pdgId
            if abs(genPartId) == 11:
              channel = channel | (1 << 0)
            elif abs(genPartId) == 13:
              channel = channel | (1 << 1)
            else:
              channel = channel | (1 << 2)
        if numTaus > 2:
          print([genParts[i].pdgId for i in xrange(len(genParts))])
          channel = int(input("Please enter the channel to be recorded:"))
        self.out.fillBranch("channel",channel)
        return True
# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

genTauDecayFlavor = lambda : GenTauDecayFlavor()
 
