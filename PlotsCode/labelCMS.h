#include <TPaveText.h>

void labelSim(const bool showlumi=false)
{
   TPaveText * label0 = new TPaveText(0.49, .905, 0.89, .945, "NDC, NB");
   label0->SetFillColor(0);
   label0->SetTextAlign(31);
   char buffer[100];
   if (showlumi) {
      sprintf(buffer, "Simulation 2018   13 TeV");
   } else {
//      sprintf(buffer, "Simulation 2018   13 TeV               ");
       sprintf(buffer, "Simulation    13 TeV");
   }
   label0->AddText(buffer);
   label0->Draw();
}

