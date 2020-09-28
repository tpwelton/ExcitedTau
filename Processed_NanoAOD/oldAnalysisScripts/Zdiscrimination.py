import ROOT
import array as a
import CMS_lumi, tdrstyle
import math
import pdb

tdrstyle.setTDRStyle()

backgroundTauFile = ROOT.TFile("TauTau2018D_hists.root")

backgroundTau_plot = backgroundTauFile.Get("plots/ll_vis_mass")
backgroundTau_plot.Draw('hist')
backgroundTaucol_plot = backgroundTauFile.Get("plots/ll_col_mass")
backgroundTaucol_plot.Draw('hist')

backgroundMuFile = ROOT.TFile("MuTau2018D_photon100_hists_slim.root")

backgroundMu_plot = backgroundMuFile.Get("plots/ll_vis_mass")
backgroundMu_plot.Draw('hist')
backgroundMucol_plot = backgroundMuFile.Get("plots/ll_col_mass")
backgroundMucol_plot.Draw('hist')

signal1000MuFile = ROOT.TFile("MuTauSignal1000_photon100_hists_slim.root")

signal1000Mu_plot = signal1000MuFile.Get("plots/ll_vis_mass")
signal1000Mu_plot.Draw('hist')
signal1000Mucol_plot = signal1000MuFile.Get("plots/ll_col_mass")
signal1000Mucol_plot.Draw('hist')

signal250MuFile = ROOT.TFile("MuTauSignal250_photon100_hists_slim.root")

signal250Mu_plot = signal250MuFile.Get("plots/ll_vis_mass")
signal250Mu_plot.Draw('hist')
signal250Mucol_plot = signal250MuFile.Get("plots/ll_col_mass")
signal250Mucol_plot.Draw('hist')

signal1000TauFile = ROOT.TFile("TauTauSignal1000_hists.root")

signal1000Tau_plot = signal1000TauFile.Get("plots/ll_vis_mass")
signal1000Tau_plot.Draw('hist')
signal1000Taucol_plot = signal1000TauFile.Get("plots/ll_col_mass")
signal1000Taucol_plot.Draw('hist')

signal250TauFile = ROOT.TFile("TauTauSignal250_hists.root")

signal250Tau_plot = signal250TauFile.Get("plots/ll_vis_mass")
signal250Tau_plot.Draw('hist')
signal250Taucol_plot = signal250TauFile.Get("plots/ll_col_mass")
signal250Taucol_plot.Draw('hist')

nBins = signal1000Mu_plot.GetNbinsX()

signal1000MuIntegral = signal1000Mu_plot.GetEntries()
signal250MuIntegral = signal250Mu_plot.GetEntries()
signal1000TauIntegral = signal1000Tau_plot.GetEntries()
signal250TauIntegral = signal250Tau_plot.GetEntries()
backgroundTauIntegral = backgroundTau_plot.GetEntries()
backgroundMuIntegral = backgroundMu_plot.GetEntries()

signal1000MuCount = 0.0
signal250MuCount = 0.0
fractionSignal1000Mu = []
fractionSignal250Mu = []
signal1000TauCount = 0.0
signal250TauCount = 0.0
fractionSignal1000Tau = []
fractionSignal250Tau = []
backgroundMuCount = 0.0
backgroundTauCount = 0.0
fractionBackgroundMu = []
fractionBackgroundTau = []
signal1000MucolCount = 0.0
signal250MucolCount = 0.0
fractionSignal1000Mucol = []
fractionSignal250Mucol = []
signal1000TaucolCount = 0.0
signal250TaucolCount = 0.0
fractionSignal1000Taucol = []
fractionSignal250Taucol = []
backgroundMucolCount = 0.0
backgroundTaucolCount = 0.0
fractionBackgroundMucol = []
fractionBackgroundTaucol = []
sig1000MuOverRootBackground = []
sig1000TauOverRootBackground = []
sig250MuOverRootBackground = []
sig250TauOverRootBackground = []
binCenter = []

for i in xrange(nBins):
  signal1000MuCount += signal1000Mu_plot.GetBinContent(i)
  signal250MuCount += signal250Mu_plot.GetBinContent(i)
  fractionSignal1000Mu.append(signal1000MuCount/signal1000MuIntegral)
  fractionSignal250Mu.append(signal250MuCount/signal250MuIntegral)
  signal1000TauCount += signal1000Tau_plot.GetBinContent(i)
  signal250TauCount += signal250Tau_plot.GetBinContent(i)
  fractionSignal1000Tau.append(signal1000TauCount/signal1000TauIntegral)
  fractionSignal250Tau.append(signal250TauCount/signal250TauIntegral)
  backgroundMuCount += backgroundMu_plot.GetBinContent(i)
  backgroundTauCount += backgroundTau_plot.GetBinContent(i)
  fractionBackgroundMu.append(backgroundMuCount/backgroundMuIntegral)
  fractionBackgroundTau.append(backgroundTauCount/backgroundTauIntegral)
  if backgroundMuCount > 0:
    sig1000MuOverRootBackground.append(fractionSignal1000Mu[i]/fractionBackgroundMu[i])
    sig250MuOverRootBackground.append(fractionSignal250Mu[i]/fractionBackgroundMu[i])
  else:
    sig1000MuOverRootBackground.append(0)
    sig250MuOverRootBackground.append(0)
  if backgroundTauCount > 0:
    sig1000TauOverRootBackground.append(fractionSignal1000Tau[i]/fractionBackgroundTau[i])
    sig250TauOverRootBackground.append(fractionSignal250Tau[i]/fractionBackgroundTau[i])
  else:
    sig1000TauOverRootBackground.append(0)
    sig250TauOverRootBackground.append(0)
  signal1000MucolCount += signal1000Mucol_plot.GetBinContent(i)
  signal250MucolCount += signal250Mucol_plot.GetBinContent(i)
  fractionSignal1000Mucol.append(signal1000MucolCount/signal1000MuIntegral)
  fractionSignal250Mucol.append(signal250MucolCount/signal250MuIntegral)
  signal1000TaucolCount += signal1000Taucol_plot.GetBinContent(i)
  signal250TaucolCount += signal250Taucol_plot.GetBinContent(i)
  fractionSignal1000Taucol.append(signal1000TaucolCount/signal1000TauIntegral)
  fractionSignal250Taucol.append(signal250TaucolCount/signal250TauIntegral)
  backgroundMucolCount += backgroundMucol_plot.GetBinContent(i)
  backgroundTaucolCount += backgroundTaucol_plot.GetBinContent(i)
  fractionBackgroundMucol.append(backgroundMucolCount/backgroundMuIntegral)
  fractionBackgroundTaucol.append(backgroundTaucolCount/backgroundTauIntegral)
  binCenter.append(signal1000Mu_plot.GetBinCenter(i))

signal1000Mu_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal1000Mu))
signal250Mu_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal250Mu))
signal1000Tau_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal1000Tau))
signal250Tau_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal250Tau))
backgroundMu_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionBackgroundMu))
backgroundTau_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionBackgroundTau))

signal1000Mucol_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal1000Mucol))
signal250Mucol_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal250Mucol))
signal1000Taucol_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal1000Taucol))
signal250Taucol_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionSignal250Taucol))
backgroundMucol_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionBackgroundMucol))
backgroundTaucol_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',fractionBackgroundTaucol))

sig1000MuOverRootBackground_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',sig1000MuOverRootBackground))
sig250MuOverRootBackground_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',sig250MuOverRootBackground))
sig1000TauOverRootBackground_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',sig1000TauOverRootBackground))
sig250TauOverRootBackground_graph = ROOT.TGraph(len(binCenter),a.array('d',binCenter),a.array('d',sig250TauOverRootBackground))

canvasMu = ROOT.TCanvas('Mu','')

backgroundMu_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
backgroundMu_graph.SetLineColor(ROOT.kRed)
backgroundMu_graph.SetMarkerSize(0)
backgroundMu_graph.GetXaxis().SetRange(0,1000)
backgroundMu_graph.Draw()

signal1000Mu_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal1000Mu_graph.SetLineColor(ROOT.kBlack)
signal1000Mu_graph.SetMarkerSize(0)
signal1000Mu_graph.Draw("same")

signal250Mu_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal250Mu_graph.SetLineColor(ROOT.kBlue)
signal250Mu_graph.SetMarkerSize(0)
signal250Mu_graph.Draw("same")

canvasTau = ROOT.TCanvas('Tau','')

backgroundTau_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
backgroundTau_graph.SetLineColor(ROOT.kRed)
backgroundTau_graph.SetMarkerSize(0)
backgroundTau_graph.GetXaxis().SetRange(0,1000)
backgroundTau_graph.Draw()

signal1000Tau_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal1000Tau_graph.SetLineColor(ROOT.kBlack)
signal1000Tau_graph.SetMarkerSize(0)
signal1000Tau_graph.Draw("same")

signal250Tau_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal250Tau_graph.SetLineColor(ROOT.kBlue)
signal250Tau_graph.SetMarkerSize(0)
signal250Tau_graph.Draw("same")

canvasMucol = ROOT.TCanvas('Mucol','')

backgroundMucol_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
backgroundMucol_graph.SetLineColor(ROOT.kRed)
backgroundMucol_graph.SetMarkerSize(0)
backgroundMucol_graph.GetXaxis().SetRange(0,1000)
backgroundMucol_graph.Draw()

signal1000Mucol_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal1000Mucol_graph.SetLineColor(ROOT.kBlack)
signal1000Mucol_graph.SetMarkerSize(0)
signal1000Mucol_graph.Draw("same")

signal250Mucol_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal250Mucol_graph.SetLineColor(ROOT.kBlue)
signal250Mucol_graph.SetMarkerSize(0)
signal250Mucol_graph.Draw("same")

canvasTaucol = ROOT.TCanvas('Taucol','')

backgroundTaucol_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
backgroundTaucol_graph.SetLineColor(ROOT.kRed)
backgroundTaucol_graph.SetMarkerSize(0)
backgroundTaucol_graph.GetXaxis().SetRange(0,1000)
backgroundTaucol_graph.Draw()

signal1000Taucol_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal1000Taucol_graph.SetLineColor(ROOT.kBlack)
signal1000Taucol_graph.SetMarkerSize(0)
signal1000Taucol_graph.Draw("same")

signal250Taucol_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Fraction of Events")
signal250Taucol_graph.SetLineColor(ROOT.kBlue)
signal250Taucol_graph.SetMarkerSize(0)
signal250Taucol_graph.Draw("same")

canvasSigBack = ROOT.TCanvas('SigBack','')

sig1000MuOverRootBackground_graph.SetTitle("; Dilepton Mass Cutoff [GeV]; Ratio (arb. units)")
sig1000MuOverRootBackground_graph.SetLineColor(ROOT.kBlue)
sig1000MuOverRootBackground_graph.SetMarkerSize(0)
sig1000MuOverRootBackground_graph.Draw()

sig1000TauOverRootBackground_graph.SetLineColor(ROOT.kRed)
sig1000TauOverRootBackground_graph.SetMarkerSize(0)
sig1000TauOverRootBackground_graph.Draw("same")

sig250MuOverRootBackground_graph.SetLineColor(ROOT.kGreen)
sig250MuOverRootBackground_graph.SetMarkerSize(0)
sig250MuOverRootBackground_graph.Draw("same")

sig250TauOverRootBackground_graph.SetLineColor(ROOT.kBlack)
sig250TauOverRootBackground_graph.SetMarkerSize(0)
sig250TauOverRootBackground_graph.Draw("same")

canvasVisMass = ROOT.TCanvas('VisMass','')

backgroundMu_plot.SetTitle("; M(#tau_{#mu}#tau_{h}); Events/10 GeV")
backgroundMu_plot.SetLineColor(ROOT.kBlack)
backgroundMu_plot.SetMarkerSize(0)
ROOT.gPad.SetLogy()
backgroundMu_plot.Draw()
pdb.set_trace()

signal250Mu_plot.SetLineColor(ROOT.kBlue)
signal250Mu_plot.SetMarkerSize(0)
signal250Mu_plot.Draw("same")

CMS_lumi.lumi_sqrtS = "13TeV"
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.relPosX = 0.12
CMS_lumi.CMS_lumi(canvasMu,0,0)
#CMS_lumi.CMS_lumi(canvasMucol,0,0)
#CMS_lumi.CMS_lumi(canvasTau,0,0)
#CMS_lumi.CMS_lumi(canvasTaucol,0,0)
CMS_lumi.CMS_lumi(canvasVisMass,0,0)

canvasMu.cd()
canvasMu.Update()
canvasMu.RedrawAxis()
frameMu = canvasMu.GetFrame()
frameMu.Draw()

legendMu = ROOT.TLegend(0.65, 0.15, 0.9, 0.35);
legendMu.SetBorderSize(0);
#legend.SetHeader("#tau* mass");
legendMu.AddEntry(signal1000Mu_graph, "Signal 1000 GeV");
legendMu.AddEntry(signal250Mu_graph, "Signal 250 GeV");
legendMu.AddEntry(backgroundMu_graph, "Background #tau_{#mu}#tau_{h}");
#legend.AddEntry(h_2, "1000 GeV", "F");
legendMu.Draw();

canvasMu.Update()
canvasMu.Draw()

canvasMucol.cd()
canvasMucol.Update()
canvasMucol.RedrawAxis()
frameMucol = canvasMucol.GetFrame()
frameMucol.Draw()

legendMucol = ROOT.TLegend(0.7, 0.15, 0.95, 0.35);
legendMucol.SetBorderSize(0);
#legend.SetHeader("#tau* mass");
legendMucol.AddEntry(signal1000Mucol_graph, "Signal 1000 GeV");
legendMucol.AddEntry(signal250Mucol_graph, "Signal 250 GeV");
legendMucol.AddEntry(backgroundMucol_graph, "Background #tau_{#mu}#tau_{h}");
#legend.AddEntry(h_2, "1000 GeV", "F");
legendMucol.Draw();

canvasMucol.Update()
canvasMucol.Draw()

canvasTau.cd()
canvasTau.Update()
canvasTau.RedrawAxis()
frameTau = canvasTau.GetFrame()
frameTau.Draw()

legendTau = ROOT.TLegend(0.6, 0.3, 0.85, 0.5);
legendTau.SetBorderSize(0);
#legend.SetHeader("#tau* mass");
legendTau.AddEntry(signal1000Tau_graph, "Signal 1000 GeV");
legendTau.AddEntry(signal250Tau_graph, "Signal 250 GeV");
legendTau.AddEntry(backgroundTau_graph, "Background #tau_{h}#tau_{h}");
#legend.AddEntry(h_2, "1000 GeV", "F");
legendTau.Draw();

canvasTau.Update()
canvasTau.Draw()

canvasTaucol.cd()
canvasTaucol.Update()
canvasTaucol.RedrawAxis()
frameTaucol = canvasTaucol.GetFrame()
frameTaucol.Draw()

legendTaucol = ROOT.TLegend(0.7, 0.2, 0.95, 0.4);
legendTaucol.SetBorderSize(0);
#legend.SetHeader("#tau* mass");
legendTaucol.AddEntry(signal1000Taucol_graph, "Signal 1000 GeV");
legendTaucol.AddEntry(signal250Taucol_graph, "Signal 250 GeV");
legendTaucol.AddEntry(backgroundTaucol_graph, "Background #tau_{h}#tau_{h}");
#legend.AddEntry(h_2, "1000 GeV", "F");
legendTaucol.Draw();

canvasTaucol.Update()
canvasTaucol.Draw()

canvasSigBack.cd()
canvasSigBack.Update()
canvasSigBack.RedrawAxis()
frameSigBack = canvasSigBack.GetFrame()
frameSigBack.Draw()

legendSigBack = ROOT.TLegend(0.7, 0.15, 0.95, 0.35);
legendSigBack.SetBorderSize(0);
#legend.SetHeader("#tau* mass");
legendSigBack.AddEntry(sig1000MuOverRootBackground_graph, "Signal 1000 GeV (#tau_{#mu}#tau_{h})");
legendSigBack.AddEntry(sig1000TauOverRootBackground_graph, "Signal 1000 GeV (#tau_{h}#tau_{h})");
legendSigBack.AddEntry(sig250MuOverRootBackground_graph, "Signal 250 GeV (#tau_{#mu}#tau_{h})");
legendSigBack.AddEntry(sig250TauOverRootBackground_graph, "Signal 250 GeV (#tau_{h}#tau_{h})");
#legend.AddEntry(h_2, "1000 GeV", "F");
legendSigBack.Draw();

canvasSigBack.Update()
canvasSigBack.Draw()

canvasVisMass.cd()
canvasVisMass.Update()
canvasVisMass.RedrawAxis()
frameVisMass = canvasVisMass.GetFrame()
frameVisMass.Draw()

legendVisMass = ROOT.TLegend(0.6, 0.6, 0.85, 0.8);
legendVisMass.SetBorderSize(0);
#legend.SetHeader("#tau* mass");
legendVisMass.AddEntry(signal250Mu_plot, "Signal 250 GeV");
legendVisMass.AddEntry(backgroundMu_plot, "Embedded Samples");
#legend.AddEntry(h_2, "1000 GeV", "F");
legendVisMass.Draw();

canvasVisMass.Update()
canvasVisMass.Draw()

pdb.set_trace()
save_file = ROOT.TFile("Zdiscrim_photon100.root","RECREATE")
save_file.cd()
signal1000Mu_graph.Write()
signal250Mu_graph.Write()
signal1000Tau_graph.Write()
signal250Tau_graph.Write()
signal1000Mucol_graph.Write()
signal250Mucol_graph.Write()
signal1000Taucol_graph.Write()
signal250Taucol_graph.Write()
backgroundMu_graph.Write()
backgroundTau_graph.Write()
backgroundMucol_graph.Write()
backgroundTaucol_graph.Write()
canvasMu.Write()
canvasTau.Write()
canvasMucol.Write()
canvasTaucol.Write()
canvasSigBack.Write()
canvasVisMass.Write()
save_file.Write()
save_file.Close()
backgroundMuFile.Close()
backgroundTauFile.Close()
signal1000MuFile.Close()
signal1000TauFile.Close()
signal250MuFile.Close()
signal250TauFile.Close()
