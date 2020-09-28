f = open("TauTau2018D_files.txt","w+")
for i in range(903):
  f.write("root://cms-xrd-global.cern.ch//store/user/mburkart/taupog/nanoAOD-v2/Embedding2018D_TauTauFinalState_inputDoubleMu102XminiAODv1_13TeV_USER_v1/1/myNanoProdData2018D_NANO_" + str(i) + ".root\n")
