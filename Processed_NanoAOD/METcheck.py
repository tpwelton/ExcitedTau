import ROOT
import array as a
import CMS_lumi, tdrstyle
import math
import pdb

tdrstyle.setTDRStyle()

signal250File = ROOT.TFile("test_1_chan0_allCuts_phiCheck.root")

h_missingPtBetween_Reco = ROOT.TH1F("missingPtBetween_Reco","",2,-.5,1.5)
h_missingPtBetween_Gen = ROOT.TH1F("missingPtBetween_Gen","",2,-.5,1.5)
h_missingPtBetween_Nu = ROOT.TH1F("missingPtBetween_Nu","",2,-.5,1.5)
h_METvsGenMET = ROOT.TH1F("METvsGenMET","",200,0,4)
h_METvsNuSum = ROOT.TH1F("METvsNuSum","",200,0,4)
h_genMETvsNuSum = ROOT.TH1F("genMETvsNuSum","",200,0,4)
for event in signal250File.Events:
  h_missingPtBetween_Reco.Fill(event.missingPtBetween_Reco)
  h_missingPtBetween_Gen.Fill(event.missingPtBetween_Gen)
  h_missingPtBetween_Nu.Fill(event.missingPtBetween_Nu)
  h_METvsGenMET.Fill(event.METvsGenMET)
  h_METvsNuSum.Fill(event.METvsNuSum)
  h_genMETvsNuSum.Fill(event.genMETvsNuSum)
pdb.set_trace()
#
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

h_genMETvsNuSum.SetTitle(";#Delta R;Events/0.02 radians")
h_genMETvsNuSum.SetLineColor(ROOT.kRed)
h_genMETvsNuSum.SetMarkerSize(0)
ROOT.gPad.SetLogy()
h_genMETvsNuSum.Draw()
h_METvsNuSum.SetTitle(";#Delta R;Events/0.02 radians")
h_METvsNuSum.SetLineColor(ROOT.kBlack)
h_METvsNuSum.SetMarkerSize(0)
h_METvsNuSum.Draw("same")
h_METvsGenMET.SetTitle(";#Delta R;Events/0.02 radians")
h_METvsGenMET.SetLineColor(ROOT.kBlue)
h_METvsGenMET.SetMarkerSize(0)
h_METvsGenMET.Draw("same")

CMS_lumi.lumi_sqrtS = "13TeV"
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(canvasMETBetween,0,0)
CMS_lumi.CMS_lumi(canvasMETDeltaR,0,0)
#

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

pdb.set_trace()
save_file = ROOT.TFile("PhiCheck.root","RECREATE")
save_file.cd()
h_missingPtBetween_Gen.Write()
h_missingPtBetween_Reco.Write()
h_missingPtBetween_Nu.Write()
h_genMETvsNuSum.Write()
h_METvsNuSum.Write()
h_METvsGenMET.Write()
canvasMETBetween.Write()
canvasMETDeltaR.Write()
save_file.Write()
save_file.Close()
signal250File.Close()
