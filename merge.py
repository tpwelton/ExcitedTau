#Usage: cmsRun merge.py inputFiles=file:file1.root,file:file2.root outputFile=file:merge_file.root
#Load file names from text file: inputFiles_load=nameOfFile.txt
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing('analysis')
options.register('loginterval', 1000, mytype=VarParsing.varType.int)
options.parseArguments()

process = cms.Process("PickEvent")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = options.loginterval

process.source = cms.Source ("PoolSource",
        fileNames = cms.untracked.vstring(options.inputFiles),
        duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.out = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string(options.outputFile)
)

process.end = cms.EndPath(process.out)
