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
year = 2018
lumi = {2016:30171.139, 2017:41525.059, 2018:59725.419} #1/pb
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

sampleLocation = str(year) + "/Samples" + str(year) + "_sdbnd.txt"
#for line in open("Samples2017.txt").readlines():
#for line in open("Samples2018_sdbnd.txt").readlines():
#for line in open("Samples2016_sdbnd.txt").readlines():
for line in open(sampleLocation).readlines():
  if line.find("#") == 0: continue
  params = line.split(",")
  filesList.append([xrd_prefix + i.strip() for i in open(params[0])])
  eventWeights.append(float(params[2])*lumi[year]/float(str(params[1])))
  fileCategory.append(params[3].strip())

pdb.set_trace()
#filesSignal250 = ["test_1_chan0_allCuts_phiCheck.root"]
#filesList.append(filesSignal250); eventWeights.append(0.0177*lumi/10000)
filesSignal1000 = ["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD_chan0_sdbnd.root"]
#filesList.append(filesSignal1000); eventWeights.append(4.069*10.**-3*lumi/10000); fileCategory.append("Signal 1000 GeV")

#h_minMassVsMaxMass = ROOT.TH2F("minMassVsMaxMass","",100,0,2000,100,0,2000)
h_minMassVsMaxMass_phiCheck = ROOT.TH2F("minMassVsMaxMass_phiCheck","",100,0,2000,100,0,2000)
h_minBkgrdSum = ROOT.TH1F("minBkgrdSum","minBkgrdSum",100,0,2000)
h_maxBkgrdSum = ROOT.TH1F("maxBkgrdSum","maxBkgrdSum",100,0,2000)

catNow = ""
h_allTypes_min = {}
h_allTypes_max = {}
h_allTypes = {}
for cat in fileCategory:
  if cat != catNow:
    h_allTypes_min[cat] = ROOT.TH1F(cat+"min",cat,100,0,2000)
    h_allTypes_min[cat].SetMarkerSize(0)
    h_allTypes_max[cat] = ROOT.TH1F(cat+"max",cat,100,0,2000)
    h_allTypes_max[cat].SetMarkerSize(0)
    h_allTypes[cat] = ROOT.TH1F(cat,cat,100,0,2000)
    h_allTypes[cat].SetMarkerSize(0)
    catNow = cat





#minMass = []
#maxMass = []
#minMass_phiCheck = []
#maxMass_phiCheck = []
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
      #this deltaR cut is included in the baseline event selection now
#      if deltaR(event.lep0_vis_eta,event.lep0_vis_phi,event.lep1_vis_eta,event.lep1_vis_phi) < 0.4: continue

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
        gamleplower = event.gamlep0_col_mass
        gamlephigher = event.gamlep1_col_mass
      else:
        gamleplower = event.gamlep1_col_mass
        gamlephigher = event.gamlep0_col_mass
        
#      minMass.append(gamleplower)
#      maxMass.append(gamlephigher)
#      h_minMassVsMaxMass.Fill(gamleplower,gamlephigher,weight)
      if phiChecker.phiChecker(event.lep0_vis_phi,event.lep1_vis_phi,event.MET_phi):
#        minMass_phiCheck.append(gamleplower)
#        maxMass_phiCheck.append(gamlephigher)
        if weight > 10: print("Event with high scaling (" + str(weight) + ") from "+ fileIndiv)
        h_minMassVsMaxMass_phiCheck.Fill(gamleplower,gamlephigher,weight)
        h_allTypes_min[cat].Fill(gamleplower,weight)
        h_allTypes_max[cat].Fill(gamlephigher,weight)
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
#  h_allTypes_max[key].Scale(3.)
  h_maxStack.Add(h_allTypes_max[key])
  h_maxBkgrdSum.Add(h_allTypes_max[key])
  h_allTypes_min[key].SetLineColor(fillColor)
  h_allTypes_min[key].SetFillColor(fillColor)
#  h_allTypes_min[key].Scale(3.)
  h_minStack.Add(h_allTypes_min[key])
  h_minBkgrdSum.Add(h_allTypes_min[key])
  h_allTypes[key].SetFillColor(fillColor)
  h_allTypes[key].SetLineColor(fillColor)
#  h_allTypes[key].Scale(3.)
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
h_MCStack.Draw("HIST")
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
#h_minStack.Draw("HISTSAME")
h_minStack.Draw("HIST")
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
#h_maxStack.Draw("HISTSAME")
h_maxStack.Draw("HIST")
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

#pdb.set_trace()
save_file = ROOT.TFile("MuTau2016_allBkgrds.root","RECREATE")
save_file.cd()
h_minMassVsMaxMass_phiCheck.Write()
h_maxStack.Write()
h_minStack.Write()
h_MCStack.Write()
h_BkgrdSum.Write()

canvasMinMaxColor.Write()
canvasMinStack.Write()
canvasMaxStack.Write()
canvasMassStack.Write()

save_file.Write()
save_file.Close()
