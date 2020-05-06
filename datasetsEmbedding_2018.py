import json

applyTauFilter_ = True
globalTag_ = ''
inputDBS_ = 'phys03'

data = {}
data['people'] = []

data['people'].append({
   'name': 'TauTau_Run2018A',
   'das': '/EmbeddingRun2018A/TauTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '10371109',
   'nFiles': '21606',
   'applyTauFilter': applyTauFilter_,
   'doMuTau': False,
   'doElTau': False,
   'doTauTau': True,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'TauTau_Run2018B',
   'das': '/EmbeddingRun2018B/TauTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '5227841',
   'nFiles': '9717',
   'applyTauFilter': applyTauFilter_,
   'doMuTau': False,
   'doElTau': False,
   'doTauTau': True,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'TauTau_Run2018C',
   'das': '/EmbeddingRun2018C/TauTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '4821754',
   'nFiles': '8968',
   'applyTauFilter': applyTauFilter_,
   'doMuTau': False,
   'doElTau': False,
   'doTauTau': True,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'TauTau_Run2018D',
   'das': '/EmbeddingRun2018D/TauTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '22561187',
   'nFiles': '56451',
   'applyTauFilter': applyTauFilter_,
   'doMuTau': False,
   'doElTau': False,
   'doTauTau': True,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'ElTau_Run2018A',
   'das': '/EmbeddingRun2018A/ElTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '11735088',
   'nFiles': '21606',
   'applyTauFilter': applyTauFilter_,
   'doElTau': True,
   'doMuTau': False,
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'ElTau_Run2018B',
   'das': '/EmbeddingRun2018B/ElTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '5893097',
   'nFiles': '9717',
   'applyTauFilter': applyTauFilter_,
   'doElTau': True,
   'doMuTau': False,
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'ElTau_Run2018C',
   'das': '/EmbeddingRun2018C/ElTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '5422423',
   'nFiles': '8968',
   'applyTauFilter': applyTauFilter_,
   'doElTau': True,
   'doMuTau': False,
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'ElTau_Run2018D',
   'das': '/EmbeddingRun2018D/ElTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '25383778',
   'nFiles': '56450',
   'applyTauFilter': applyTauFilter_,
   'doElTau': True,
   'doMuTau': False,
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'MuTau_Run2018A',
   'das': '/EmbeddingRun2018A/MuTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '11735808',
   'nFiles': '21606',
   'applyTauFilter': applyTauFilter_,
   'doElTau': False,
   'doMuTau': True,  
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'MuTau_Run2018B',
   'das': '/EmbeddingRun2018B/MuTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nevents': '5892212',
   'nfiles': '9717',
   'applyTauFilter': applyTauFilter_,
   'doElTau': False,
   'doMuTau': True,
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'MuTau_Run2018C',
   'das': '/EmbeddingRun2018C/MuTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '5420887',
   'nFiles': '8967',
   'applyTauFilter': applyTauFilter_,
   'doElTau': False,
   'doMuTau': True,
   'doTauTau': False,
   'inputDBS': inputDBS_
})
data['people'].append({
   'name': 'MuTau_Run2018D',
   'das': '/EmbeddingRun2018D/MuTauFinalState-inputDoubleMu_102X_miniAOD-v1/USER',
   'globalTag': '',
   'nEvents': '25379684',
   'nFiles': '56451',
   'applyTauFilter': applyTauFilter_,
   'doElTau': False,
   'doMuTau': True,
   'doTauTau': False,
   'inputDBS': inputDBS_
})

with open('datasetsEmbedding_2018.json', 'w') as outfile:
   json.dump(data, outfile)
