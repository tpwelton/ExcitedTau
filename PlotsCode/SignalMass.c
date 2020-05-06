#include <iostream>
#include <TAxis.h>
#include <TLegend.h>
#include <TPaveText.h>
#include <TChain.h>
#include <TCanvas.h>
#include <TCut.h>
#include <TGraph.h>
#include "labelCMS.h"

TGraph * runPoint(const TString infile, const TString tree, const TString tag, const TString label)
{
   const TCut baselineCuts = "haveTriplet==1 && m_ll>=100. && BTags[2]==0";

   char fileBuffer[100];
   sprintf(fileBuffer, "./mcsamples/%s.root", infile.Data());
   
   TChain chain("eventAnalyzer/tree");
   chain.Add(fileBuffer);

   TChain chain1(tree);
   chain1.Add(fileBuffer);
   chain.AddFriend(&chain1);
 
   bool haveTriplet = false;
   int nBJets[3] = {0, 0, 0};
   double ll_mass = 0.;
   double collmass_glead = 0.;
   double collmass_gsublead = 0.;
   double m_lead = 0.;
   double m_sublead = 0.;
   chain.SetBranchAddress("haveTriplet", &haveTriplet);
   chain.SetBranchAddress("nBJets", nBJets);
   chain.SetBranchAddress("ll_mass", &ll_mass);
   chain.SetBranchAddress("gtau_cmass", &collmass_glead);
   chain.SetBranchAddress("glepton_cmass", &collmass_gsublead);
   //chain.SetBranchAddress("m_lead", &m_lead);
   //chain.SetBranchAddress("m_sublead", &m_sublead);
   
   char cuts[100];
   //sprintf(cuts, "haveTriplet==1 && nBJets[2]==0 && ll_mass>=100.");
   sprintf(cuts, "haveTriplet==1");
   const int ntot = chain.GetEntries(cuts);
   double minmass[ntot], maxmass[ntot];

   std::cout << "entries in the chain: " << chain.GetEntries() << std::endl;
   std::cout << "entries after selection: " << ntot << std::endl;

   int n = 0;
   for (int i = 0; i < chain.GetEntries(); ++i) {
      chain.GetEntry(i);
      if (haveTriplet && nBJets[2]==0 && ll_mass>=100.) {
         minmass[n] = TMath::Min(collmass_glead, collmass_gsublead);
         maxmass[n] = TMath::Max(collmass_glead, collmass_gsublead);
   //      minmass[n] = TMath::Min(m_lead, m_sublead);
     //    maxmass[n] = TMath::Max(m_lead, m_sublead);
         ++n;
      }
   }

   TGraph *g = new TGraph(ntot, minmass, maxmass);
   char axislabels[100];
   sprintf(axislabels, ";min mass(%s, #tau_{h}, #gamma) [GeV];max mass(%s, #tau_{h}, #gamma) [GeV]", label.Data(), label.Data());
   g->SetTitle(axislabels);

   return g;
}

void doDouble(const TString tree, const TString tag, const TString who)
{
   TGraph * h_1 = runPoint("Taustar_m175", tree, tag, who);
   TGraph * h_2 = runPoint("Taustar_m1000", tree, tag, who);
   //TGraph * h_1 = runPoint("DYJetsToLL_Zpt150", tree1, tree2, tag, who);
   //TGraph * h_2 = runPoint("DYJetsToLL_Zpt150", tree1, tree2, tag, who);

   char buffername[100];
   sprintf(buffername, "can_%s", tag.Data());
   TCanvas * can = new TCanvas(buffername, buffername, 400, 400);
   
   h_1->SetMarkerColor(8);
   h_1->SetMarkerStyle(7);
   h_1->SetFillColor(8);
   h_1->Draw("AP");
   h_1->SetMinimum(0.);
   h_1->SetMaximum(2000.);
   h_1->GetXaxis()->SetRangeUser(0., 2000.);
   h_1->Draw("AP");
   can->Update();

   h_2->SetMarkerColor(9);
   h_2->SetMarkerStyle(7);
   h_2->SetFillColor(9);
   h_2->Draw("P, SAME");

   TLegend * l = new TLegend(0.6, 0.2, 0.85, 0.5);
   l->SetBorderSize(0);
   l->SetHeader("#tau* mass");
   l->AddEntry(h_1, "175 GeV", "F");
   l->AddEntry(h_2, "1000 GeV", "F");
   l->Draw();

   labelSim(true);

   //TPaveText * label0 = new TPaveText(0.2, .905, 0.4, .945, "NDC, NB");
   //label0->SetFillColor(0);
   //label0->SetTextAlign(31);
   //label0->AddText(label);
   //label0->Draw();
   can->SaveAs("./plots/signalsum.2masscollinear."+tag+".pdf");
}

void SignalMass()
{
   doDouble("osMuTauChannel/tree", "mutau", "#tau_{#mu}");
   doDouble("osETauChannel/tree", "etau", "#tau_{e}");
   doDouble("osTauTauChannel/tree", "tautau", "#tau_{h}");
}
