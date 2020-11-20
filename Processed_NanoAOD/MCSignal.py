import ROOT
import array as a
import CMS_lumi, tdrstyle
import math
import pdb
import re
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
import phiChecker

tdrstyle.setTDRStyle()
ROOT.gStyle.SetLabelSize(0.03,"XYZ")
#ROOT.gStyle.SetOptTitle(1)
#ROOT.gStyle.SetTitleStyle(1)
#ROOT.gStyle.SetTitleX(.2)
#ROOT.gStyle.SetTitleY(.95)
#ROOT.gStyle.SetTitleBorderSize(0)
#ROOT.gStyle.SetMarkerSize(0)
#ROOT.gStyle.SetMarkerSize(5)

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/RA2b13TeVProduction
year = 2018
#massesToRun = ["250","750","1500","2500","4000"]
#massesToRun = ["1000"]
#massesToRun = ["250","500","1000"]
massesToRun = ["250","375","500","625","750","1000","1250","1500","1750","2000","2500","3000","3500","4000","4500","5000"] 

channel = 6
channelWord = {1:"ElEl", 2:"MuMu", 3:"ElMu", 4:"HadHad", 5:"ElHad", 6:"MuHad"}
BR_tau = {"el": .1783, "mu":.1741,"had":.6476}
BR_channel = {1: BR_tau["el"]**2, 2: BR_tau["mu"]**2, 3: 2*BR_tau["el"]*BR_tau["mu"], 4: BR_tau["had"]**2, 5: 2*BR_tau["el"]*BR_tau["had"], 6: 2*BR_tau["mu"]*BR_tau["had"]}


lumi = {2016:30171.139, 2017:41525.059, 2018:59725.419} #1/pb
xsec = {175:0.02888,250:0.02135,375:0.01546,500:0.01177,625:0.009072,750:0.007024,1000:0.004236,1250:0.002554,1500:0.001522,1750:0.0009048,2000:0.0005328,2500:0.0001862,3000:6.429e-5,3500:2.23e-5,4000:8.056e-6,4500:3.009e-6,5000: 1.178e-6}
xrd_prefix = "root://cms-xrd-global.cern.ch/"
#xrd_prefix = "root://cmseos.fnal.gov/"
filesList = []
eventWeights = []
fileCategory = []

sampleLocation = "Signal" + str(year) + ".txt"
for line in open(sampleLocation).readlines():
  if line.find("#") == 0: continue
  filesList.append(xrd_prefix + line.strip())
  massString = re.search("m\d+",line)
#  eventWeights.append(1)
  fileCategory.append(massString.group()[1:])


#h_minMassVsMaxMass = ROOT.TH2F("minMassVsMaxMass","",100,0,2000,100,0,2000)
numCat = len(set(fileCategory))
h_signalEfficiency = ROOT.TH1F("signalEfficiency","signalEfficiency",numCat,0,numCat)
h_yield = ROOT.TH1F("yield","yield",numCat,0,numCat)
h_phiCheck = ROOT.TH1F("phiCheck","phiCheck",2*numCat,0,2*numCat)
h_filters = ROOT.TH1F("filters","filters",2*numCat,0,2*numCat)
h_ll_vis_mass = ROOT.TH1F("ll_vis_mass","ll_vis_mass",2*numCat,0,2*numCat)
#h_diff_correct = ROOT.TH1F("diff_correct","diff_correct",1000,-10,100)
#h_ratio_correct = ROOT.TH1F("ratio_correct","ratio_correct",1000,0,20)
#h_diff_wrong = ROOT.TH1F("diff_wrong","diff_wrong",1000,-10,100)
#h_ratio_wrong = ROOT.TH1F("ratio_wrong","ratio_wrong",1000,0,20)
#h_diff_diff = ROOT.TH1F("diff diff","diff diff",100,-10,10)
#h_ratio_diff = ROOT.TH1F("ratio diff","ratio diff",100,-10,10)

#pdb.set_trace()
#minMass = []
#maxMass = []
minMass_phiCheck = {}
maxMass_phiCheck = {}
diff_correct = {}
diff_wrong = {}
ratio_correct = {}
ratio_wrong = {}
diff_diff = {}
ratio_diff = {}
h_photon_pt = {}
h_tau_correct_pt = {}
h_tau_wrong_pt = {}
h_gen_gam_pt = {}
catNow = ""
for ind,fileIndiv in enumerate(filesList):
#  weight = eventWeights[ind]
  cat = fileCategory[ind]
  if cat not in massesToRun: continue
  if cat != catNow:
    minMass_phiCheck[cat] = []
    maxMass_phiCheck[cat] = []
    diff_correct[cat] = []
    diff_wrong[cat] = []
    ratio_correct[cat] = []
    ratio_wrong[cat] = []
    diff_diff[cat] = []
    ratio_diff[cat] = []
    h_photon_pt[cat] = ROOT.TH1F(cat+"photon_pt",cat+"photon_pt",100,0,2000)
    h_tau_correct_pt[cat] = ROOT.TH1F(cat+"tau_correct_pt",cat+"tau_correct_pt",100,0,2000)
    h_tau_wrong_pt[cat] = ROOT.TH1F(cat+"tau_wrong_pt",cat+"tau_wrong_pt",100,0,2000)
    h_gen_gam_pt[cat] = ROOT.TH1F(cat+"gen_gam_pt",cat+"gen_gam_pt",100,0,2000)
    catNow = cat
  events = ROOT.TFile.Open(fileIndiv)
#  print(fileIndiv + "\n")
#  pdb.set_trace()
  inputTree = events.Get("Events")
  if not inputTree: continue
  Events = InputTree(inputTree)
  
  for iEvent in range(Events.entries):
    event = Event(Events,iEvent)
    if not (event.channel == channel): continue
#    if not (event.photon_pt > 20): continue
    h_photon_pt[cat].Fill(event.photon_pt)
#    if not (event.ll_vis_mass > 100): continue
    if not (event.ll_vis_mass > 100): 
      h_ll_vis_mass.Fill(cat+" Fail",1.)
      continue
    else:
      h_ll_vis_mass.Fill(cat+" Pass",1.)
    if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_eeBadScFilter): 
      h_filters.Fill(cat+" Fail",1.)
      continue
    else:
      h_filters.Fill(cat+" Pass",1.)
    #this deltaR cut is included in the baseline event selection now
#     if deltaR(event.lep0_vis_eta,event.lep0_vis_phi,event.lep1_vis_eta,event.lep1_vis_phi) < 0.4: continue

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

#     pdb.set_trace()
#     if not (cat.find("Signal") == -1):# and event.missingPtBetween_Reco:
#       h_genVisPVsRecoP0.Fill(event.genVisPVsRecoP0)
#       h_genColPVsRecoP0.Fill(event.genColPVsRecoP0)
#       h_genVisPVsRecoP1.Fill(event.genVisPVsRecoP1)
#       h_genColPVsRecoP1.Fill(event.genColPVsRecoP1)
#       h_deltaR0_nu.Fill(event.deltaR0_nu)
#       h_deltaR0_nu.Fill(event.deltaR1_nu)
#       h_deltaR0_truth.Fill(event.deltaR0_truth)
#       h_deltaR1_truth.Fill(event.deltaR1_truth)

    #Remove Z events with weaker restrictions on second muon
    if len(event.Muon_pt) > 1:
      muSum = 0
      for ind in range(len(event.Muon_pt)):
        muSum += (event.Muon_pt[ind] >= 10 and abs(event.Muon_eta[ind]) < 2.4 and event.Muon_mediumId[ind] and event.Muon_pfIsoId[ind]>=2)
      if muSum >= 2: continue 

    tau = -99
    taustar_daughters = []
    for idx in range(len(event.GenPart_pdgId)):
      if abs(event.GenPart_pdgId[idx]) == 15: 
        if event.GenPart_genPartIdxMother[idx] > 1: 
          if event.GenPart_genPartIdxMother[idx] == tau:
            tau = idx
        else:
          tau = idx
      if abs(event.GenPart_pdgId[idx]) == 4000015:
        if (event.GenPart_statusFlags[idx] & (1 << 13)):
          for idx_daughter in range(idx+1,len(event.GenPart_pdgId)):
            if event.GenPart_genPartIdxMother[idx_daughter] == idx:
              taustar_daughters.append(idx_daughter)
      taustar_daughters_updated = [x for x in taustar_daughters if not (event.GenPart_genPartIdxMother[idx] == x and event.GenPart_pdgId[idx] == event.GenPart_pdgId[x])]
      if len(taustar_daughters_updated) < len(taustar_daughters):
        taustar_daughters_updated.append(idx)
        taustar_daughters = taustar_daughters_updated
    taustar_daughters.sort(key=lambda x: event.GenPart_pdgId[x])
    tau_correct_idx = taustar_daughters[0]
    gam_idx = taustar_daughters[1]
    tau_correct = ROOT.TLorentzVector()
    tau_correct.SetPtEtaPhiM(event.GenPart_pt[tau_correct_idx],event.GenPart_eta[tau_correct_idx],event.GenPart_phi[tau_correct_idx],event.GenPart_mass[tau_correct_idx])
    h_tau_correct_pt[cat].Fill(tau_correct.Pt())
    gam = ROOT.TLorentzVector()
    gam.SetPtEtaPhiM(event.GenPart_pt[gam_idx],event.GenPart_eta[gam_idx],event.GenPart_phi[gam_idx],event.GenPart_mass[gam_idx])
    h_gen_gam_pt[cat].Fill(gam.Pt())
    tau_wrong = ROOT.TLorentzVector()
    tau_wrong.SetPtEtaPhiM(event.GenPart_pt[tau],event.GenPart_eta[tau],event.GenPart_phi[tau],event.GenPart_mass[tau])
    h_tau_wrong_pt[cat].Fill(tau_wrong.Pt())
    deltaR_correct = deltaR(tau_correct.Eta(),tau_correct.Phi(),gam.Eta(),gam.Phi())
    deltaR_wrong = deltaR(tau_wrong.Eta(),tau_wrong.Phi(),gam.Eta(),gam.Phi())
    taustar_reco_correct = tau_correct + gam
    deltaR_reco_correct = 2*taustar_reco_correct.M()/taustar_reco_correct.Pt()
    diff_correct[cat].append(deltaR_reco_correct - deltaR_correct)
    ratio_correct[cat].append(deltaR_reco_correct/deltaR_correct)
    taustar_reco_wrong = tau_wrong + gam
    deltaR_reco_wrong = 2*taustar_reco_wrong.M()/taustar_reco_wrong.Pt()
    diff_wrong[cat].append(deltaR_reco_wrong - deltaR_wrong)
    ratio_wrong[cat].append(deltaR_reco_wrong/deltaR_wrong)
    diff_diff[cat].append(diff_correct[cat][-1] - diff_wrong[cat][-1])
    ratio_diff[cat].append(ratio_correct[cat][-1] - ratio_wrong[cat][-1])

    #Assign min and max mass appropriately
    if event.gamlep0_col_mass < event.gamlep1_col_mass:
      gamleplower = event.gamlep0_col_mass
      gamlephigher = event.gamlep1_col_mass
    else:
      gamleplower = event.gamlep1_col_mass
      gamlephigher = event.gamlep0_col_mass
      
#     minMass.append(gamleplower)
#     maxMass.append(gamlephigher)
#     h_minMassVsMaxMass.Fill(gamleplower,gamlephigher,weight)
    if phiChecker.phiChecker(event.lep0_vis_phi,event.lep1_vis_phi,event.MET_phi):
      h_phiCheck.Fill(cat+" Pass",1.)
      minMass_phiCheck[cat].append(gamleplower)
      maxMass_phiCheck[cat].append(gamlephigher)
      h_signalEfficiency.Fill(cat,1./(50000.*BR_channel[channel]))
      h_yield.Fill(cat,xsec[int(cat)]*lumi[year]/50000.)
#       if weight > 10: print("Event with high scaling (" + str(weight) + ") from "+ fileIndiv)
#       h_minMassVsMaxMass_phiCheck.Fill(gamleplower,gamlephigher,weight)
#       h_allTypes_min[cat].Fill(gamleplower,weight)
#       h_allTypes_max[cat].Fill(gamlephigher,weight)
#     h_allTypes[cat].Fill(event.ll_col_mass,weight)
    else: 
      h_phiCheck.Fill(cat + " Fail",1.)
  events.Close()        

minMassVsMaxMass_graph = {}
minMassVsMaxMass_mg = []#ROOT.TMultiGraph()
h_diff_diff = {}
h_ratio_diff = {}
for ind,key in enumerate(massesToRun):
  minMassVsMaxMass_graph[key] = ROOT.TGraph(len(minMass_phiCheck[key]),a.array('d',minMass_phiCheck[key]),a.array('d',maxMass_phiCheck[key]))
#  minMassVsMaxMass_graph[key].GetXaxis().SetLimits(0,6000)
#  minMassVsMaxMass_graph[key].GetYaxis().SetLimits(0,6000)
  if ind%5 == 0: minMassVsMaxMass_mg.append(ROOT.TMultiGraph())
  markerColor = ind%5 + 2
  minMassVsMaxMass_graph[key].SetTitle(key)
  minMassVsMaxMass_graph[key].SetLineColor(0)
  minMassVsMaxMass_graph[key].SetMarkerColor(markerColor)
  minMassVsMaxMass_graph[key].SetMarkerSize(.125)
  minMassVsMaxMass_mg[ind/5].Add(minMassVsMaxMass_graph[key])
  h_diff_diff[key] = ROOT.TH1F("diff_diff"+key,key,100,-10,10)
  h_diff_diff[key].FillN(len(diff_diff[key]),a.array('d',diff_diff[key]),ROOT.nullptr)
  h_ratio_diff[key] = ROOT.TH1F("ratio_diff"+key,key,100,-10,10)
  h_ratio_diff[key].FillN(len(ratio_diff[key]),a.array('d',ratio_diff[key]),ROOT.nullptr)
  
canvas = []
for indCanvas,graph in enumerate(minMassVsMaxMass_mg):
  canvas.append(ROOT.TCanvas("SignalGraph" + str(indCanvas),"SignalGraph" + str(indCanvas)))
  graph.SetMinimum(0.)
  graph.SetMaximum(6000.)
  graph.SetTitle("; M_{min}(#tau#gamma); M_{max}(#tau#gamma)")
  graph.Draw("AP")
  graph.GetHistogram().GetXaxis().SetRangeUser(0.,6000.)
  ROOT.gPad.Modified()
  ROOT.gPad.Update()
#minMassVsMaxMass_mg.GetXaxis().SetLimits(0,6000)
#minMassVsMaxMass_mg.GetYaxis().SetLimits(0,6000)
  ROOT.gPad.BuildLegend(0.6,0.2,0.9,0.4,"#tau* Mass [GeV]")
canvasSignalEfficiency = ROOT.TCanvas("SignalEfficiency","")
h_signalEfficiency.SetTitle("Signal Efficiency (#tau_{#mu}#tau_{h} events only); #tau* Mass [GeV]; Events Accepted/Total Events")
h_signalEfficiency.SetMinimum(0)
h_signalEfficiency.Draw("PE")
#simParams = ROOT.TPaveText(0.7,0.8,0.95,0.95,"NB")
#simParams.AddText("Simulation Parameters:")
#simParams.AddText("#lambda (coupling constant) = 1")
#simParams.AddText("#Lambda (compositeness scale) = 10000 GeV")
#simParams.Draw()
canvasYield = ROOT.TCanvas("Yield","")
h_yield.SetTitle("Signal Yield (#tau_{#mu}#tau_{h} events only); #tau* Mass [GeV]; Expected Events")
h_yield.Draw("HISTE")

canvasPhiCheck = ROOT.TCanvas("PhiCheck","Phi Check")
h_phiCheck.Draw("HIST")
canvasVisMass = ROOT.TCanvas("VisMass","Vis Mass")
h_ll_vis_mass.Draw("HIST")
canvasFilters = ROOT.TCanvas("Filters","Filters")
h_filters.Draw("HIST")
canvasPhotonPt = ROOT.TCanvas("PhotonPt","Photon Pt")
for ind,key in enumerate(reversed(massesToRun)):
  h_photon_pt[key].SetLineColor(ind + 2)
  h_photon_pt[key].SetMarkerSize(0)
  h_photon_pt[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasTauCorrectPt = ROOT.TCanvas("TauCorrectPt","Tau Correct Pt")
for ind,key in enumerate(reversed(massesToRun)):
  h_tau_correct_pt[key].SetLineColor(ind + 2)
  h_tau_correct_pt[key].SetMarkerSize(0)
  h_tau_correct_pt[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasTauWrongPt = ROOT.TCanvas("TauWrongPt","Tau Wrong Pt")
for ind,key in enumerate(reversed(massesToRun)):
  h_tau_wrong_pt[key].SetLineColor(ind + 2)
  h_tau_wrong_pt[key].SetMarkerSize(0)
  h_tau_wrong_pt[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasGenGamPt = ROOT.TCanvas("GenGamPt","Gen Gamma Pt")
for ind,key in enumerate(reversed(massesToRun)):
  h_gen_gam_pt[key].SetLineColor(ind + 2)
  h_gen_gam_pt[key].SetMarkerSize(0)
  h_gen_gam_pt[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)

#canvasDiff = ROOT.TCanvas("Diff","Diff")
#h_diff_correct.Draw("HIST")
#h_diff_wrong.SetLineColor(ROOT.kRed)
#h_diff_wrong.Draw("HISTSAME")
#canvasRatio = ROOT.TCanvas("Ratio","Ratio")
#h_ratio_correct.Draw("HIST")
#h_ratio_wrong.SetLineColor(ROOT.kRed)
#h_ratio_wrong.Draw("HISTSAME")










#canvasDiffDiff = ROOT.TCanvas("DiffDiff","DiffDiff")
#for ind,key in enumerate(reversed(massesToRun)):
#  h_diff_diff[key].SetLineColor(ind + 2)
#  h_diff_diff[key].SetMarkerSize(0)
#  h_diff_diff[key].Draw("HISTSAME")
#ROOT.gPad.BuildLegend(0.2,0.6,0.5,0.9)
#canvasRatioDiff = ROOT.TCanvas("RatioDiff","RatioDiff")
#for ind,key in enumerate(reversed(massesToRun)):
#  h_ratio_diff[key].SetLineColor(ind + 2)
#  h_ratio_diff[key].SetMarkerSize(0)
#  h_ratio_diff[key].Draw("HISTSAME")
pdb.set_trace()

#pdb.set_trace()
save_file = ROOT.TFile(channelWord[channel] + str(year) + "_signal.root","RECREATE")
save_file.cd()

for canv in canvas:
  canv.Write()
canvasSignalEfficiency.Write()
canvasYield.Write()

for graph in minMassVsMaxMass_mg:
  graph.Write()
h_signalEfficiency.Write()
h_yield.Write()

save_file.Write()
save_file.Close()
