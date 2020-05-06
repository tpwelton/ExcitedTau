import json

applyTauFilter_ = True
globalTag_ = ''

data = {}
data['people'] = []

data['people'].append({
   'name': 'SingleMuon_2018A',
   'das': '/SingleMuon/Run2018A-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '68383706',
   'nFiles': '765',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'SingleMuon_2018B',
   'das': '/SingleMuon/Run2018B-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '7574181',
   'nFiles': '105',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'SingleMuon_2018C',
   'das': '/SingleMuon/Run2018C-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '47948288',
   'nFiles': '537',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'SingleMuon_2018D',
   'das': '/SingleMuon/Run2018D-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_Prompt_v14',
   'nEvents': '506717754',
   'nFiles': '5533',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'EGamma_2018A',
   'das': '/EGamma/Run2018A-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '82136296',
   'nFiles': '957',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'EGamma_2018B',
   'das': '/EGamma/Run2018B-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '9234833',
   'nFiles': '160',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'EGamma_2018C',
   'das': '/EGamma/Run2018C-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nevents': '65529767',
   'nfiles': '770',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'EGamma_2018D',
   'das': '/EGamma/Run2018D-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_Prompt_v14',
   'nEvents': '738976078',
   'nFiles': '8663',
   'applyTauFilter': applyTauFilter_,
})
#data['people'].append({
#   'name': 'EGamma_2018E',
#   'das': '/EGamma/Run2018E-PromptReco-v1/MINIAOD',
#   'globalTag': '',
#   'nEvents': '112215',
#   'nFiles': '2',
#   'applyTauFilter': applyTauFilter_,
#})
data['people'].append({
   'name': 'JetHT_Run2018A',
   'das': '/JetHT/Run2018A-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '44331925',
   'nFiles': '623',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'JetHT_Run2018B',
   'das': '/JetHT/Run2018B-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '4476872',
   'nFiles': '94',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'JetHT_Run2018C',
   'das': '/JetHT/Run2018C-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '31413719',
   'nFiles': '460',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'JetHT_Run2018D',
   'das': '/JetHT/Run2018D-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_Prompt_v14',
   'nEvents': '358853510',
   'nFiles': '5157',
   'applyTauFilter': applyTauFilter_,
})
#data['people'].append({
#   'name': 'JetHT_Run2018E',
#   'das': '/JetHT/Run2018E-PromptReco-v1/MINIAOD',
#   'globalTag': '',
#   'nevents': '63022',
#   'nfiles': '2',
#   'applyTauFilter': applyTauFilter_,
#})
data['people'].append({
   'name': 'Tau_2018A',
   'das': '/Tau/Run2018A-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '17972951',
   'nFiles': '258',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'Tau_2018B',
   'das': '/Tau/Run2018B-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '2368587',
   'nFiles': '53',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'Tau_2018C',
   'das': '/Tau/Run2018C-PromptReco-v3/MINIAOD',
   'globalTag': '102X_dataRun2_v11',
   'nEvents': '235',
   'nFiles': '235',
   'applyTauFilter': applyTauFilter_,
})
data['people'].append({
   'name': 'Tau_2018D',
   'das': '/Tau/Run2018D-PromptReco-v2/MINIAOD',
   'globalTag': '102X_dataRun2_Prompt_v14',
   'nEvents': '167889795',
   'nFiles': '2372',
   'applyTauFilter': applyTauFilter_,
})
#data['people'].append({
#   'name': 'Tau_2018E',
#   'das': '/Tau/Run2018E-PromptReco-v2/MINIAOD',
#   'globalTag': '',
#   'nEvents': '0',
#   'nFiles': '2',
#   'applyTauFilter': applyTauFilter_,
#})
#
with open('datasetsData_2018.json', 'w') as outfile:
   json.dump(data, outfile)
