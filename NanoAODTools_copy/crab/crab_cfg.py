from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'WJetsBackground'
config.General.workArea = 'crab_projects'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/WJetsToLNu_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_TuneUp/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.totalUnits = 5947749
#config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.unitsPerJob = 2
#config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/twelton/WJetsBackground' 
config.Data.publication = True
config.Data.outputDatasetTag = 'WJetsBackground'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"
#config.Site.storageSite = "T2_DE_DESY"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

