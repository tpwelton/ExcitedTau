#include <iostream>
#include "labelCMS.h"
#include <TH1D.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TChain.h>
#include "addOverflow.h"

void runPoint(TH1D * htemp, const TString var)
{
   //const int n = 3;
   const int n = 2;
   
   std::cout << "doing var: " << var << std::endl; 
   htemp->SetStats(0);
   htemp->SetLineWidth(2);
   //const TString labels[n] = {"250 GeV", "500 GeV", "1000 GeV"};
   //const TString files[n] = {"Taustar_m250", "Taustar_m500", "Taustar_m1000"};
   const TString labels[n] = {"175 GeV", "1000 GeV"};
   const TString files[n] = {"Taustar_m175","Taustar_m1000"};

   TH1D * h[n];
   for (int i = 0; i < n; ++i) {
      std::cout << "running on Taustar m=" << labels[i] << std::endl;
      h[i] = (TH1D*)htemp->Clone("h_"+TString::Itoa(i, 10)+"_"+var);
      TChain c("genVisTauProducer/tree");
      char buffer[100];
      sprintf(buffer, "./mcsamples/%s.root", files[i].Data());
      c.Add(buffer);
      std::cout << c.Project(h[i]->GetName(), var) << " entries in the projection." << std::endl;
      addOverflow(h[i]);
      std::cout << h[i]->Integral() << " is the integral of the histogram." << std::endl;
   }

   TLegend * l = new TLegend(0.25, 0.75, 0.85, 0.85);
   l->SetNColumns(3);
   l->SetHeader("#tau* mass");
   l->SetBorderSize(0);

   TCanvas * canvas = new TCanvas("canvas_"+var, "", 400, 400);
   for (int i = 0; i < n; ++i) {
      h[i]->SetLineColor(i+6);
      h[i]->Scale(1./h[i]->Integral());
      h[i]->Draw("HIST, E, SAME");
      l->AddEntry(h[i], labels[i], "L"); 
   }
   h[0]->SetMinimum(0.001);
   h[0]->SetMaximum(10.);
   canvas->SetLogy();
   l->Draw();
   labelSim(true);
   canvas->SaveAs("./plots/genplots."+var+".pdf");
   std::cout << "" << std::endl;
}

void genPlots()
{
   TH1D * photon_pt = new TH1D("photon_pt", ";photon p_{T} [GeV, truth];events / 50 GeV", 14, 0., 700.);
   runPoint(photon_pt, "photon_pt");

   TH1D * lead_pt = new TH1D("leadvis_pt", ";leading #tau_{vis} p_{T} [GeV, truth];events / 50 GeV", 14, 0., 700.);
   runPoint(lead_pt, "leadvis_pt");

   TH1D * sublead_pt = new TH1D("sublvis_pt", ";subleading #tau_{vis} p_{T} [GeV, truth];events / 50 GeV", 14, 0., 700.);
   runPoint(sublead_pt, "sublvis_pt");
}   

