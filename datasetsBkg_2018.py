import json

applyTauFilter_ = True
globalTag_ = '102X_upgrade2018_realistic_v19'
isMC_ = True

data = {}
data['people'] = []

data['people'].append({
   'name': 'DYJetsToLL',
   'das': '/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '100194597',
   'nFiles': '1254',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '6025.2',
})
data['people'].append({
   'name': 'DYJetsToLL_Zpt150',
   'das': '/DYJetsToLL_M-50_Zpt-150toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '2135787',
   'nFiles': '60',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '27.150108', ###derived from inclusive sample
})
data['people'].append({
   'name': 'TTGJets',
   'das': '/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4691915',
   'nFiles': '133',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '3.697',
})
data['people'].append({
   'name': 'TTGamma_SingleLeptFromT',
   'das': '/TTGamma_SingleLeptFromT_TuneCP5_13TeV_madgraph_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4840000',
   'nFiles': '140',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '0.704',
})
data['people'].append({
   'name': 'TTGamma_SingleLeptFromTbar',
   'das': '/TTGamma_SingleLeptFromTbar_TuneCP5_13TeV_madgraph_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4945000',
   'nFiles': '141',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '0.704',
})
data['people'].append({
   'name': 'TTGamma_DiLept',
   'das': '/TTGamma_Dilept_TuneCP5_13TeV_madgraph_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4940000',
   'nFiles': '151',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '0.5804',
})
data['people'].append({
   'name': 'TTGamma_Hadronic',
   'das': '/TTGamma_Hadronic_TuneCP5_13TeV_madgraph_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4940000',
   'nFiles': '143',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '1.7086', #3.697-0.704-0.704-0.5804
})
data['people'].append({
   'name': 'TTTo2L2Nu',
   'das': '/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '64310000',
   'nFiles': '968',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '88.29',
})
data['people'].append({
   'name': 'TTToSemiLeptonic',
   'das': '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '101550000',
   'nFiles': '1523',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '365.34',
})
data['people'].append({
   'name': 'TTToHadronic',
   'das': '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '133808000',
   'nFiles': '3313',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '377.96',
})
data['people'].append({
   'name': 'TTToHadronic_ext',
   'das': '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext2-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '199524000',
   'nFiles': '3762',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '377.96',
})
data['people'].append({
   'name': 'ST_tW_antitop',
   'das': '/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '5823328',
   'nFiles': '148',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '19.4674',
})
data['people'].append({
   'name': 'ST_tW_top',
   'das': '/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v3/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '7636887',
   'nFiles': '184',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '19.4674',
})
data['people'].append({
   'name': 'ZGToLLG',
   'das': '/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '13946364',
   'nFiles': '266',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '16.837021', #(32.3/0.2)*(0.033632+0.033662+0.03696)
})
data['people'].append({
   'name': 'WGToLNuG',
   'das': '/WGToLNuG_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '6108186',
   'nFiles': '117',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '405.271',###
})
data['people'].append({
   'name': 'WJetsToLNu',
   'das': '/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '71026861',
   'nFiles': '990',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '61334.9',
})
data['people'].append({
   'name': 'GJets_HT-40To100',
   'das': '/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '9371355',
   'nFiles': '130',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '9226.0',###FIXME
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_HT-100To200',
   'das': '/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-4cores5k_102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '9798176',
   'nFiles': '163',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '9226.0',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_HT-200To400',
   'das': '/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '19062809',
   'nFiles': '312',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '2300.0',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_HT-400To600',
   'das': '/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4655985',
   'nFiles': '124',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '277.4',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_HT-600ToInf',
   'das': '/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15_ext1-v2/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '4981121',
   'nFiles': '165',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '93.38',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_DR-0p4_HT-100To200',
   'das': '/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '15424758',
   'nFiles': '245',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '5000.0',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_DR-0p4_HT-200To400',
   'das': '/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '49457520',
   'nFiles': '928',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '1079.0',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_DR-0p4_HT-400To600',
   'das': '/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '13717985',
   'nFiles': '431',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '125.9',
   'doSS': 'True'
})
data['people'].append({
   'name': 'GJets_DR-0p4_HT-600ToInf',
   'das': '/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '12456593',
   'nFiles': '390',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '43.36',
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT50to100',
   'das': '/QCD_HT50to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '38754230',
   'nFiles': '547',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '19380000.', #FIXME
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT100to200',
   'das': '/QCD_HT100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '93972378',
   'nFiles': '1296',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '19380000.', ###
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT200to300',
   'das': '/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '54289442',
   'nFiles': '780',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '1717000.',
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT300to500',
   'das': '/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '54661579',
   'nFiles': '829',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '351300.',
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT500to700',
   'das': '/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '55152960',
   'nFiles': '1355',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '31630.',
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT700to1000',
   'das': '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '48158738',
   'nFiles': '1257',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '6802.',
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT1000to1500',
   'das': '/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '15466225',
   'nFiles': '420',
   'applyTauFilter': applyTauFilter_,
   'xs': '1206.',
   'isMC': isMC_,
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT1500to2000',
   'das': '/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '10955087',
   'nFiles': '302',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '120.4',
   'doSS': 'True'
})
data['people'].append({
   'name': 'QCD_HT2000toInf',
   'das': '/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM',
   'globalTag': globalTag_,
   'nEvents': '5475677',
   'nFiles': '166',
   'applyTauFilter': applyTauFilter_,
   'isMC': isMC_,
   'xs': '25.24',
   'doSS': 'True'
})

with open('datasetsBkg_2018.json', 'w') as outfile:
   json.dump(data, outfile)
