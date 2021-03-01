import os
ind = 0
f = open("cmdEmbedding.txt","w")
number = ["004617",
          "004729",
          "004824",
          "004918",
          "005013",
          "005107",
          "005202",
          "005314",
          "005410",
          "005504",
          "005559",
          "005704",
          "005810",
          "005908",
          "010002",
          "010112",
          "010211",
          "010305",
          "010400",
          "010513",
          "010620",
          "010715",
          "010809",
          "010915",
          "011021",
          "011120",
          "011214",
          "011328",
          "011427",
          "011521",
          "011616",
          "011732",
          "011827",
          "011923",
          "012031",
          "012130",
          "012224",
          "012320",
          "012435",
          "012532",
          "012626",
          "012722",
          "012816"]
for year in ["2016","2017","2018"]:
  for alpha in ["A","B","C","D","E","F","G","H"]:
    if year == "2016":
      if alpha < "B": continue
    if year == "2017":
      if alpha < "B" or alpha > "F": continue
    if year == "2018":
      if alpha > "D": break
    for final in ["ElMu","TauTau","ElTau","MuTau"]:
      if year == "2016" and final != "MuTau": continue
      name = "EmbeddingRun" + year + alpha + "_" + final 
      name += "_puWeight_all"
      nameSplit = name.split("_")
      cmd = "eosls /store/user/twelton/EmbeddedSamples_NanoAODv5/"+nameSplit[0]+"/"+name+"/210216_"+number[ind]+"/0000/ >> Embedding" + year
      for subname in nameSplit[2:]:
        cmd = "_".join([cmd,subname])
      cmd += ".txt\n"
      f.write(cmd)
      ind += 1
f.close()

