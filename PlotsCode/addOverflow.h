#include <TH1D.h>
double addOverflow(TH1D *h)
{
   const int n = h->GetNbinsX();
   const double overflow = h->GetBinContent(n+1);
   h->AddBinContent(n, overflow);
   h->SetBinContent(n+1, 0);
   h->SetBinError(n+1, 0);
   return overflow;
}
