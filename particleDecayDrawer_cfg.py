import FWCore.ParameterSet.Config as cms

process = cms.Process("Analysis")

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
#      '/store/mc/RunIIFall15MiniAODv2/Taustar_TauG_L10000_m250_13TeV-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/50000/1CE7319C-3CCE-E511-B917-7845C4FC379D.root'
      'root://cms-xrd-global.cern.ch//store/user/twelton/TaustarMC/Taustar_TauG_L10000_m250_CP5_13TeV_pythia8/Taustar_TauG_L10000_m250_CP5_13TeV_pythia8_2018/201025_011056/0000/tree_1.root'
   )
)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(10)
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printDecay = cms.EDAnalyzer("ParticleDecayDrawer",
#   src = cms.InputTag("prunedGenParticles"),
   src = cms.InputTag("genParticles"),
   printP4 = cms.untracked.bool(False),
   printPtEtaPhi = cms.untracked.bool(True),
   printVertex = cms.untracked.bool(False),
)

process.p = cms.Path(process.printDecay)

