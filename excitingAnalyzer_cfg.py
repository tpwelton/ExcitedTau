import FWCore.ParameterSet.Config as cms

process = cms.Process("analysis")

#https://twiki.cern.ch/CMSPublic/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T
import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')
options.register('nEvents',
   1,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.int,
   "Number of events in the dataset."
)
options.register('xs',
   1.,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.float,
   "Cross section of the MC process."
)
options.register('isSignalMC',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Is this signal MC?"
)
options.register('applyTauFilter',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Apply skim requiring at least 1 loose hadronic tau?"
)
options.register('isMC',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Is this simulation?"
)
options.register("doMuMu",
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include MuMu channel?"
)
options.register("doElEl",
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include ElEl channel?"
)
options.register("doMuEl",
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include MuEl channel?"
)
options.register("doMuTau",
   True,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include MuTau channel?"
)
options.register("doElTau",
   True,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include ElTau channel?"
)
options.register("doTauTau",
   True,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include TauTau channel?"
)
options.register('doSS',
   False,
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.bool,
   "Include SS channels?"
)
options.register('globalTag',
   '',
   VarParsing.VarParsing.multiplicity.singleton,
   VarParsing.VarParsing.varType.string,
   "globalTag"
)

options.parseArguments()

if options.isSignalMC:
   options.isMC = True

if options.isMC:
   if options.globalTag=="":
      options.globalTag="102X_upgrade2018_realistic_v19"
   if options.isSignalMC:
      infile = "file:/uscms_data/d3/twelton/WorkingArea/CMSSW_10_2_16/src/AOD/Taustar_TauG_L10000_m175_13TeV_pythia8_MiniAOD.root"
      outfile = "./output_sig.root"
   else:
      infile = "/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/270000/FD444175-C881-DC48-B2EC-604BF12A182F.root"
      outfile = "./output_mc.root"
else:
   if options.globalTag=="":
      options.globalTag="102X_dataRun2_v11"
   infile = "/store/data/Run2018A/JetHT/MINIAOD/PromptReco-v3/000/316/985/00000/F2F7664B-B366-E811-A007-FA163EF336AB.root"
   outfile = "./output_data.root"

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = options.globalTag
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Geometry.CaloEventSetup.CaloTopology_cfi')
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,era='2018-Prompt')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(infile)
)

process.maxEvents = cms.untracked.PSet(
   input = cms.untracked.int32(100)
)

process.TFileService = cms.Service("TFileService",
   fileName = cms.string(outfile)
)

process.options = cms.untracked.PSet(
   wantSummary = cms.untracked.bool(True),
)

mypath = cms.Sequence()

if options.applyTauFilter:
   process.tauFilter = cms.EDFilter("TauFilter",
      tauCollection = cms.InputTag("slimmedTaus"),
      minpt = cms.double(20.),
      maxeta = cms.double(2.3),
   )
   mypath = mypath * process.tauFilter

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
   applyFilter = cms.bool(False)
)
mypath = mypath * process.rerunMvaIsolationSequence * getattr(process,updatedTauName) * process.goodTaus

process.triggerProducer = cms.EDFilter("TriggerProducer",
   bits = cms.InputTag("TriggerResults", "", "HLT"),
   prescales = cms.InputTag("patTrigger"),
   applyFilter = cms.bool(not options.isMC),
   triggerList = cms.vstring(
      #https://twiki.cern.ch/CMS/TauTrigger#Trigger_table_for_2018
      "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v",
      "HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v",
      "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v", #add
      "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_CrossL1_v",
      "HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1_v", #add
      "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v",
      "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v", #add
      "HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTauHPS30_eta2p1_CrossL1_v",
      "HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTau30_eta2p1_CrossL1_v", #add
      "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "HLT_MediumChargedIsoPFTau200HighPtRelaxedIso_Trk50_eta2p1_v",
      #https://twiki.cern.ch/CMS/MuonHLT2018
      "HLT_IsoMu24_v",
      "HLT_Mu50_v",
      "HLT_OldMu100_v",
      "HLT_TkMu100_v",
      #https://twiki.cern.ch/CMS/EgHLTRunIISummary#2018
      "HLT_Ele32_WPTight_Gsf_v",
      "HLT_Ele115_CaloIdVT_GsfTrkIdT_v",
      "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v",
      "HLT_Photon200_v",
      "HLT_Photon175_v",
   ),
   triggerList_HT = cms.vstring(
      # reference triggers
      "HLT_PFHT180_v",
      "HLT_PFHT250_v",
      "HLT_PFHT350_v",
      "HLT_PFHT370_v",
      "HLT_PFHT430_v",
      "HLT_PFHT510_v",
      "HLT_PFHT590_v",
      "HLT_PFHT680_v",
      "HLT_PFHT780_v",
      "HLT_PFHT890_v",
      "HLT_PFHT1050_v",
   ),
   triggerList_HTMHT = cms.vstring(
      #reference triggers
      "HLT_PFHT500_PFMET100_PFMHT100_IDTight_v",
      "HLT_PFHT500_PFMET110_PFMHT110_IDTight_v",
      "HLT_PFHT700_PFMET85_PFMHT85_IDTight_v",
      "HLT_PFHT700_PFMET95_PFMHT95_IDTight_v",
      "HLT_PFHT800_PFMET75_PFMHT75_IDTight_v",
      "HLT_PFHT800_PFMET85_PFMHT85_IDTight_v",
      #"HLT_PFMET100_PFMHT100_IDTight_PFHT60_v",
      #"HLT_PFMET120_PFMHT120_IDTight_PFHT60_v",
      #"HLT_PFMETTypeOne120_PFMHT120_IDTight_PFHT60_v",
      #"HLT_PFMETTypeOne100_PFMHT100_IDTight_PFHT60_v",
   ),
   triggerList_MET = cms.vstring(
      #reference triggers
      "HLT_PFMET110_PFMHT110_IDTight_v",
      "HLT_PFMET120_PFMHT120_IDTight_v",
      "HLT_PFMET130_PFMHT130_IDTight_v",
      "HLT_PFMET140_PFMHT140_IDTight_v",
      #"HLT_PFMETTypeOne110_PFMHT110_IDTight_v",
      #"HLT_PFMETTypeOne120_PFMHT120_IDTight_v",
      #"HLT_PFMETTypeOne130_PFMHT130_IDTight_v",
      #"HLT_PFMETTypeOne140_PFMHT140_IDTight_v",
   )
)

mypath = mypath * process.triggerProducer

process.goodPhotons = cms.EDFilter("PhotonProducer",
   photonCollection = cms.InputTag("slimmedPhotons"),
   minpt = cms.double(50.),
   maxeta = cms.double(2.5),
   applyFilter = cms.bool(False),
)

process.goodElectrons = cms.EDFilter("ElectronProducer",
   electronCollection = cms.InputTag("slimmedElectrons"),
   minpt = cms.double(35.),
   maxeta = cms.double(2.5),
   applyFilter = cms.bool(False),
)
mypath = mypath * process.egammaPostRecoSeq * process.goodPhotons * process.goodElectrons

process.goodVertices = cms.EDFilter("VertexSelector",
   src = cms.InputTag("offlineSlimmedPrimaryVertices"),
   cut = cms.string("!isFake && ndof > 4 && abs(z) < 24 && position.Rho < 2"),
   filter = cms.bool(False)
)
mypath = mypath * process.goodVertices

process.goodMuons = cms.EDFilter("MuonProducer",
   muonCollection = cms.InputTag("slimmedMuons"),
   minpt = cms.double(27.),
   maxeta = cms.double(2.4),
   applyFilter = cms.bool(False)
)
mypath = mypath * process.goodMuons

process.goodJets = cms.EDProducer("JetProducer",
   jetCollection = cms.InputTag("slimmedJets"),
   minpt = cms.double(30.),
   maxeta = cms.double(2.6),
   electronCollection = cms.InputTag("goodElectrons:goodElectrons"),
   muonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
)
mypath = mypath * process.goodJets

if options.doMuMu:
   from channels_cfi import Channel_MuMu
   process.channel_MuMu = Channel_MuMu.clone()
   mypath = mypath * process.channel_OSMuMu
   if options.doSS:
      process.channel_SSMuMu = Channel_MuMu.clone(q1q1=-1)
      mypath = mypath * process.channel_SSMuMu

if options.doElEl:
   from channels_cfi import Channel_ElEl
   process.channel_OSElEl = Channel_ElEl.clone()
   mypath = mypath * process.channel_OSElEl
   if options.doSS:
      process.channel_SSElEl = Channel_EE.clone(q1q1=-1)
      mypath = mypath * process.channel_SSElEl

if options.doMuEl:
   from channels_cfi import Channel_MuEl
   process.channel_OSMuEl = Channel_MuEl.clone()
   mypath = mypath * process.channel_OSMuEl
   if options.doSS:
      process.channel_SSMuEl = Channel_MuEl.clone(q1q1=-1)
      mypath = mypath * process.channel_SSMuEl

if options.doMuTau:
   from channels_cfi import Channel_MuTau
   process.channel_OSMuTau = Channel_MuTau.clone()
   mypath = mypath * process.channel_OSMuTau
   if options.doSS:
      process.channel_SSMuTau = Channel_MuTau.clone(q1q1=-1)
      mypath = mypath * process.channel_SSMuTau

if options.doElTau:
   from channels_cfi import Channel_ElTau
   process.channel_OSElTau = Channel_ElTau.clone()
   mypath = mypath * process.channel_OSElTau
   if options.doSS:
      process.channel_SSElTau = Channel_ElTau.clone(q1q1=-1)
      mypath = mypath * process.channel_SSElTau

if options.doTauTau:
   from channels_cfi import Channel_TauTau
   process.channel_OSTauTau = Channel_TauTau.clone()
   mypath = mypath * process.channel_OSTauTau
   if options.doSS:
      process.channel_SSTauTau = Channel_TauTau.clone(q1q1=-1)
      mypath = mypath * process.channel_SSTauTau

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

xsWeight_ = options.xs / options.nEvents
process.eventAnalyzer = cms.EDAnalyzer("EventAnalyzer",
   electronCollection = cms.InputTag("goodElectrons:goodElectrons"),
   muonCollection = cms.InputTag("goodMuons:goodMuons"),
   tauCollection = cms.InputTag("goodTaus:goodTaus"),
   photonCollection = cms.InputTag("goodPhotons:goodPhotons"),
   vertexCollection = cms.InputTag("goodVertices"),
   metCollection = cms.InputTag("slimmedMETs"),
   jetCollection = cms.InputTag("goodJets:goodJets"),
   htjetCollection = cms.InputTag("goodJets:HTJets"),
   isMC = cms.bool(options.isMC),
   genParticleCollection = cms.InputTag("prunedGenParticles"),
   xsWeight = cms.double(xsWeight_)
)
mypath = mypath * process.eventAnalyzer

#process.Tracer = cms.Service("Tracer")
process.p = cms.Path(mypath)
