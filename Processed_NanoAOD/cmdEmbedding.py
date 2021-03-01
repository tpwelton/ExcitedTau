f1 = open("cmdEmbedding.txt","r")
f2 = open("Embedding2017_puWeight_all.txt","r")
f3 = open("Embedding2018_puWeight_all.txt","r")

fout1 = open("test2017.txt","w")
fout2 = open("test2018.txt","w")
lines1 = f1.readlines()
ind = 6
for line in f2.readlines():
  if not(line.find("log") == -1):
    header = lines1[ind+1].split(" ")[1]
    ind += 1
  fout1.write(header + line)
fout1.close()
for line in f3.readlines():
  if not(line.find("log") == -1):
    header = lines1[ind+1].split(" ")[1]
    ind += 1
  fout2.write(header + line)
fout2.close()
