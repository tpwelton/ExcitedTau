import ROOT
import array as a
import CMS_lumi, tdrstyle
import math
import pdb
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
import phiChecker

tdrstyle.setTDRStyle()
ROOT.gStyle.SetLabelSize(0.03,"XYZ")
#ROOT.gStyle.SetMarkerSize(0)
#ROOT.gStyle.SetMarkerSize(5)

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/RA2b13TeVProduction
lumi = 2572.903+4242.292+4025.228+3104.509+7575.579+8650.628 #1/pb
xrd_prefix = "root://cms-xrd-global.cern.ch/"
#xrd_prefix = "root://cmseos.fnal.gov/"
filesList = []
eventWeights = []
fileCategory = []

#filesQCD_Pt600to800 = [xrd_prefix + i.strip() for i in open("QCDBackground_Pt600to800_sdbnd.txt")] 
#filesQCD_Pt800to1000 = [xrd_prefix + i.strip() for i in open("QCDBackground_Pt800to1000_sdbnd.txt")]
##pdb.set_trace()
#eventCount_QCD = {"600to800": 3896412, "800to1000": 3992112}
#filesList.append(filesQCD_Pt600to800);eventWeights.append(186.9*lumi/eventCount_QCD["600to800"]);fileCategory.append("QCD")
#filesList.append(filesQCD_Pt800to1000);eventWeights.append(32.293*lumi/eventCount_QCD["800to1000"]);fileCategory.append("QCD")

filesQCD_Mu15 = [xrd_prefix + i.strip() for i in open("QCDBackground_MuEnriched15_ditau.txt")] 
eventCount_QCD = {"Mu15": 22094081}
xs_QCD = {"Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8": 269900}
filesList.append(filesQCD_Mu15);eventWeights.append(xs_QCD["Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8"]*lumi/eventCount_QCD["Mu15"]);fileCategory.append("QCD")

filesTTG = [xrd_prefix + i.strip() for i in open("TTGBackground_ditau.txt")]
eventCount_TTG = {"ext1": 9877942}
xs_TTG = {"TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8": 3.795}
filesList.append(filesTTG); eventWeights.append(xs_TTG["TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"]*lumi/sum(eventCount_TTG.values())); fileCategory.append("TTG")

filesTT = [xrd_prefix + i.strip() for i in open("TTBackground_ditau.txt")]
eventCount_TT = {"noSC_TuneCUETP8M2T4": 9853428}
xs_TT = {"TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8": 76.7}
filesList.append(filesTT); eventWeights.append(xs_TT["TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8"]*lumi/sum(eventCount_TT.values())); fileCategory.append("TT")

filesWG = [xrd_prefix + i.strip() for i in open("WGBackground_ditau.txt").readlines()]
eventCount_WG = {"ext1": 5059865, "ext2": 10231994, "ext3": 12219986}
xs_WG = {"WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8" : 510.6}
filesList.append(filesWG); eventWeights.append(xs_WG["WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]*lumi/sum(eventCount_WG.values()));fileCategory.append("WG");

filesW = [xrd_prefix + i.strip() for i in open("WJetsBackground_ditau.txt").readlines()]
eventCount_W = {"200ToInf": 5884226}
xs_W = {"WJetsToLNu_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 50.48}
filesList.append(filesW); eventWeights.append(xs_W["WJetsToLNu_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]*lumi/sum(eventCount_W.values()));fileCategory.append("WJets");

filesZZ = [xrd_prefix + i.strip() for i in open("ZZBackground_ditau.txt").readlines()]
eventCount_ZZ = {"2Jets": 1016643}
xs_ZZ = {"ZZTo2L2Nu_2Jets_ZZOnShell_13TeV-amcatnloFXFX-madspin-pythia8": 0.04631}
filesList.append(filesZZ); eventWeights.append(xs_ZZ["ZZTo2L2Nu_2Jets_ZZOnShell_13TeV-amcatnloFXFX-madspin-pythia8"]*lumi/sum(eventCount_ZZ.values()));fileCategory.append("ZZ");

#filesDY = [xrd_prefix + i.strip() for i in open("DYJetsBackground_sdbnd.txt").readlines()]
#eventCount_DY = {"Pt400to650_ext1": 589842, "Pt400to650_ext2": 604038}
#filesList.append(filesDY); eventWeights.append(0.3921*lumi/sum(eventCount_DY.values()));fileCategory.append("DYJets");
filesDY = [xrd_prefix + i.strip() for i in open("DYJets_Zpt200toInf_ditau.txt").readlines()]
eventCount_DY = {"Zpt200toInf": 2903064}
xs_DY = {"DYJetsToLL_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 6.733}
filesList.append(filesDY); eventWeights.append(xs_DY["DYJetsToLL_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]*lumi/sum(eventCount_DY.values()));fileCategory.append("DYJets");

filesZG = [xrd_prefix + i.strip() for i in open("ZGBackground_ditau.txt").readlines()]
eventCount_ZG = {"ext1": 14372682}
xs_ZG = {"ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 123.8}
filesList.append(filesZG);eventWeights.append(xs_ZG["ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]*lumi/sum(eventCount_ZG.values()));fileCategory.append("ZG"); 

filesData = [xrd_prefix + i.strip() for i in open("Data_ditau.txt").readlines()]
filesList.append(filesData);eventWeights.append(1);fileCategory.append("Data")

#filesSignal250 = ["test_1_chan0_allCuts_phiCheck.root"]
#filesList.append(filesSignal250); eventWeights.append(0.0177*lumi/10000)
filesSignal1000 = ["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD_chan0_ditau.root"]
#filesList.append(filesSignal1000); eventWeights.append(4.069*10.**-3*lumi/10000); fileCategory.append("Signal 1000 GeV")

#Make histograms for each category
catNow = ""
h_allTypes = {}
for cat in fileCategory:
  if cat is not catNow:
    h_allTypes[cat] = ROOT.TH1F(cat,cat,100,0,2000)
    h_allTypes[cat].SetMarkerSize(0)
    catNow = cat

#Loop over categories
for ind,files in enumerate(filesList):
  weight = eventWeights[ind]
  cat = fileCategory[ind]
  #Loop over files
  for fileIndiv in files:
    events = ROOT.TFile.Open(fileIndiv)
    inputTree = events.Get("Events")
    if not inputTree: continue
    Events = InputTree(inputTree)
    
    #Loop over events
    for iEvent in range(Events.entries):
      event = Event(Events,iEvent)
      if not (event.channel == 6): continue
#      if not (event.photon_pt > 20): continue
      if not (event.ll_vis_mass > 100): continue
#      if not (phiChecker.phiChecker(event.lep0_vis_phi,event.lep1_vis_phi,event.MET_phi)): continue
      if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_eeBadScFilter): continue
      if deltaR(event.lep0_vis_eta,event.lep0_vis_phi,event.lep1_vis_eta,event.lep1_vis_phi) < 0.4: continue

      #Overlap removal between Gamma samples and Jet samples
      if not (cat.find("Jets") == -1):
        for i in range(len(event.GenPart_pdgId)):
          if event.GenPart_pdgId[i] == 22:
            maxPDGId = 0;
            parentIdx = i;
            motherPDGId = 0;
            while parentIdx != -1:
              motherPDGId = abs(event.GenPart_pdgId[parentIdx])
              maxPDGId = max(maxPDGId,motherPDGId)
              parentIdx = event.GenPart_genPartIdxMother[parentIdx]
            if maxPDGId < 37: continue


      #Remove Z events with weaker restrictions on second muon
      if len(event.Muon_pt) > 1:
        muSum = 0
        for ind in range(len(event.Muon_pt)):
          muSum += (event.Muon_pt[ind] >= 10 and abs(event.Muon_eta[ind]) < 2.4 and event.Muon_mediumId[ind] and event.Muon_pfIsoId[ind]>=2)
        if muSum >= 2: continue 

      h_allTypes[cat].Fill(event.ll_col_mass,weight)
    events.Close()        

h_MCStack = ROOT.THStack("MCStack","")
h_BkgrdSum = ROOT.TH1F("BkgrdSum","BkgrdSum",100,0,2000)
for ind,key in enumerate(h_allTypes.keys()):
  if key == "Data": continue
  if ind+2 >= 10: 
    fillColor = ind+3
  else:
    fillColor = ind+2
  h_allTypes[key].SetFillColor(fillColor)
  h_allTypes[key].SetLineColor(fillColor)
  h_allTypes[key].Scale(20.)
  h_MCStack.Add(h_allTypes[key])
  h_BkgrdSum.Add(h_allTypes[key])


canvasMassStack = ROOT.TCanvas("MassStack","")
stackPad = ROOT.TPad("stackPad","stackPad", 0.05,0.1,0.95,0.95)
stackPad.SetRightMargin(0.04)
stackPad.Draw()
stackPad.cd()
ratioPlot = h_allTypes["Data"].Clone("ratioPlot")
h_allTypes["Data"].SetTitle("; ; Events/20 GeV")
h_allTypes["Data"].GetXaxis().SetTickLength(0)
h_allTypes["Data"].GetXaxis().SetLabelOffset(999)
h_allTypes["Data"].Draw("ex")
h_MCStack.Draw("HISTSAME")
h_allTypes["Data"].Draw("exsame")
ROOT.gPad.BuildLegend()
#ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9,"")
ratioPad = ROOT.TPad("ratioPad","ratioPad",0.05,0.001,0.95,0.2)
ratioPad.SetBottomMargin(0.5)
ratioPad.SetTopMargin(0.05)
ratioPad.SetRightMargin(0.04)
canvasMassStack.cd()
ratioPad.Draw()
ratioPad.cd()
ratioPlot.Divide(h_BkgrdSum)
ratioPlot.SetTitle("; M(#tau#tau); Data/MC") 
#ratioPlot_min.SetTitleOffset(0.1)
ratioPlot.GetYaxis().SetTitleOffset(0.5)
ratioPlot.SetNdivisions(205,"y")
ratioPlot.SetMaximum(2)
ratioPlot.SetMinimum(0)
ratioPlot.SetTitleSize(0.15,"XYZ")
ratioPlot.SetLabelSize(0.12,"XYZ")
ratioPlot.Draw("ex")
CMS_lumi.lumi_sqrtS = "13 TeV"
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(canvasMassStack,0,0)


pdb.set_trace()
save_file = ROOT.TFile("PhiCheck1000_MuTau_TTBkgrdIncl.root","RECREATE")
save_file.cd()


save_file.Write()
save_file.Close()
