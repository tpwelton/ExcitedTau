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
lumi = 30171.139#2572.903+4242.292+4025.228+3104.509+7575.579+8650.628 #1/pb
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

filesQCD_Mu15 = [xrd_prefix + i.strip() for i in open("QCDBackground_MuEnriched15_sdbnd.txt")] 
eventCount_QCD = {"Mu15": 22094081}
xs_QCD = {"Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8": 269900}
filesList.append(filesQCD_Mu15);eventWeights.append(xs_QCD["Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8"]*lumi/eventCount_QCD["Mu15"]);fileCategory.append("QCD")

filesTTG = [xrd_prefix + i.strip() for i in open("TTGBackground_sdbnd.txt")]
eventCount_TTG = {"ext1": 9877942}
xs_TTG = {"TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8": 3.795}
filesList.append(filesTTG); eventWeights.append(xs_TTG["TTGJets_TuneCUETP8M1_13TeV-amcatnloFXFX-madspin-pythia8"]*lumi/sum(eventCount_TTG.values())); fileCategory.append("TTG")

filesTT = [xrd_prefix + i.strip() for i in open("TTBackground_sdbnd.txt")]
eventCount_TT = {"noSC_TuneCUETP8M2T4": 9853428}
xs_TT = {"TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8": 76.7}
filesList.append(filesTT); eventWeights.append(xs_TT["TTTo2L2Nu_noSC_TuneCUETP8M2T4_13TeV-powheg-pythia8"]*lumi/sum(eventCount_TT.values())); fileCategory.append("TT")

filesWG = [xrd_prefix + i.strip() for i in open("WGBackground_sdbnd.txt").readlines()]
eventCount_WG = {"ext1": 5059865, "ext2": 10231994, "ext3": 12219986}
xs_WG = {"WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8" : 510.6}
filesList.append(filesWG); eventWeights.append(xs_WG["WGToLNuG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]*lumi/sum(eventCount_WG.values()));fileCategory.append("WG");

filesW = [xrd_prefix + i.strip() for i in open("WJetsBackground_sdbnd.txt").readlines()]
eventCount_W = {"200ToInf": 5884226}
xs_W = {"WJetsToLNu_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 50.48}
filesList.append(filesW); eventWeights.append(xs_W["WJetsToLNu_Wpt-200toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]*lumi/sum(eventCount_W.values()));fileCategory.append("WJets");

filesZZ = [xrd_prefix + i.strip() for i in open("ZZBackground_sdbnd.txt").readlines()]
eventCount_ZZ = {"2Jets": 1016643}
xs_ZZ = {"ZZTo2L2Nu_2Jets_ZZOnShell_13TeV-amcatnloFXFX-madspin-pythia8": 0.04631}
filesList.append(filesZZ); eventWeights.append(xs_ZZ["ZZTo2L2Nu_2Jets_ZZOnShell_13TeV-amcatnloFXFX-madspin-pythia8"]*lumi/sum(eventCount_ZZ.values()));fileCategory.append("ZZ");

#filesDY = [xrd_prefix + i.strip() for i in open("DYJetsBackground_sdbnd.txt").readlines()]
#eventCount_DY = {"Pt400to650_ext1": 589842, "Pt400to650_ext2": 604038}
#filesList.append(filesDY); eventWeights.append(0.3921*lumi/sum(eventCount_DY.values()));fileCategory.append("DYJets");
filesDY = [xrd_prefix + i.strip() for i in open("DYJets_Zpt200toInf_sdbnd.txt").readlines()]
eventCount_DY = {"Zpt200toInf": 2903064}
xs_DY = {"DYJetsToLL_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": 6.733}
filesList.append(filesDY); eventWeights.append(xs_DY["DYJetsToLL_Zpt-200toInf_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]*lumi/sum(eventCount_DY.values()));fileCategory.append("DYJets");

filesZG = [xrd_prefix + i.strip() for i in open("ZGBackground_sdbnd.txt").readlines()]
eventCount_ZG = {"ext1": 14372682}
xs_ZG = {"ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": 123.8}
filesList.append(filesZG);eventWeights.append(xs_ZG["ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"]*lumi/sum(eventCount_ZG.values()));fileCategory.append("ZG"); 

filesData = [xrd_prefix + i.strip() for i in open("Data_sdbnd.txt").readlines()]
filesList.append(filesData);eventWeights.append(1.);fileCategory.append("Data")

#filesSignal250 = ["test_1_chan0_allCuts_phiCheck.root"]
#filesList.append(filesSignal250); eventWeights.append(0.0177*lumi/10000)
filesSignal1000 = ["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD_chan0_sdbnd.root"]
#filesList.append(filesSignal1000); eventWeights.append(4.069*10.**-3*lumi/10000); fileCategory.append("Signal 1000 GeV")

h_missingPtBetween_Reco = ROOT.TH1F("missingPtBetween_Reco","",2,-.5,1.5)
h_missingPtBetween_Gen = ROOT.TH1F("missingPtBetween_Gen","",2,-.5,1.5)
h_missingPtBetween_Nu = ROOT.TH1F("missingPtBetween_Nu","",2,-.5,1.5)
h_genVisPVsRecoP0 = ROOT.TH1F("genVisPVsRecoP0","",100,-1000,1000)
h_genColPVsRecoP0 = ROOT.TH1F("genColPVsRecoP0","",100,-1000,1000)
h_genVisPVsRecoP1 = ROOT.TH1F("genVisPVsRecoP1","",100,-1000,1000)
h_genColPVsRecoP1 = ROOT.TH1F("genColPVsRecoP1","",100,-1000,1000)
h_METvsGenMET = ROOT.TH1F("METvsGenMET","",200,0,4)
h_METvsNuSum = ROOT.TH1F("METvsNuSum","",200,0,4)
h_genMETvsNuSum = ROOT.TH1F("genMETvsNuSum","",200,0,4)
h_minMassVsMaxMass = ROOT.TH2F("minMassVsMaxMass","",100,0,2000,100,0,2000)
h_minMassVsMaxMass_phiCheck = ROOT.TH2F("minMassVsMaxMass_phiCheck","",100,0,2000,100,0,2000)
h_deltaR0_nu = ROOT.TH1F("deltaR0","",100,0,1)
h_deltaR1_nu = ROOT.TH1F("deltaR1","",100,0,1)
h_deltaR0_truth = ROOT.TH1F("deltaR0_truth","",100,0,1)
h_deltaR1_truth = ROOT.TH1F("deltaR1_truth","",100,0,1)
h_minBkgrdSum = ROOT.TH1F("minBkgrdSum","minBkgrdSum",100,0,2000)
h_maxBkgrdSum = ROOT.TH1F("maxBkgrdSum","maxBkgrdSum",100,0,2000)

catNow = ""
h_allTypes_min = {}
h_allTypes_max = {}
h_allTypes = {}
for cat in fileCategory:
  if cat is not catNow:
    h_allTypes_min[cat] = ROOT.TH1F(cat+"min",cat,100,0,2000)
    h_allTypes_min[cat].SetMarkerSize(0)
    h_allTypes_max[cat] = ROOT.TH1F(cat+"max",cat,100,0,2000)
    h_allTypes_max[cat].SetMarkerSize(0)
    h_allTypes[cat] = ROOT.TH1F(cat,cat,100,0,2000)
    h_allTypes[cat].SetMarkerSize(0)
    catNow = cat





minMass = []
maxMass = []
minMass_phiCheck = []
maxMass_phiCheck = []
for ind,files in enumerate(filesList):
  weight = eventWeights[ind]
  cat = fileCategory[ind]
  for fileIndiv in files:
    events = ROOT.TFile.Open(fileIndiv)
#    pdb.set_trace()
    inputTree = events.Get("Events")
    if not inputTree: continue
    Events = InputTree(inputTree)
    
    for iEvent in range(Events.entries):
      event = Event(Events,iEvent)
      if not (event.channel == 6): continue
      if not (event.photon_pt > 20): continue
      if not (event.ll_vis_mass > 100): continue
      if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_eeBadScFilter): continue
      if deltaR(event.lep0_vis_eta,event.lep0_vis_phi,event.lep1_vis_eta,event.lep1_vis_phi) < 0.4: continue

      #Overlap removal between Gamma samples and Jet samples
      if not (cat.find("Jets") == -1):
        for i in range(len(event.GenPart_pdgId)):
          if event.GenPart_pdgId[i] == 22:
            #Only remove events where the photon would be picked up
            if event.GenPart_eta[i] <= 2.6 and event.GenPart_pt[i] >= 15:
              maxPDGId = 0;
              parentIdx = i;
              motherPDGId = 0;
              while parentIdx != -1:
                motherPDGId = abs(event.GenPart_pdgId[parentIdx])
                maxPDGId = max(maxPDGId,motherPDGId)
                parentIdx = event.GenPart_genPartIdxMother[parentIdx]
              if maxPDGId < 37: continue

#      pdb.set_trace()
#      if not (cat.find("Signal") == -1):# and event.missingPtBetween_Reco:
#        h_genVisPVsRecoP0.Fill(event.genVisPVsRecoP0)
#        h_genColPVsRecoP0.Fill(event.genColPVsRecoP0)
#        h_genVisPVsRecoP1.Fill(event.genVisPVsRecoP1)
#        h_genColPVsRecoP1.Fill(event.genColPVsRecoP1)
#        h_deltaR0_nu.Fill(event.deltaR0_nu)
#        h_deltaR0_nu.Fill(event.deltaR1_nu)
#        h_deltaR0_truth.Fill(event.deltaR0_truth)
#        h_deltaR1_truth.Fill(event.deltaR1_truth)

      #Remove Z events with weaker restrictions on second muon
      if len(event.Muon_pt) > 1:
        muSum = 0
        for ind in range(len(event.Muon_pt)):
          muSum += (event.Muon_pt[ind] >= 10 and abs(event.Muon_eta[ind]) < 2.4 and event.Muon_mediumId[ind] and event.Muon_pfIsoId[ind]>=2)
        if muSum >= 2: continue 

      #Assign min and max mass appropriately
      if event.gamlep0_col_mass < event.gamlep1_col_mass:
        minMass.append(event.gamlep0_col_mass)
        maxMass.append(event.gamlep1_col_mass)
        h_minMassVsMaxMass.Fill(event.gamlep0_col_mass,event.gamlep1_col_mass,weight)
        if phiChecker.phiChecker(event.lep0_vis_phi,event.lep1_vis_phi,event.MET_phi):
          minMass_phiCheck.append(event.gamlep0_col_mass)
          maxMass_phiCheck.append(event.gamlep1_col_mass)
          h_minMassVsMaxMass_phiCheck.Fill(event.gamlep0_col_mass,event.gamlep1_col_mass,weight)
          h_allTypes_min[cat].Fill(event.gamlep0_col_mass,weight)
          h_allTypes_max[cat].Fill(event.gamlep1_col_mass,weight)
      else:
        minMass.append(event.gamlep1_col_mass)
        maxMass.append(event.gamlep0_col_mass)
        h_minMassVsMaxMass.Fill(event.gamlep1_col_mass,event.gamlep0_col_mass,weight)
        if phiChecker.phiChecker(event.lep0_vis_phi,event.lep1_vis_phi,event.MET_phi):
          minMass_phiCheck.append(event.gamlep1_col_mass)
          maxMass_phiCheck.append(event.gamlep0_col_mass)
          h_minMassVsMaxMass_phiCheck.Fill(event.gamlep1_col_mass,event.gamlep0_col_mass,weight)
          h_allTypes_min[cat].Fill(event.gamlep1_col_mass,weight)
          h_allTypes_max[cat].Fill(event.gamlep0_col_mass,weight)
      h_allTypes[cat].Fill(event.ll_col_mass,weight)
    events.Close()        

h_maxStack = ROOT.THStack("maxStack","")
h_minStack = ROOT.THStack("minStack","")
h_MCStack = ROOT.THStack("MCStack","")
h_BkgrdSum = ROOT.TH1F("BkgrdSum","BkgrdSum",100,0,2000)
for ind,key in enumerate(h_allTypes_max.keys()):
  if key == "Data": continue
  if ind+2 >= 10: 
    fillColor = ind+3
  else:
    fillColor = ind+2
  h_allTypes_max[key].SetFillColor(fillColor)
  h_allTypes_max[key].SetLineColor(fillColor)
  h_allTypes_max[key].Scale(3.)
  h_maxStack.Add(h_allTypes_max[key])
  h_maxBkgrdSum.Add(h_allTypes_max[key])
  h_allTypes_min[key].SetLineColor(fillColor)
  h_allTypes_min[key].SetFillColor(fillColor)
  h_allTypes_min[key].Scale(3.)
  h_minStack.Add(h_allTypes_min[key])
  h_minBkgrdSum.Add(h_allTypes_min[key])
  h_allTypes[key].SetFillColor(fillColor)
  h_allTypes[key].SetLineColor(fillColor)
  h_allTypes[key].Scale(3.)
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
canvasMinStack = ROOT.TCanvas("MinStack","")
stackPad_min = ROOT.TPad("stackPad_min","stackPad_min", 0.05,0.1,0.95,0.95)
stackPad_min.SetRightMargin(0.04)
stackPad_min.Draw()
stackPad_min.cd()
ratioPlot_min = h_allTypes_min["Data"].Clone("ratioPlot_min")
h_allTypes_min["Data"].SetTitle("; ; Events/20 GeV")
h_allTypes_min["Data"].GetXaxis().SetTickLength(0)
h_allTypes_min["Data"].GetXaxis().SetLabelOffset(999)
h_allTypes_min["Data"].Draw("ex")
h_minStack.Draw("HISTSAME")
h_allTypes_min["Data"].Draw("exsame")
#h_minStack.GetHistogram().GetXaxis().SetTickLength(0)
#h_minStack.GetHistogram().GetXaxis().SetLabelOffset(999)
ROOT.gPad.BuildLegend()
#ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9,"")
ratioPad_min = ROOT.TPad("ratioPad_min","ratioPad_min",0.05,0.001,0.95,0.2)
ratioPad_min.SetBottomMargin(0.5)
ratioPad_min.SetTopMargin(0.05)
ratioPad_min.SetRightMargin(0.04)
canvasMinStack.cd()
ratioPad_min.Draw()
ratioPad_min.cd()
ratioPlot_min.Divide(h_minBkgrdSum)
ratioPlot_min.SetTitle("; M_{min}(#tau#gamma); Data/MC") 
#ratioPlot_min.SetTitleOffset(0.1)
ratioPlot_min.GetYaxis().SetTitleOffset(0.5)
ratioPlot_min.SetNdivisions(205,"y")
ratioPlot_min.SetMaximum(2.)
ratioPlot_min.SetMinimum(0)
ratioPlot_min.SetTitleSize(0.15,"XYZ")
ratioPlot_min.SetLabelSize(0.12,"XYZ")
ratioPlot_min.Draw("ex")
CMS_lumi.lumi_sqrtS = "13 TeV"
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(canvasMinStack,0,0)

canvasMaxStack = ROOT.TCanvas("MaxStack","")
canvasMaxStack.SetBottomMargin(0.)
stackPad = ROOT.TPad("stackPad","stackPad", 0.05,0.1,0.95,0.95)
stackPad.SetRightMargin(0.04)
stackPad.Draw()
stackPad.cd()
ratioPlot_max = h_allTypes_max["Data"].Clone("ratioPlot_max")
h_allTypes_max["Data"].SetTitle(";; Events/20 GeV")
h_allTypes_max["Data"].GetXaxis().SetTickLength(0)
h_allTypes_max["Data"].GetXaxis().SetLabelOffset(999)
h_allTypes_max["Data"].Draw("ex")
h_maxStack.Draw("HISTSAME")
h_allTypes_max["Data"].Draw("exsame")
#h_maxStack.GetHistogram().GetXaxis().SetTickLength(0)
#h_maxStack.GetHistogram().GetXaxis().SetLabelOffset(999)
ROOT.gPad.BuildLegend()
#ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9,"")
ratioPad_max = ROOT.TPad("ratioPad_max","ratioPad_max",0.05,0.001,0.95,0.2)
ratioPad_max.SetBottomMargin(0.5)
ratioPad_max.SetTopMargin(0.05)
ratioPad_max.SetRightMargin(0.04)
canvasMaxStack.cd()
ratioPad_max.Draw()
ratioPad_max.cd()
ratioPlot_max.Divide(h_maxBkgrdSum)
ratioPlot_max.SetTitle("; M_{max}(#tau#gamma); Data/MC")
#ratioPlot_max.SetTitleOffset(0.1)
ratioPlot_max.GetYaxis().SetTitleOffset(0.5)
ratioPlot_max.SetNdivisions(205,"y")
ratioPlot_max.SetMaximum(2.)
ratioPlot_max.SetMinimum(0)
ratioPlot_max.SetTitleSize(0.15,"XYZ")
ratioPlot_max.SetLabelSize(0.12,"XYZ")
ratioPlot_max.Draw("ex")
CMS_lumi.CMS_lumi(canvasMaxStack,0,0)
pdb.set_trace()
#
#h_minMassVsMaxMass.Draw()
canvasDeltaR_truth = ROOT.TCanvas("DeltaR_truth","")
h_deltaR0_truth.SetTitle("; #DeltaR; Events/0.01")
h_deltaR0_truth.SetMarkerSize(0)
h_deltaR0_truth.SetLineColor(ROOT.kBlue)
h_deltaR0_truth.Draw()
h_deltaR1_truth.SetMarkerSize(0)
h_deltaR1_truth.SetLineColor(ROOT.kBlack)
h_deltaR1_truth.Draw("same")

canvasDeltaR_nu = ROOT.TCanvas("DeltaR_nu","")
h_deltaR0_nu.SetTitle("; #DeltaR(#tau,#nu); Events/0.01")
h_deltaR0_nu.SetMarkerSize(0)
h_deltaR0_nu.SetLineColor(ROOT.kBlack)
h_deltaR0_nu.Draw()
#h_deltaR1_nu.SetMarkerSize(0)
#h_deltaR1_nu.SetLineColor(ROOT.kGreen)
#h_deltaR1_nu.Draw("same")

canvasMomentum_truth = ROOT.TCanvas("Momentum_truth","")
h_genColPVsRecoP1.SetTitle("; |p|_{truth} - |p|_{reco};Events/20 GeV")
h_genColPVsRecoP1.SetLineColor(ROOT.kGreen)
h_genColPVsRecoP1.SetMarkerSize(0)
h_genColPVsRecoP1.Draw()
h_genVisPVsRecoP0.SetMarkerSize(0)
h_genVisPVsRecoP0.SetLineColor(ROOT.kBlue)
h_genVisPVsRecoP0.Draw("same")
h_genColPVsRecoP0.SetMarkerSize(0)
h_genColPVsRecoP0.SetLineColor(ROOT.kBlack)
h_genColPVsRecoP0.Draw("same")
h_genVisPVsRecoP1.SetMarkerSize(0)
h_genVisPVsRecoP1.SetLineColor(ROOT.kRed)
h_genVisPVsRecoP1.Draw("same")

canvasMinMaxColor = ROOT.TCanvas("MinMaxColor","")
#h_minMassVsMaxMass_phiCheck.SetMarkerColor(ROOT.kRed)
h_minMassVsMaxMass_phiCheck.SetTitle("; M_{min}(#tau#gamma); M_{max}(#tau#gamma)")
h_minMassVsMaxMass_phiCheck.Draw("colz")
#minMassVsMaxMass = ROOT.TGraph(len(minMass),a.array('d',minMass),a.array('d',maxMass))
#minMassVsMaxMass_phiCheck = ROOT.TGraph(len(minMass_phiCheck),a.array('d',minMass_phiCheck),a.array('d',maxMass_phiCheck))
#minMassVsMaxMass_mg = ROOT.TMultiGraph()
#minMassVsMaxMass_mg.Add(minMassVsMaxMass)
#minMassVsMaxMass_mg.Add(minMassVsMaxMass_phiCheck)
#
#minMassVsMaxMass.SetMarkerColor(ROOT.kBlack)
#minMassVsMaxMass_phiCheck.SetMarkerColor(ROOT.kRed)
#minMassVsMaxMass_mg.GetXaxis().SetRangeUser(0,1000)
#ROOT.gPad.Clear()
#minMassVsMaxMass_mg.Draw("AP")
pdb.set_trace()

canvasMETBetween = ROOT.TCanvas('METBetween','')
#
h_missingPtBetween_Nu.SetTitle("; Is MET between the Taus?; Number of Events")
h_missingPtBetween_Nu.SetLineColor(ROOT.kRed)
h_missingPtBetween_Nu.SetMarkerSize(0)
h_missingPtBetween_Nu.Draw()
h_missingPtBetween_Gen.SetTitle("; Is MET between the Taus?; Number of Events")
h_missingPtBetween_Gen.SetLineColor(ROOT.kBlack)
h_missingPtBetween_Gen.SetMarkerSize(0)
h_missingPtBetween_Gen.Draw("same")
h_missingPtBetween_Reco.SetTitle("; Is MET between the Taus?; Number of Events")
h_missingPtBetween_Reco.SetLineColor(ROOT.kBlue)
h_missingPtBetween_Reco.SetMarkerSize(0)
h_missingPtBetween_Reco.Draw("same")
#
canvasMETDeltaR = ROOT.TCanvas('DeltaR','')

h_genMETvsNuSum.SetTitle(";#DeltaR;Events/0.02")
h_genMETvsNuSum.SetLineColor(ROOT.kRed)
h_genMETvsNuSum.SetMarkerSize(0)
ROOT.gPad.SetLogy()
h_genMETvsNuSum.Draw()
h_METvsNuSum.SetTitle(";#DeltaR;Events/0.02")
h_METvsNuSum.SetLineColor(ROOT.kBlack)
h_METvsNuSum.SetMarkerSize(0)
h_METvsNuSum.Draw("same")
h_METvsGenMET.SetTitle(";#DeltaR;Events/0.02")
h_METvsGenMET.SetLineColor(ROOT.kBlue)
h_METvsGenMET.SetMarkerSize(0)
h_METvsGenMET.Draw("same")

CMS_lumi.lumi_sqrtS = "13TeV"
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(canvasMETBetween,0,0)
CMS_lumi.CMS_lumi(canvasMETDeltaR,0,0)
CMS_lumi.CMS_lumi(canvasDeltaR_truth,0,0)
CMS_lumi.CMS_lumi(canvasDeltaR_nu,0,0)
CMS_lumi.CMS_lumi(canvasMomentum_truth,0,0)
CMS_lumi.CMS_lumi(canvasMinMaxColor,0,0)
#
#pdb.set_trace() 
#
canvasMETDeltaR.Update()
canvasMETDeltaR.Draw()

canvasMETDeltaR.cd()
canvasMETDeltaR.Update()
canvasMETDeltaR.RedrawAxis()
frameMETDeltaR = canvasMETDeltaR.GetFrame()
frameMETDeltaR.Draw()
#
legendMETDeltaR = ROOT.TLegend(0.65,0.4,0.9,0.6)
legendMETDeltaR.SetBorderSize(0)
legendMETDeltaR.AddEntry(h_genMETvsNuSum, "Gen MET vs Gen #nu addition")
legendMETDeltaR.AddEntry(h_METvsNuSum, "MET vs Gen #nu addition")
legendMETDeltaR.AddEntry(h_METvsGenMET, "MET vs Gen MET");
legendMETDeltaR.Draw()

canvasMETBetween.cd()
canvasMETBetween.Update()
canvasMETBetween.RedrawAxis()
frameMETBetween = canvasMETBetween.GetFrame()
frameMETBetween.Draw()

legendMETBetween = ROOT.TLegend(0.65, 0.2, 0.9, 0.4)
legendMETBetween.SetBorderSize(0)
#legend.SetHeader("#tau* mass");
legendMETBetween.AddEntry(h_missingPtBetween_Reco, "Reconstructed MET")
legendMETBetween.AddEntry(h_missingPtBetween_Gen, "Generator level MET")
legendMETBetween.AddEntry(h_missingPtBetween_Nu, "Summed #nu momentum")
#legend.AddEntry(h_2, "1000 GeV", "F");
legendMETBetween.Draw()

canvasMETBetween.cd()

canvasDeltaR_truth.Update()
canvasDeltaR_truth.RedrawAxis()
frameDeltaR_truth = canvasDeltaR_truth.GetFrame()
frameDeltaR_truth.Draw()

legendDeltaR_truth = ROOT.TLegend(0.65, 0.2, 0.9, 0.4)
legendDeltaR_truth.SetBorderSize(0)
#legend.SetHeader("#tau* mass");
legendDeltaR_truth.AddEntry(h_deltaR0_truth, "Leading #tau Gen vs Reco")
legendDeltaR_truth.AddEntry(h_deltaR1_truth, "Subleading #tau Gen vs Reco")
#legend.AddEntry(h_2, "1000 GeV", "F");
legendDeltaR_truth.Draw()

#canvasDeltaR_nu.Update()
#canvasDeltaR_nu.RedrawAxis()
#frameDeltaR_nu = canvasDeltaR_nu.GetFrame()
#frameDeltaR_nu.Draw()

#legendDeltaR_nu = ROOT.TLegend(0.65, 0.2, 0.9, 0.4)
#legendDeltaR_nu.SetBorderSize(0)
##legend.SetHeader("#tau* mass");
#legendDeltaR_nu.AddEntry(h_deltaR0_nu, "Leading #tau Gen vs Reco")
#legendDeltaR_nu.AddEntry(h_deltaR1_nu, "Subleading #tau Gen vs Reco")
##legend.AddEntry(h_2, "1000 GeV", "F");
#legendDeltaR_nu.Draw()

canvasMomentum_truth.Update()
canvasMomentum_truth.RedrawAxis()
frameMomentum_truth = canvasMomentum_truth.GetFrame()
frameMomentum_truth.Draw()

legendMomentum_truth = ROOT.TLegend(0.65, 0.6, 0.9, 0.8)
legendMomentum_truth.SetBorderSize(0)
#legend.SetHeader("#tau* mass");
legendMomentum_truth.AddEntry(h_genVisPVsRecoP0, "Leading #tau vis mass")
legendMomentum_truth.AddEntry(h_genColPVsRecoP0, "Leading #tau col mass")
legendMomentum_truth.AddEntry(h_genVisPVsRecoP1, "Subleading #tau vis mass")
legendMomentum_truth.AddEntry(h_genColPVsRecoP1, "Subleading #tau col mass")
#legend.AddEntry(h_2, "1000 GeV", "F");
legendMomentum_truth.Draw()
#pdb.set_trace()
save_file = ROOT.TFile("PhiCheck1000_MuTau_TTBkgrdIncl.root","RECREATE")
save_file.cd()
h_missingPtBetween_Gen.Write()
h_missingPtBetween_Reco.Write()
h_missingPtBetween_Nu.Write()
h_genMETvsNuSum.Write()
h_METvsNuSum.Write()
h_METvsGenMET.Write()
h_deltaR0_truth.Write()
h_deltaR1_truth.Write()
h_deltaR0_nu.Write()
h_genColPVsRecoP1.Write()
h_genVisPVsRecoP0.Write()
h_genColPVsRecoP0.Write()
h_genVisPVsRecoP1.Write()
h_minMassVsMaxMass_phiCheck.Write()

canvasMETBetween.Write()
canvasMETDeltaR.Write()
canvasDeltaR_truth.Write()
canvasDeltaR_nu.Write()
canvasMomentum_truth.Write()
canvasMinMaxColor.Write()

save_file.Write()
save_file.Close()
