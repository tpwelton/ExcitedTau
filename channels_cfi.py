import FWCore.ParameterSet.Config as cms

### mu + mu ###
Channel_MuMu = cms.EDAnalyzer("ChannelAnalyzer",
   leptonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodMuons:goodMuons"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(20.),
   maxeta_lepton = cms.double(2.3),
   minpt_tau = cms.double(180.),
   maxeta_tau = cms.double(2.1),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
)
### e + e ###
Channel_ElEl = cms.EDAnalyzer("ChannelAnalyzer",
   leptonCollection = cms.InputTag("goodElectrons:goodElectrons"),
   tauCollection = cms.InputTag("goodElectrons:goodElectrons"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(20.),
   maxeta_lepton = cms.double(2.3),
   minpt_tau = cms.double(180.),
   maxeta_tau = cms.double(2.1),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
)
### mu + e ###
Channel_MuEl = cms.EDAnalyzer("ChannelAnalyzer",
   leptonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodElectrons:goodElectrons"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(20.),
   maxeta_lepton = cms.double(2.3),
   minpt_tau = cms.double(180.),
   maxeta_tau = cms.double(2.1),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
)
### mu + tau ###
Channel_MuTau = cms.EDAnalyzer("ChannelAnalyzer",
   leptonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(27.),
   maxeta_lepton = cms.double(2.4),
   minpt_tau = cms.double(20.),
   maxeta_tau = cms.double(2.3),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
)
### e + tau
Channel_ElTau = cms.EDAnalyzer("ChannelAnalyzer",
   leptonCollection = cms.InputTag("goodElectrons:goodElectrons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(35.),
   maxeta_lepton = cms.double(2.5),
   minpt_tau = cms.double(20.),
   maxeta_tau = cms.double(2.3),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
)
### tau + tau ###
Channel_TauTau = cms.EDAnalyzer("ChannelAnalyzer",
   leptonCollection = cms.InputTag("goodTaus:goodTaus"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(20.),
   maxeta_lepton = cms.double(2.3),
   minpt_tau = cms.double(180.),
   maxeta_tau = cms.double(2.1),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
)

