# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: nanoProd_16 -s NANO --data --eventcontent NANOAOD --datatier NANOAOD --no_exec --conditions 102X_dataRun2_nanoAOD_2016_v1 --era Run2_2016,run2_nanoAOD_94X2016 --filein file:test_16.root --fileout file:test_nano_16.root
import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('NANO',eras.Run2_2016,eras.run2_nanoAOD_94X2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#      'file:merged_miniaod.root'),
      "root://cms-xrd-global.cern.ch//store/user/sbrommer/embedding_disk_update/embedding_16_legacy_miniaod/TauTau_data_legacy_2016_CMSSW9414/TauEmbedding_TauTau_data_legacy_2016_CMSSW9414_Run2016B-v2/72/merged_miniaod_1371.root"),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('nanoProd_16 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

#Deep Tau
updatedTauName = "slimmedTausNewID" #name of pat::Tau collection with new tau-Ids
import RecoTauTag.RecoTau.tools.runTauIdMVA as tauIdConfig
tauIdEmbedder = tauIdConfig.TauIDEmbedder(process, cms, debug = False,
                    updatedTauName = updatedTauName,
                    toKeep = ["deepTau2017v2p1"
#                   toKeep = [ "2017v2", "dR0p32017v2", "newDM2017v2", #classic MVAIso tau-Ids
#                              "deepTau2017v1", #deepTau Tau-Ids
#                              "DPFTau_2016_v0", #D[eep]PF[low] Tau-Id
                               ])
tauIdEmbedder.runTauID()

# Output definition

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:merged_nanoaod.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)

# Additional output definition
process.unpackedPatTrigger.triggerResults = cms.InputTag('TriggerResults::SIMembedding')

process.NANOAODoutput.outputCommands.append("keep edmTriggerResults_*_*_SIMembedding")  # Trigger information
process.NANOAODoutput.outputCommands.append("keep edmTriggerResults_*_*_MERGE")  # MET filter flags
#process.NANOAODoutput.outputCommands.append("keep *_"+updatedTauName+"_*_*")

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '102X_dataRun2_nanoAOD_2016_v1', '')

# Path and EndPath definitions
#process.nanoAOD_step = cms.Path(process.nanoSequence)
process.nanoAOD_step = cms.Path(process.rerunMvaIsolationSequence * getattr(process,updatedTauName) * process.genParticleSequence + process.nanoSequenceCommon + process.nanoSequenceOnlyFullSim + process.muonMC + process.electronMC + process.photonMC + process.tauMC + process.globalTablesMC + process.btagWeightTable + process.genWeightsTable + process.genParticleTables)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeData 

#call to customisation function nanoAOD_customizeData imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeData(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
