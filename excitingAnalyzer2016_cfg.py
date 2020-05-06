import FWCore.ParameterSet.Config as cms

process = cms.Process("analysis")

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')
options.register('nevents',
   1,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.int,
   "Number of events in the dataset."
)
options.register('xs',
   1.,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.float,
   "Cross section of the dataset process."
)
options.register('isSignalMC',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Is this signal MC?"
)
options.register('applyFilter',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Apply skim requiring at least 1 loose tau?"
)
options.register('isMC',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Is this simulation?"
)
options.register('doSS',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "do SS channels?"
)

options.parseArguments()
if options.isSignalMC:
   options.isMC = True

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.GlobalTag.globaltag = '102X_upgrade2018_realistic_v18'
process.GlobalTag.globaltag = '94X_mcRun2_asymptotic_v3'
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Geometry.CaloEventSetup.CaloTopology_cfi')
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
#setupEgammaPostRecoSeq(process,era='2018-Prompt')
setupEgammaPostRecoSeq(process,
                       runVID=True,
                       runEnergyCorrections=False, #no point in re-running them, they are already fine
                       era='2016-Legacy')  #era is new to select between 2016 / 2017,  it defaults to 2017
#a sequence egammaPostRecoSeq has now been created and should be added to your path, eg process.p=cms.Path(process.egammaPostRecoSeq)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

if options.isSignalMC:
   infile = "/store/mc/RunIIFall15MiniAODv2/Taustar_TauG_L10000_m250_13TeV-pythia8/MINIAODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/60000/E4F9CE0A-5BCE-E511-8E00-002590D60026.root"
else:
   infile = "/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/FD444175-C881-DC48-B2EC-604BF12A182F.root"

#infile = "./filelists/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8.list", outfile = "./mcsamples/GJets_DR-0p4_HT-100To200.root"
#infile = "./filelists/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8.list", outfile = "/mcsamples/GJets_DR-0p4_HT-200To400.root"
#infile = "./filelists/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8.list", outfile = "/mcsamples/GJets_DR-0p4_HT-400To600.root"
#infile = "./filelists/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8.list", outfile = "/mcsamples/GJets_DR-0p4_HT-600ToInf.root"
#infile = './filelists/Taustar_TauG_L10000_m250_13TeV-pythia8.list'
#outfile = "./mcsamples/Taustar_m250.root"
#infile = "./filelists/Taustar_TauG_L10000_m500_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m500.root"
#infile = "./filelists/Taustar_TauG_L10000_m750_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m750.root"
#infile = "./filelists/Taustar_TauG_L10000_m1000_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m1000.root"
#infile = "./filelists/Taustar_TauG_L10000_m1250_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m1250.root"
#infile = "./filelists/Taustar_TauG_L10000_m1500_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m1500.root"
#infile = "./filelists/Taustar_TauG_L10000_m1750_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m1750.root"
#infile = "./filelists/Taustar_TauG_L10000_m2000_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m2000.root"
#infile = "./filelists/Taustar_TauG_L10000_m2250_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m2250.root"
#infile = "./filelists/Taustar_TauG_L10000_m2500_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m2500.root"
#infile = "./filelists/Taustar_TauG_L10000_m2750_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m2750.root"
#infile = "./filelists/Taustar_TauG_L10000_m3000_13TeV-pythia8.list"
#outfile = "./mcsamples/Taustar_m3000.root"
#import FWCore.Utilities.FileUtils as FileUtils
#mylist = FileUtils.loadListFromFile(infile)
#readFiles = cms.untracked.vstring(*mylist)

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(infile)
   #fileNames = readFiles
)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(-1)
)

process.TFileService = cms.Service("TFileService",
   fileName = cms.string("output.root")
   #fileName = cms.string(outfile)
)

process.options = cms.untracked.PSet(
   wantSummary = cms.untracked.bool(True),
)

mypath = cms.Sequence()

updatedTauName = "slimmedTausNewID" #name of pat::Tau collection with new tau-Ids
import RecoTauTag.RecoTau.tools.runTauIdMVA as tauIdConfig
tauIdEmbedder = tauIdConfig.TauIDEmbedder(process, cms, debug = False,
                    updatedTauName = updatedTauName,
                    toKeep = ["deepTau2017v2p1", #deepTau TauIDs
                               ])
tauIdEmbedder.runTauID()

process.goodTaus = cms.EDFilter("TauProducer",
   tauCollection = cms.InputTag(updatedTauName),
   minpt = cms.double(20.),
   maxeta = cms.double(2.3),
   applyFilter = cms.bool(options.applyFilter)
)
mypath = mypath * process.rerunMvaIsolationSequence * getattr(process,updatedTauName) * process.goodTaus

process.goodPhotons = cms.EDFilter("PhotonProducer",
   photonCollection = cms.InputTag("slimmedPhotons"),
   minpt = cms.double(50.),
   maxeta = cms.double(2.5),
   applyFilter = cms.bool(False),
)
mypath = mypath * process.egammaPostRecoSeq * process.goodPhotons

process.goodElectrons = cms.EDFilter("ElectronProducer",
   electronCollection = cms.InputTag("slimmedElectrons"),
   minpt = cms.double(35.),
   maxeta = cms.double(2.5),
   applyFilter = cms.bool(False),
)
mypath = mypath * process.goodElectrons

process.goodVertices = cms.EDFilter("VertexSelector",
   src = cms.InputTag("offlineSlimmedPrimaryVertices"),
   cut = cms.string("!isFake && ndof > 4 && abs(z) < 24 && position.Rho < 2"),
   filter = cms.bool(False)
)
mypath = mypath * process.goodVertices

process.goodMuons = cms.EDFilter("MuonProducer",
   muonCollection = cms.InputTag("slimmedMuons"),
   vertexCollection = cms.InputTag("goodVertices"),
   minpt = cms.double(27.),
   maxeta = cms.double(2.4),
   isSignalMC = cms.bool(options.isSignalMC),
   applyFilter = cms.bool(False)
)
mypath = mypath * process.goodMuons

jetTag = cms.InputTag("slimmedJets")
if options.isSignalMC:
   #https://twiki.cern.ch/CMS/JetToolbox
   from JMEAnalysis.JetToolbox.jetToolbox_cff import jetToolbox
   jetToolbox(
      process, #process
      'ak4', #jetType
      'jetSequence', #sequence
      'noOutput', #outputModules
      JETCorrPayload='AK4PFchs',
      bTagDiscriminators = ['pfDeepCSVJetTags:probb', 'pfDeepCSVJetTags:probbb']
   )
   jetTag = cms.InputTag("selectedPatJetsAK4PFCHS")
   mypath = process.jetSequence * mypath

process.goodJets = cms.EDProducer("JetProducer",
   jetCollection = jetTag,
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   minpt = cms.double(30.),
   maxeta = cms.double(2.6)
)
mypath = mypath * process.goodJets

process.triggerProducer = cms.EDFilter("TriggerProducer",
   bits = cms.InputTag("TriggerResults", "", "HLT"),
   #prescales = cms.InputTag("patTrigger"),
   #applyFilter = cms.bool(False)
)
mypath = mypath * process.triggerProducer

xsWeight_ = options.xs / options.nevents
process.eventAnalyzer = cms.EDAnalyzer("EventAnalyzer",
   electronCollection = cms.InputTag("goodElectrons:goodElectrons"),
   muonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   vertexCollection = cms.InputTag("goodVertices"),
   genParticleCollection = cms.InputTag("prunedGenParticles"),
   metCollection = cms.InputTag("slimmedMETs"),
   jetCollection = cms.InputTag("goodJets:goodJets"),
   xsWeight = cms.double(xsWeight_)
)
mypath = mypath * process.eventAnalyzer

'''### mu + mu ###
process.osMuMuPairProducer = cms.EDProducer("LeptonPairProducer",
   leptonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodMuons:goodMuons"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(27.),
   maxeta_lepton = cms.double(2.4),
   minpt_tau = cms.double(27.),
   maxeta_tau = cms.double(2.4),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
   applyFilter = cms.bool(False),
   isMC = cms.bool(options.isSignalMC),
   genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"),
)
process.osMuMuPairAnalyzer = cms.EDAnalyzer("LeptonPairAnalyzer",
   visibleTauCollection = cms.InputTag("osMuMuPairProducer:visibleTaus"),
   collinearTauCollection = cms.InputTag("osMuMuPairProducer:collinearTaus"),
   photonCollection = cms.InputTag("osMuMuPairProducer:selectedPhoton")
)

### e + e ###
process.osEEPairProducer = cms.EDProducer("LeptonPairProducer",
   leptonCollection = cms.InputTag("goodElectrons:goodElectrons"),
   tauCollection = cms.InputTag("goodElectrons:goodElectrons"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(35.),
   maxeta_lepton = cms.double(2.5),
   minpt_tau = cms.double(35.),
   maxeta_tau = cms.double(2.5),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
   applyFilter = cms.bool(False),
   isMC = cms.bool(options.isSignalMC),
   genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"),
)
process.osEEPairAnalyzer = cms.EDAnalyzer("LeptonPairAnalyzer",
   visibleTauCollection = cms.InputTag("osEEPairProducer:visibleTaus"),
   collinearTauCollection = cms.InputTag("osEEPairProducer:collinearTaus"),
   photonCollection = cms.InputTag("osEEPairProducer:selectedPhoton")
)

### e + mu ###
process.osEMuPairProducer = cms.EDProducer("LeptonPairProducer",
   leptonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodElectrons:goodElectrons"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(27.),
   maxeta_lepton = cms.double(2.4),
   minpt_tau = cms.double(35.),
   maxeta_tau = cms.double(2.5),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
   applyFilter = cms.bool(False),
   isMC = cms.bool(options.isSignalMC),
   genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"),
)
process.osEMuPairAnalyzer = cms.EDAnalyzer("LeptonPairAnalyzer",
   visibleTauCollection = cms.InputTag("osEMuPairProducer:visibleTaus"),
   collinearTauCollection = cms.InputTag("osEMuPairProducer:collinearTaus"),
   photonCollection = cms.InputTag("osEMuPairProducer:selectedPhoton")
)
'''
### mu + tau ###
process.osMuTauPairProducer = cms.EDProducer("LeptonPairProducer",
   leptonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   eVeto_tau = cms.string("byVVVLooseDeepTau2017v2p1VSe"),
   muVeto_tau = cms.string("byVLooseDeepTau2017v2p1VSmu"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(27.),
   maxeta_lepton = cms.double(2.4),
   minpt_tau = cms.double(20.),
   maxeta_tau = cms.double(2.3),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
   applyFilter = cms.bool(False),   
 #  isMC = cms.bool(options.isSignalMC),
 #  genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"),
)
process.osMuTauPairAnalyzer = cms.EDAnalyzer("LeptonPairAnalyzer",
   visibleTauCollection = cms.InputTag("osMuTauPairProducer:visibleTaus"),
   collinearTauCollection = cms.InputTag("osMuTauPairProducer:collinearTaus"),
   photonCollection = cms.InputTag("osMuTauPairProducer:selectedPhoton")
)
mypath = mypath * process.osMuTauPairProducer * process.osMuTauPairAnalyzer

### e + tau ###
process.osETauPairProducer = cms.EDProducer("LeptonPairProducer",
   leptonCollection = cms.InputTag("goodElectrons:goodElectrons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(35.),
   maxeta_lepton = cms.double(2.5),
   minpt_tau = cms.double(20.),
   maxeta_tau = cms.double(2.3),
   eVeto_tau = cms.string("byVVVLooseDeepTau2017v2p1VSe"),
   muVeto_tau = cms.string("byVLooseDeepTau2017v2p1VSmu"),
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
   applyFilter = cms.bool(False),
   #isMC = cms.bool(options.isSignalMC),
   #genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"),
)
process.osETauPairAnalyzer = cms.EDAnalyzer("LeptonPairAnalyzer",
   visibleTauCollection = cms.InputTag("osETauPairProducer:visibleTaus"),
   collinearTauCollection = cms.InputTag("osETauPairProducer:collinearTaus"),
   photonCollection = cms.InputTag("osETauPairProducer:selectedPhoton")
)
mypath = mypath * process.osETauPairProducer * process.osETauPairAnalyzer

### tau + tau ###
process.osTauTauPairProducer = cms.EDProducer("LeptonPairProducer",
   leptonCollection = cms.InputTag("goodTaus:goodTaus"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   metCollection = cms.InputTag("slimmedMETs"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   minpt_lepton = cms.double(20.),
   maxeta_lepton = cms.double(2.3),
   minpt_tau = cms.double(180.),
   maxeta_tau = cms.double(2.1),
   eVeto_tau = cms.string("byVVVLooseDeepTau2017v2p1VSe"),
   muVeto_tau = cms.string("byVLooseDeepTau2017v2p1VSmu"),   
   minpt_photon = cms.double(50.),
   maxeta_photon = cms.double(2.5),
   q1q2 = cms.int32(-1),
   #isMC = cms.bool(options.isSignalMC),
   #genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"),
)
process.osTauTauPairAnalyzer = cms.EDAnalyzer("LeptonPairAnalyzer",
   visibleTauCollection = cms.InputTag("osTauTauPairProducer:visibleTaus"),
   collinearTauCollection = cms.InputTag("osTauTauPairProducer:collinearTaus"),
   photonCollection = cms.InputTag("osTauTauPairProducer:selectedPhoton")
)
mypath = mypath * process.osTauTauPairProducer * process.osTauTauPairAnalyzer

if options.isMC:
   process.genVisTauProducer = cms.EDProducer("GenVisTauProducer",
      genParticleCollection = cms.InputTag("prunedGenParticles")
   )
   mypath = mypath * process.genVisTauProducer

if options.isSignalMC:
   process.genSignalAnalyzer = cms.EDAnalyzer("GenSignalAnalyzer",
      genParticleCollection = cms.InputTag("prunedGenParticles"),
      metCollection = cms.InputTag("slimmedMETs")
   )
   mypath = mypath * process.genSignalAnalyzer

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
   src = cms.InputTag("prunedGenParticles"),
   printP4 = cms.untracked.bool(False),
   printPtEtaPhi = cms.untracked.bool(True),
   printVertex = cms.untracked.bool(False),
   printStatus = cms.untracked.bool(True),
   printIndex = cms.untracked.bool(False),
   #status = cms.untracked.vint32(3),
)

if options.doSS:
   ### mu + tau ###
   process.ssMuTauPairProducer = process.osMuTauPairProducer.clone()
   process.ssMuTauPairProducer.q1q2 = cms.int32(1)
   process.ssMuTauPairAnalyzer = process.osMuTauPairAnalyzer.clone()
   process.ssMuTauPairAnalyzer.visibleTauCollection = cms.InputTag("ssMuTauPairProducer:visibleTaus")
   process.ssMuTauPairAnalyzer.collinearTauCollection = cms.InputTag("ssMuTauPairProducer:collinearTaus")
   process.ssMuTauPairAnalyzer.photonCollection = cms.InputTag("ssMuTauPairProducer:selectedPhoton")
   mypath = mypath * process.ssMuTauPairProducer * process.ssMuTauPairAnalyzer
   ### e + tau ###
   process.ssETauPairProducer = process.osETauPairProducer.clone()
   process.ssETauPairProducer.q1q2 = cms.int32(1)
   process.ssETauPairAnalyzer = process.osETauPairAnalyzer.clone()
   process.ssETauPairAnalyzer.visibleTauCollection = cms.InputTag("ssETauPairProducer:visibleTaus")
   process.ssETauPairAnalyzer.collinearTauCollection = cms.InputTag("ssETauPairProducer:collinearTaus")
   process.ssETauPairAnalyzer.photonCollection = cms.InputTag("ssETauPairProducer:selectedPhoton")
   mypath = mypath * process.ssETauPairProducer * process.ssETauPairAnalyzer
   ### tau + tau ###
   process.ssTauTauPairProducer = process.osTauTauPairProducer.clone()
   process.ssTauTauPairProducer.q1q2 = cms.int32(1)
   process.ssTauTauPairAnalyzer = process.osTauTauPairAnalyzer.clone()
   process.ssTauTauPairAnalyzer.visibleTauCollection = cms.InputTag("ssTauTauPairProducer:visibleTaus")
   process.ssTauTauPairAnalyzer.collinearTauCollection = cms.InputTag("ssTauTauPairProducer:collinearTaus")
   process.ssTauTauPairAnalyzer.photonCollection = cms.InputTag("ssTauTauPairProducer:selectedPhoton")
   mypath = mypath * process.ssTauTauPairProducer * process.ssTauTauPairAnalyzer

#process.Tracer = cms.Service("Tracer")
process.p = cms.Path(mypath)

