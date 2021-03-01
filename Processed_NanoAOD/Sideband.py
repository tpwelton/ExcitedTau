import ROOT
import array as a
import CMS_lumi, tdrstyle
import math
import pdb
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import InputTree
from PhysicsTools.NanoAODTools.postprocessing.framework.preskimming import preSkim
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from TauPOG.TauIDSFs.TauIDSFTool import TauIDSFTool
from MuonPOG.MuonSFs.MuonSFTool import MuonSFTool
from trigger import *
#import phiChecker

tdrstyle.setTDRStyle()
ROOT.gStyle.SetLabelSize(0.03,"XYZ")
#ROOT.gStyle.SetMarkerSize(0)
#ROOT.gStyle.SetMarkerSize(5)

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/RA2b13TeVProduction
year = 2017
isEmb = True
channelWord = {1:"ElEl",2:"MuMu",3:"ElMu",4:"TauTau",5:"ElTau",6:"MuTau"}
channel = 6

lumi = {2016:30171.139, 2017:41525.059, 2018:59725.419} #1/pb
lumiMask = True
lumiFile = {2016: 'JSON/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt', 2017: 'JSON/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt', 2018: 'JSON/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'}
#MCScale = {2016: 0.96, 2017: 0.71, 2018: 1.01}
MCScale = {2016: 0.96, 2017: 2.28, 2018: 1.01}
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

#sampleLocation = str(year) + "/Samples" + str(year) + "_sdbnd.txt"
#sampleLocation = str(year) + "/Samples" + str(year) + "_all.txt"
sampleLocation = str(year) + "/Samples" + str(year) + "_embed.txt"
#for line in open("Samples2017.txt").readlines():
#for line in open("Samples2018_sdbnd.txt").readlines():
#for line in open("Samples2016_sdbnd.txt").readlines():
for line in open(sampleLocation).readlines():
  if line.find("#") == 0: continue
  params = line.split(",")
  filesList.append([xrd_prefix + i.strip() for i in open(str(year)+"/"+params[0])])
  eventWeights.append(float(params[2])*lumi[year]/float(str(params[1])))
  fileCategory.append(params[3].strip())

#pdb.set_trace()
#filesSignal250 = ["test_1_chan0_allCuts_phiCheck.root"]
#filesList.append(filesSignal250); eventWeights.append(0.0177*lumi/10000)
#filesSignal1000 = ["Taustar_TauG_L10000_m1000_13TeV_pythia8_NanoAOD_chan0_sdbnd.root"]
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

#h_yield = ROOT.TH1F("yield","yield",len(h_allTypes),0,len(h_allTypes))


numCat = len(set(fileCategory))
#h_Efficiency = ROOT.TH1F("Efficiency","Efficiency",numCat,0,numCat)
h_yield = ROOT.TH1F("yield","yield",numCat,0,numCat)
h_phiCheck = ROOT.TH1F("phiCheck","phiCheck",2*numCat,0,2*numCat)
h_filters = ROOT.TH1F("filters","filters",2*numCat,0,2*numCat)
h_ll_vis_mass = ROOT.TH1F("ll_vis_mass","ll_vis_mass",2*numCat,0,2*numCat)

minMass_phiCheck = {}
maxMass_phiCheck = {}
h_photon_pt = {}
h_photon_dr_cut = {}
h_too_many_leptons = {}
h_bjet_present = {}
h_muNum = {}
h_q0q1_sign = {}
h_MET_pt = {}
h_MET_sig = {}
h_pass_cuts = {}

tauTag = {2016: "2016Legacy", 2017: "2017ReReco", 2018: "2018ReReco"}
if year not in tauTag.keys():
  raise Exception("Invalid data year")
tauIDSFtool_jet = {}
wp_jet = ["VVVLoose","VVLoose","VLoose","Loose","Medium","Tight","VTight","VVTight"]
for wp in wp_jet:
  tauIDSFtool_jet[wp] = TauIDSFTool(tauTag[year],'DeepTau2017v2p1VSjet',wp, False,  isEmb)
tauIDSFtool_mu = TauIDSFTool(tauTag[year],'DeepTau2017v2p1VSmu','Tight')
tauIDSFtool_e = {}
wp_e = ["VLoose","Loose","Medium","Tight","VTight","VVTight"]
for wp in wp_e:
  tauIDSFtool_e[wp] = TauIDSFTool(tauTag[year],'DeepTau2017v2p1VSe',wp)#, False,  isEmb)
muonSFtool = MuonSFTool(year,"Tight","Tight")

catNow = ""
for indGroup,fileGroup in enumerate(filesList):
  weight = eventWeights[indGroup]
  cat = fileCategory[indGroup]
#  if cat.find("Data") == -1: weight = weight*MCScale[year]
  if cat != catNow:
    minMass_phiCheck[cat] = []
    maxMass_phiCheck[cat] = []
#    diff_correct[cat] = []
#    diff_wrong[cat] = []
#    ratio_correct[cat] = []
#    ratio_wrong[cat] = []
#    diff_diff[cat] = []
#    ratio_diff[cat] = []
    h_photon_pt[cat] = ROOT.TH1F(cat+"photon_pt",cat+"photon_pt",100,0,2000)
#    h_tau_correct_pt[cat] = ROOT.TH1F(cat+"tau_correct_pt",cat+"tau_correct_pt",100,0,2000)
#    h_tau_wrong_pt[cat] = ROOT.TH1F(cat+"tau_wrong_pt",cat+"tau_wrong_pt",100,0,2000)
#    h_gen_gam_pt[cat] = ROOT.TH1F(cat+"gen_gam_pt",cat+"gen_gam_pt",100,0,2000)
    h_photon_dr_cut[cat] = ROOT.TH1F(cat+"photon_dr_cut",cat+"photon_dr_cut",16,0,16)
    h_too_many_leptons[cat] = ROOT.TH1F(cat+"too_many_leptons",cat+"too_many_leptons",2,0,2)
    h_bjet_present[cat] = ROOT.TH1F(cat+"bjet_present",cat+"bjet_present",4,-1.75,7.25)
    h_muNum[cat] = ROOT.TH1F(cat+"muNum",cat+"muNum",5,0,5)
    h_q0q1_sign[cat] = ROOT.TH1F(cat+"q0q1_sign",cat+"q0q1_sign",2,-1,1)
    h_MET_pt[cat] = ROOT.TH1F("MET_pt_"+cat,"MET_pt_"+cat,100,0,2000)
    h_MET_sig[cat] = ROOT.TH1F("MET_sig_"+cat,"MET_sig_"+cat,20,0,20)
    h_pass_cuts[cat] = ROOT.TH1F("pass_cuts_"+cat,"pass_cuts_"+cat,14,0,14)
    catNow = cat
  for fileIndiv in fileGroup:
    print("Opening file {}".format(fileIndiv))
    events = ROOT.TFile.Open(fileIndiv)
  #  print(fileIndiv + "\n")
  #  pdb.set_trace()
    try:
      inputTree = events.Get("Events")
    except ReferenceError:
      print("File could not be opened. Skipping...")
      continue
    if not inputTree: continue
    if lumiMask:
      eventlist,jsonFilter = preSkim(inputTree,jsonInput=lumiFile[year])
    else:
      eventlist = None
    Events = InputTree(inputTree,eventlist)
    
    for iEvent in range(Events.entries):
#      if iEvent%1000 != 0: continue
      if iEvent%1000 == 0: print("Processing event {}...".format(iEvent))
      event = Event(Events,iEvent)
      h_pass_cuts[cat].Fill("All",1.)
  
      if not (event.channel == channel): continue
      h_pass_cuts[cat].Fill("Channel",1.)
  
      if not passTrigger(event,channel): continue
      h_pass_cuts[cat].Fill("Trigger",1.)

      h_too_many_leptons[cat].Fill(event.too_many_leptons_cutFlag)
      if event.too_many_leptons_cutFlag: continue
      h_pass_cuts[cat].Fill("TooManyLeptons",1.)
  
      if event.q0q1_sign == 1: 
        h_q0q1_sign[cat].Fill(1)
        continue
      else:
        h_q0q1_sign[cat].Fill(-1)
        h_pass_cuts[cat].Fill("OppositeSign",1.)
      
      if not (event.ll_vis_mass > 100): 
        h_ll_vis_mass.Fill(cat+" Fail",1.)
        continue
      else:
        h_ll_vis_mass.Fill(cat+" Pass",1.)
        h_pass_cuts[cat].Fill("DileptonMass",1.)
  
      #Remove Z events with weaker restrictions on second muon
      if len(event.Muon_pt) > 1:
        muSum = 0
        for ind in range(len(event.Muon_pt)):
          muSum += (event.Muon_pt[ind] >= 10 and abs(event.Muon_eta[ind]) < 2.4 and event.Muon_mediumId[ind] and event.Muon_pfIsoId[ind]>=2)
        h_muNum[cat].Fill(muSum)
        if muSum >= 2: continue
      h_pass_cuts[cat].Fill("Zpair",1.)
  
      if not (event.Flag_goodVertices and event.Flag_globalSuperTightHalo2016Filter and event.Flag_HBHENoiseFilter and event.Flag_HBHENoiseIsoFilter and event.Flag_EcalDeadCellTriggerPrimitiveFilter and event.Flag_BadPFMuonFilter and event.Flag_eeBadScFilter): 
        h_filters.Fill(cat+" Fail",1.)
        continue
      else:
        h_filters.Fill(cat+" Pass",1.)
        h_pass_cuts[cat].Fill("METFilters",1.)
  
      h_MET_pt[cat].Fill(event.MET_pt)
      if event.MET_pt < 20: continue
      h_pass_cuts[cat].Fill("METpt",1.)
  
      h_MET_sig[cat].Fill(event.MET_significance)
      if event.MET_significance < 2: continue
      h_pass_cuts[cat].Fill("METsignificance",1.)
  
      h_bjet_present[cat].Fill(event.bjet_present)
      if event.bjet_present & 1 << 2: continue
      h_pass_cuts[cat].Fill("bJet",1.)
  
      #photon pt bits: [20,50,80,100,120,150,175]
      if not (event.photon_pt_cutFlag & 1 << 3): continue
      h_pass_cuts[cat].Fill("PhotonPt",1.)
      h_photon_pt[cat].Fill(event.photon_pt)
  
      h_photon_dr_cut[cat].Fill(event.photon_dr_cutFlag)
      if event.photon_dr_cutFlag < 2: continue
      h_pass_cuts[cat].Fill("PhotonDeltaR",1.)
  
  
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
  
  
      #Assign min and max mass appropriately
      if event.gamlep0_col_mass < event.gamlep1_col_mass:
        gamleplower = event.gamlep0_col_mass
        gamlephigher = event.gamlep1_col_mass
      else:
        gamleplower = event.gamlep1_col_mass
        gamlephigher = event.gamlep0_col_mass
        
      lepInd = 0
      sf = weight
      if hasattr(event,'puWeight'):
        sf *= event.puWeight
      if cat.find("Data") == -1: 
        if channel & 1 << 1: #muon-type channel
          sf *= muonSFtool.getSF_ID(event.lep0_vis_pt,event.lep0_vis_eta)*muonSFtool.getSF_ISO(event.lep0_vis_pt,event.lep0_vis_eta)*muonSFtool.getSF_Trigger(event.lep0_vis_pt,event.lep0_vis_eta)
          lepInd += 1
        if channel & 1 << 2: #had-type channel
          genPartFlav = [0,0]
          Flav0found = -1
          Flav1found = -1
          if lepInd == 0:
            for ind in range(len(event.Tau_pt)):
              if abs(event.Tau_pt[ind]-event.lep0_vis_pt) < 0.0001 and Flav0found == -1:
                genPartFlav[0] = event.Tau_genPartFlav[ind]
                Flav0found = ind
              if abs(event.Tau_pt[ind]-event.lep1_vis_pt) < 0.0001 and Flav1found == -1:
                if Flav0found == ind:
                  print("Error! Method doesn't work...")
                  continue
                genPartFlav[1] = event.Tau_genPartFlav[ind]
                Flav1found = ind
          else:
            for ind in range(len(event.Tau_pt)):
              if abs(event.Tau_pt[ind]-event.lep1_vis_pt) < 0.0001 and Flav1found == -1:
                genPartFlav[1] = event.Tau_genPartFlav[ind]
                break 
          sf *= tauIDSFtool_jet["Tight"].getSFvsPT(event.lep0_vis_pt,genPartFlav[0])*tauIDSFtool_mu.getSFvsEta(event.lep0_vis_eta,genPartFlav[0])*tauIDSFtool_e["Tight"].getSFvsEta(event.lep0_vis_eta,genPartFlav[0])*tauIDSFtool_jet["Tight"].getSFvsPT(event.lep1_vis_pt,genPartFlav[1])*tauIDSFtool_mu.getSFvsEta(event.lep1_vis_eta,genPartFlav[1])*tauIDSFtool_e["Tight"].getSFvsEta(event.lep1_vis_eta,genPartFlav[1])
      if event.phiCheck_cutFlag:
        h_phiCheck.Fill(cat+" Pass",1.)
        h_pass_cuts[cat].Fill("PhiCheck",1.)
        minMass_phiCheck[cat].append(gamleplower)
        maxMass_phiCheck[cat].append(gamlephigher)
        if weight > 10: print("Event with high scaling (" + str(weight) + ") from "+ fileIndiv)
        h_minMassVsMaxMass_phiCheck.Fill(gamleplower,gamlephigher,sf)
        h_allTypes_min[cat].Fill(gamleplower,sf)
        h_allTypes_max[cat].Fill(gamlephigher,sf)
        h_yield.Fill(cat,sf)
        h_allTypes[cat].Fill(event.ll_col_mass,sf)
      else: 
        h_phiCheck.Fill(cat + " Fail",1.)
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


canvasYield = ROOT.TCanvas("Yield","")
h_yield.Draw("HIST")

if "Data" in h_allTypes.keys():
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
#pdb.set_trace()

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
canvasPhiCheck = ROOT.TCanvas("PhiCheck","Phi Check")
h_phiCheck.LabelsDeflate("X")
h_phiCheck.LabelsOption("a","X")
h_phiCheck.Draw("HIST")
canvasVisMass = ROOT.TCanvas("VisMass","Vis Mass")
h_ll_vis_mass.LabelsDeflate("X")
h_ll_vis_mass.LabelsOption("a","X")
h_ll_vis_mass.Draw("HIST")
canvasFilters = ROOT.TCanvas("Filters","Filters")
h_filters.LabelsDeflate("X")
h_filters.LabelsOption("a","X")
h_filters.Draw("HIST")
canvasPhotonPt = ROOT.TCanvas("PhotonPt","Photon Pt")
for ind,key in enumerate(h_photon_pt.keys()):
  h_photon_pt[key].SetLineColor(ind + 2)
  h_photon_pt[key].SetMarkerSize(0)
  h_photon_pt[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasMETpt = ROOT.TCanvas("MET_pt","MET Pt")
for ind,key in enumerate(h_MET_pt.keys()):
  h_MET_pt[key].SetLineColor(ind + 2)
  h_MET_pt[key].SetMarkerSize(0)
  h_MET_pt[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasMETsig = ROOT.TCanvas("MET_sig","MET Sig")
for ind,key in enumerate(h_MET_sig.keys()):
  h_MET_sig[key].SetLineColor(ind + 2)
  h_MET_sig[key].SetMarkerSize(0)
  h_MET_sig[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasPhotonDrCut = ROOT.TCanvas("PhotonDr","Photon /Delta R Cut")
for ind,key in enumerate(h_photon_dr_cut.keys()):
  h_photon_dr_cut[key].SetLineColor(ind + 2)
  h_photon_dr_cut[key].SetMarkerSize(0)
  h_photon_dr_cut[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasTooManyLeptons = ROOT.TCanvas("TooManyLeptons","Too Many Leptons Flag")
for ind,key in enumerate(h_too_many_leptons.keys()):
  h_too_many_leptons[key].SetLineColor(ind + 2)
  h_too_many_leptons[key].SetMarkerSize(0)
  h_too_many_leptons[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasQ0Q1 = ROOT.TCanvas("q0q1","q0q1 sign")
for ind,key in enumerate(h_q0q1_sign.keys()):
  h_q0q1_sign[key].SetLineColor(ind + 2)
  h_q0q1_sign[key].SetMarkerSize(0)
  h_q0q1_sign[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasBjetPresent = ROOT.TCanvas("BjetPresent","b jet present Cut")
for ind,key in enumerate(h_bjet_present.keys()):
  h_bjet_present[key].SetLineColor(ind + 2)
  h_bjet_present[key].SetMarkerSize(0)
  h_bjet_present[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
canvasMuNum = ROOT.TCanvas("MuNum","Number of Muons")
for ind,key in enumerate(h_muNum.keys()):
  h_muNum[key].SetLineColor(ind + 2)
  h_muNum[key].SetMarkerSize(0)
  h_muNum[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)

canvasPassCuts = ROOT.TCanvas("PassCuts","Cut Flow Table")
for ind,key in enumerate(h_pass_cuts.keys()):
  h_pass_cuts[key].SetLineColor(ind + 2)
  h_pass_cuts[key].SetMarkerSize(0)
  h_pass_cuts[key].Draw("HISTSAME")
ROOT.gPad.BuildLegend(0.7,0.6,0.9,0.9)
pdb.set_trace()
canvasPassCuts.SetLogy()

pdb.set_trace()
save_file = ROOT.TFile(channelWord[channel] + str(year) + "_allBkgrds.root","RECREATE")
save_file.cd()

if "Data" in h_allTypes.keys():
  canvasMinStack.Write()
  canvasMaxStack.Write()
  canvasMassStack.Write()
  h_maxStack.Write()
  h_minStack.Write()
  h_MCStack.Write()

canvasMinMaxColor.Write()
canvasYield.Write()
canvasPhiCheck.Write()
canvasVisMass.Write()
canvasFilters.Write()
canvasPhotonPt.Write()
canvasMETpt.Write()
canvasMETsig.Write()
canvasPhotonDrCut.Write()
canvasTooManyLeptons.Write()
canvasQ0Q1.Write()
canvasBjetPresent.Write()
canvasMuNum.Write()
canvasPassCuts.Write()

#for graph in minMassVsMaxMass_mg:
#  graph.Write()
h_minMassVsMaxMass_phiCheck.Write()
h_BkgrdSum.Write()
h_yield.Write()
h_phiCheck.Write()
h_ll_vis_mass.Write()
h_filters.Write()
for key in h_photon_pt.keys():
  h_photon_pt[key].Write()
  h_MET_pt[key].Write()
  h_MET_sig[key].Write()
  h_photon_dr_cut[key].Write()
  h_too_many_leptons[key].Write()
  h_q0q1_sign[key].Write()
  h_bjet_present[key].Write()
  h_muNum[key].Write()
  h_pass_cuts[key].Write()

save_file.Write()
save_file.Close()
