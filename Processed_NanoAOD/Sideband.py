import ROOT
import array as a
import CMS_lumi, tdrstyle
import math
import pdb
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
import phiChecker

tdrstyle.setTDRStyle()
ROOT.gStyle.SetLabelSize(0.03,"XYZ")
#ROOT.gStyle.SetMarkerSize(0)
#ROOT.gStyle.SetMarkerSize(5)

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/RA2b13TeVProduction
lumi = 4025.228+3104.509+7575.579+8650.628 #1/pb
xrd_prefix = "root://cms-xrd-global.cern.ch/"
#xrd_prefix = "root://cmseos.fnal.gov/"
filesList = []
eventWeights = []
fileCategory = []

filesQCD_Pt600to800 = [xrd_prefix + i.strip() for i in open("QCDBackground_Pt600to800_sdbnd.txt")] 
filesQCD_Pt800to1000 = [xrd_prefix + i.strip() for i in open("QCDBackground_Pt800to1000_sdbnd.txt")]
#pdb.set_trace()
eventCount_QCD = {"600to800": 3896412, "800to1000": 3992112}
filesList.append(filesQCD_Pt600to800);eventWeights.append(186.9*lumi/eventCount_QCD["600to800"]);fileCategory.append("QCD")
filesList.append(filesQCD_Pt800to1000);eventWeights.append(32.293*lumi/eventCount_QCD["800to1000"]);fileCategory.append("QCD")

filesTT = [xrd_prefix + i.strip() for i in open("TTGBackground_sdbnd.txt")]
eventCount_TT = {"ext1": 9877942}
filesList.append(filesTT); eventWeights.append(3.697*lumi/sum(eventCount_TT.values())); fileCategory.append("TTG")

filesWG = [xrd_prefix + i.strip() for i in open("WGBackground_sdbnd.txt").readlines()]
eventCount_WG = {"ext1": 5059865, "ext2": 10231994, "ext3": 12219986}
filesList.append(filesWG); eventWeights.append(405.271*lumi/sum(eventCount_WG.values()));fileCategory.append("WG");

filesW = [xrd_prefix + i.strip() for i in open("WJetsBackground_sdbnd.txt").readlines()]
eventCount_W = {"200ToInf": 5884226}
filesList.append(filesW); eventWeights.append(50.71*lumi/sum(eventCount_W.values()));fileCategory.append("WJets");

filesZZ = [xrd_prefix + i.strip() for i in open("ZZBackground_sdbnd.txt").readlines()]
eventCount_ZZ = {"2Jets": 1016643}
filesList.append(filesZZ); eventWeights.append(0.041*lumi/sum(eventCount_ZZ.values()));fileCategory.append("ZZ");

filesDY = [xrd_prefix + i.strip() for i in open("DYJetsBackground_sdbnd.txt").readlines()]
eventCount_DY = {"Pt400to650_ext1": 589842, "Pt400to650_ext2": 604038}
filesList.append(filesDY); eventWeights.append(0.3921*lumi/sum(eventCount_DY.values()));fileCategory.append("DYJets");

filesZ = [xrd_prefix + i.strip() for i in open("ZGBackground_sdbnd.txt").readlines()]
eventCount_Z = {"ext1": 14372682}
filesList.append(filesZ);eventWeights.append(117.864*lumi/sum(eventCount_Z.values()));fileCategory.append("ZG"); 

filesData = [xrd_prefix + i.strip() for i in open("Data_sdbnd.txt").readlines()]
filesList.append(filesData);eventWeights.append(1);fileCategory.append("Data")

#filesSignal250 = ["test_1_chan0_allCuts_phiCheck.root"]
#filesList.append(filesSignal250); eventWeights.append(0.0177*lumi/10000)
#filesSignal1000 = ["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD_chan0_allCuts_phiCheck.root"]
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

catNow = ""
h_allTypes_min = {}
h_allTypes_max = {}
for cat in fileCategory:
  if cat is not catNow:
    h_allTypes_min[cat] = ROOT.TH1F(cat+"min",cat,100,0,2000)
    h_allTypes_min[cat].SetMarkerSize(0)
    h_allTypes_max[cat] = ROOT.TH1F(cat+"max",cat,100,0,2000)
    h_allTypes_max[cat].SetMarkerSize(0)
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
#      pdb.set_trace()
      if not (cat.find("Signal") == -1):# and event.missingPtBetween_Reco:
        h_genVisPVsRecoP0.Fill(event.genVisPVsRecoP0)
        h_genColPVsRecoP0.Fill(event.genColPVsRecoP0)
        h_genVisPVsRecoP1.Fill(event.genVisPVsRecoP1)
        h_genColPVsRecoP1.Fill(event.genColPVsRecoP1)
        h_deltaR0_nu.Fill(event.deltaR0_nu)
        h_deltaR0_nu.Fill(event.deltaR1_nu)
        h_deltaR0_truth.Fill(event.deltaR0_truth)
        h_deltaR1_truth.Fill(event.deltaR1_truth)
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
    events.Close()        

h_maxStack = ROOT.THStack("maxStack","")
h_minStack = ROOT.THStack("minStack","")
for ind,key in enumerate(h_allTypes_max.keys()):
  if key == "Data": continue
  h_allTypes_max[key].SetFillColor(ind+2)
  h_allTypes_max[key].SetLineColor(ind+2)
  h_maxStack.Add(h_allTypes_max[key])
  h_allTypes_min[key].SetLineColor(ind+2)
  h_allTypes_min[key].SetFillColor(ind+2)
  h_minStack.Add(h_allTypes_min[key])

canvasMaxStack = ROOT.TCanvas("MaxStack","")
h_allTypes_max["Data"].SetTitle("; M_{max}(#tau#gamma); Events/20 GeV")
h_allTypes_max["Data"].Draw("ex")
h_maxStack.Draw("HISTSAME")
ROOT.gPad.BuildLegend()
#ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9,"")
CMS_lumi.lumi_sqrtS = "13 TeV"
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(canvasMaxStack,0,0)

canvasMinStack = ROOT.TCanvas("MinStack","")
h_allTypes_min["Data"].SetTitle("; M_{min}(#tau#gamma); Events/20 GeV")
h_allTypes_min["Data"].Draw("ex")
h_minStack.Draw("HISTSAME")
ROOT.gPad.BuildLegend()
#ROOT.gPad.BuildLegend(0.7,0.7,0.9,0.9,"")
CMS_lumi.CMS_lumi(canvasMinStack,0,0)

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
