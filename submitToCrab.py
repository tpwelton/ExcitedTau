import json
import os

infile = 'datasetsBkg_2018.json'
#infile = 'datasetsSig_2015.json'
#infile = 'datasetsEmbedding_2018.json'
#infile = 'datasetsData_2018.json'

with open(infile) as json_file:

   data = json.load(json_file)
   
   for p in data['people']:
      f = open("./crabSubmits/"+p['name']+".py","w+")
      
      f.write("from CRABClient.UserUtilities import config, getUsernameFromSiteDB\n")
      f.write("config = config()\n")
      f.write("\n")
      
      f.write("config.General.requestName = 'ExcitingAnalyzer_"+p['name']+"'\n")
      f.write("config.General.workArea = 'crab_projects'\n")
      f.write("config.General.transferOutputs = True\n")
      f.write("config.General.transferLogs = True\n")
      f.write("\n")
      
      f.write("config.JobType.pluginName = 'Analysis'\n")
      f.write("config.JobType.psetName = './excitingAnalyzer_cfg.py'\n")
      pyCfgParams = []
      pyCfgParams.append('globalTag='+str(p['globalTag']))
      pyCfgParams.append('applyTauFilter='+str(p['applyTauFilter']))
      if 'isMC' in p and p['isMC']==True:
         pyCfgParams.append('isMC=True')
         pyCfgParams.append('xs='+str(eval(p['xs'])))
         pyCfgParams.append('nEvents='+str(eval(p['nEvents'])))
      if 'doSS' in p:
         pyCfgParams.append('doSS='+str(p['doSS']))
      if 'doMuTau' in p:
         pyCfgParams.append('doMuTau=' + str(p['doMuTau']))
      if 'doElTau' in p:
         pyCfgParams.append('doElTau=' + str(p['doElTau']))
      if 'doTauTau' in p:
         pyCfgParams.append('doTauTau=' + str(p['doTauTau']))
      f.write("config.JobType.pyCfgParams = " + str(pyCfgParams) + "\n")
      f.write("\n")

      f.write("config.Data.inputDataset = '"+p['das']+"'\n")
      if 'inputDBS' in p:
         f.write("config.Data.inputDBS = '" + str(p['inputDBS'])+"'\n")
      if 'isMC' in p and p['isMC']==True:
         f.write("config.Data.splitting = 'FileBased'\n")
         f.write("config.Data.unitsPerJob = 1\n")
      else :
         f.write("config.Data.splitting = 'Automatic'\n")
         f.write("config.Data.lumiMask = './Final/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'\n")
      f.write("config.Data.allowNonValidInputDataset = True\n")
      f.write("config.Data.outLFNDirBase = '/store/user/fjensen/ExcitingAnalyzer_v'\n")
      f.write("\n")

      f.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")

      f.close()

      # actually submit jobs or not
      #os.system("crab submit -c " + f.name)
      #os.system("crab submit -c " + f.name + " --dryrun")

