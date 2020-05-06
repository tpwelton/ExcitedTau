import pdb
import os

#modLoc0 = "PhysicsTools.NanoAODTools.postprocessing.modules.ExcitedTau.GenTauDecayFlavor "
modLoc0 = "PhysicsTools.NanoAODTools.postprocessing.modules.ExcitedTau.EventSelection "
modLocElse = "PhysicsTools.NanoAODTools.postprocessing.modules.ExcitedTau.ChannelAnalyzer "

modules = []
#modules.append("genTauDecayFlavor")
modules.append("event_selection_min")
modules.append("channel_elel")
modules.append("channel_mumu")
modules.append("channel_elmu")
modules.append("channel_tautau")
modules.append("channel_eltau")
modules.append("channel_mutau")

#which channels to include
include = [0]
#include = [1,2,3,4,5,6]
#include = [3]
#f = open("../../../ExcitedTau/Processed_NanoAOD/TauTau2018D/TauTau2018D_files.txt","r")
#f = open("../../../ExcitedTau/TauTau2016B_files.txt","r")
#f = open("../../../ExcitedTau/Processed_NanoAOD/ElMu2018D.txt","r")
#f = open("../../../ExcitedTau/Processed_NanoAOD/MuTau2018C.txt","r")
f = open("../../../ExcitedTau/EmbeddedSamples_NanoAOD/TauTau2018D/TauTau2018D_local.txt")
#f = open("../../../ExcitedTau/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD_files.txt","r")
files = f.readlines()
#f.close()
#files = ["root://cmseos.fnal.gov//store/user/twelton/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD/Taustar_TauG_L10000_m250_13TeV_pythia8_GEN-SIM/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD/200222_093547/0000/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD_1.root"]
#files = ["root://cmseos.fnal.gov//store/user/twelton/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD/Taustar_TauG_L10000_m250_13TeV_pythia8_GEN-SIM/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD/200318_120803/0000/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD_1.root"]
#files = ["root://cmseos.fnal.gov//store/user/twelton/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD/Taustar_TauG_L10000_m250_13TeV_pythia8_GEN-SIM/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD/200324_011356/0000/test_1.root"]
#files = ["../../NanoAOD/Taustar_TauG_L10000_m250_13TeV_pythia8_NanoAOD.root"]
#files = ["../../NanoAOD/Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD.root"]

for file in files:
#  os.system("python scripts/nano_postproc.py ../../../ExcitedTau/Processed_NanoAOD " + file.strip() + " -I PhysicsTools.NanoAODTools.postprocessing.modules.ExcitedTau.ChannelAnalyzer channel_tautau -s _proc") 
#  pdb.set_trace()
  for num, mod in enumerate(modules):
    if num in include:
      if num == 0:
        modLoc = modLoc0
      else:
        modLoc = modLocElse
#      cmd = "python scripts/nano_postproc.py ../../../ExcitedTau/Processed_NanoAOD ../../../ExcitedTau/EmbeddedSamples_NanoAOD/TauTau2018D/" + file.strip() + " -I " + modLoc + mod + " -s _chan" + str(num)
      cmd = "python scripts/nano_postproc.py ../../../ExcitedTau/Processed_NanoAOD " + file.strip() + " -I " + modLoc + mod + " -s _chan" + str(num)
      cmd = cmd + "_allCuts"
#      cmd = cmd + "_2taus"
#      cmd = cmd + "_jetCut"
#      cmd = cmd + "_pairCut"
#      cmd = cmd + "_deltaRcut"
#      cmd = cmd + "_loose"
#      cmd = cmd + "_tight"
#      cmd = cmd + "_tauCompat"
#      cmd = cmd + "_photon"
#      pdb.set_trace()
      os.system(cmd)
#  break
