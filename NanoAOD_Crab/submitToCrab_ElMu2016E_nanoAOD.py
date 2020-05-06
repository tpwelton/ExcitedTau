from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'ElMuFinalState-inputDoubleMu_94X_Legacy_nanoAOD-v1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = './nanoProd_16_NANO.py'
#config.JobType.numCores = 4
#config.JobType.maxMemoryMB = 2500
#config.JobType.pyCfgParams = ['applyFilter=True', 'doSS=False', 'isMC=False']

config.Data.inputDataset = '/EmbeddingRun2016E/ElMuFinalState-inputDoubleMu_94X_Legacy_miniAOD-v5/USER'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'Automatic'
config.Data.totalUnits = 3052000
#config.Data.unitsPerJob = 10
#config.Data.lumiMask = './Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
#config.Data.allowNonValidInputDataset = True
#config.Data.outputPrimaryDataset = 'Taustar_TauG_L10000_m175_13TeV_pythia8_step1'
config.Data.outLFNDirBase = '/store/user/twelton/ElMuFinalState-inputDoubleMu_94X_Legacy_nanoAOD-v1'
config.Data.outputDatasetTag = 'ElMuFinalState-inputDoubleMu_94X_Legacy_nanoAOD-v1'

config.Site.storageSite = 'T3_US_FNALLPC'
