#include <TCut.h>
#include <TLegend.h>
#include "labelCMS.h"
#include <TPaveText.h>
#include <TH1D.h>
#include <TCanvas.h>
#include <TChain.h>
#include "addOverflow.h"

void runPoint(const TString t1, const TString t2, const TString dmtag, const TString label, const int genselect=0)
{
   const TString infile = "./mcsamples/DYJetsToLL_Zpt150.root";

   TChain tree(t1); tree.Add(infile);
   TChain tree2(t2); tree2.Add(infile); tree.AddFriend(&tree2);
   TChain tree3("eventAnalyzer/tree"); tree3.Add(infile); tree.AddFriend(&tree3);
   TChain tree4("genVisTauProducer/tree"); tree4.Add(infile); tree.AddFriend(&tree4);

   char hvisname[100]; sprintf(hvisname, "h_vis_%s", dmtag.Data());
   TH1D * h_vis = new TH1D(hvisname, ";mass [GeV];events / 10 GeV", 25, 0., 250.);
   h_vis->SetStats(0);
   h_vis->SetLineWidth(2);
   char hcolname[100]; sprintf(hcolname, "h_col_%s", dmtag.Data());
   TH1D * h_col = (TH1D*)h_vis->Clone(hcolname);
   h_vis->SetLineStyle(2);
 
   char cuts[100];
   sprintf(cuts, "xsWeight * 59740. * (havePair && nTaus_gen>=2)");
   
   tree.Project(h_vis->GetName(), "ll_mass", cuts);
   addOverflow(h_vis);
   tree.Project(h_col->GetName(), "ll_collinearmass", cuts);
   addOverflow(h_col);
   
   TCanvas * canvas = new TCanvas("canvas_"+dmtag, label, 400, 400);
   h_vis->Draw("HIST, E");
   h_col->Draw("HIST, E, SAME");
   h_vis->SetMinimum(0.);
   h_vis->SetMaximum(1.1 * TMath::Max(h_vis->GetMaximum(), h_col->GetMaximum()));

   TPaveText * label0 = new TPaveText(0.65, 0.75, 0.875, 0.875, "NDC, NB");
   label0->SetFillColor(0);
   label0->SetTextAlign(31);
   label0->AddText(label);
   label0->Draw();

   TLegend * l = new TLegend(0.6, 0.6, 0.875, 0.75);
   l->SetBorderSize(0);
   l->AddEntry(h_vis, "visible mass", "L");
   l->AddEntry(h_col, "collinear mass", "L");
   l->Draw();

   labelSim("true");
   char savebuffer[100];
   if (genselect) {
      sprintf(savebuffer, "./plots/recomass.DYJetsToLL_Zpt150.%s.gen%d.pdf", dmtag.Data(), genselect);
   } else {
      sprintf(savebuffer, "./plots/recomass.DYJetsToLL_Zpt150.%s.pdf", dmtag.Data());
   }
   canvas->SaveAs(savebuffer);
}

void recoZMass()
{
   runPoint("osMuTauPairAnalyzer/tree", "osMuTauPairProducer/tree", "mutau", "#tau_{#mu} + #tau_{h}", 4);
   runPoint("osETauPairAnalyzer/tree", "osETauPairProducer/tree", "etau", "#tau_{e} + #tau_{h}", 5);
   runPoint("osTauTauPairAnalyzer/tree", "osTauTauPairProducer/tree", "tautau", "#tau_{h} + #tau_{h}", 6);
}

