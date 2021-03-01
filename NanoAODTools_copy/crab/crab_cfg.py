from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config#, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'Taustar_TauG_L10000_m5000_13TeV_pythia8_2018_puWeight_all'
config.General.transferLogs=True
config.General.workArea = 'crab_projects'
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_script.py','../scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/Taustar_TauG_L10000_m5000_CP5_13TeV_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
config.Data.totalUnits = 6

#config.Data.lumiMask = "JSON/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt"
#config.Data.lumiMask = "JSON/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"
#config.Data.lumiMask = "JSON/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"
config.Data.outLFNDirBase = '/store/user/twelton/TaustarMC'
config.Data.publication = True
config.Data.outputDatasetTag = 'Taustar_TauG_L10000_m5000_13TeV_pythia8_2018_puWeight_all'
config.section_("Site")
config.Site.storageSite = "T3_US_FNALLPC"
#config.Site.storageSite = "T2_DE_DESY"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

