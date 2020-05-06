#include <iostream>
#include <TCanvas.h>
#include <TCut.h>
#include <TLegend.h>
#include <TChain.h>
#include <TGraphErrors.h>
#include "labelCMS.h"

void SignalEff()
{
   const TCut cuts_num = "haveTriplet && nBJets[2]==0 && ll_mass>=100.";
   const TCut cuts_denom[3] = {"dm==6", "dm==5", "dm==4"};
   //const TCut cuts_denom[3] = {"1>0", "1>0", "1>0"};

   const int n = 12;
   const double mass[n] = {250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000};

   const TString AnalyzerNames[3] = {"osTauTauPairAnalyzer", "osETauPairAnalyzer", "osMuTauPairAnalyzer"};
   const TString ProducerNames[3] = {"osTauTauPairProducer", "osETauPairProducer", "osMuTauPairProducer"};   
   TGraphErrors * g[3];

   for (int i = 0; i < 3; ++i) {
      g[i] = new TGraphErrors(n);
      g[i]->SetMarkerStyle(20);
      g[i]->SetMarkerColor(6+i);
      g[i]->SetLineColor(6+i);
      for (int j = 0; j < n; ++j) {
         TChain chain(AnalyzerNames[i]+"/tree");
         char buffer[100];
         sprintf(buffer, "./mcsamples/Taustar_m%d.root", int(mass[j]));
         chain.Add(buffer);
         std::cout << chain.GetEntries() << " entries in signal m = " << mass[j] << std::endl;
         TChain chain2(ProducerNames[i]+"/tree"); chain2.Add(buffer); chain.AddFriend(&chain2);
         TChain chain3("eventAnalyzer/tree");     chain3.Add(buffer); chain.AddFriend(&chain3);
         TChain chain4("genVisTauProducer/tree"); chain4.Add(buffer); chain.AddFriend(&chain4);
         const double denom = chain.GetEntries(cuts_denom[i]);
         double eff = 0.;
         double err = 0.;
         if (denom>0) {
            const double num = chain.GetEntries(cuts_num && cuts_denom[i]);
            eff = num/denom;
            err = sqrt(denom*eff*(1.-eff));
            err = err/denom;
         }
         g[i]->SetPoint(j, mass[j], eff);
         g[i]->SetPointError(j, 0., err);
      }
   }

   TCanvas * canvas = new TCanvas("canvas", "", 400, 400);
   g[0]->Draw("APE");
   g[0]->SetMinimum(0.);
   g[0]->SetMaximum(0.5);
   g[0]->SetTitle(";#tau* mass [GeV, truth];signal efficiency");
   g[1]->Draw("PE, SAME");
   g[2]->Draw("PE, SAME");

   TLegend *l = new TLegend(0.6, 0.175, 0.875, 0.4);
   l->SetBorderSize(0);
   l->AddEntry(g[2], "#tau_{#mu} + #tau_{h}", "P");
   l->AddEntry(g[1], "#tau_{e} + #tau_{h}", "P");
   l->AddEntry(g[0], "#tau_{h} + #tau_{h}", "P");
   l->Draw();

   labelSim(true);

   canvas->SaveAs("./plots/signaleff.fixedgenchannel.pdf");
   //canvas->SaveAs("./plots/signaleff.inclusivechannel.pdf");
}

