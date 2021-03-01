def passTrigger(event,channel):
    if channel == 6:
      if not(event.HLT_IsoMu24 or event.HLT_IsoMu27): return False
      else: return True
    if hasattr(event,"HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg"): return trigger2017(event,channel)
    if hasattr(event,"HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg"): return triggerV6(event,channel)
    if hasattr(event,"HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg"): return triggerDataV7(event,channel)
    return triggerDefault(event,channel)

def triggerV6(event,channel):
    if channel == 4:
      return event.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg
    if channel == 6:
      return event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1

def triggerDataV7(event,channel):
    if channel == 4:
      return event.HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg
    if channel == 6:
      return event.HLT_IsoMu19_eta2p1_LooseCombinedIsoPFTau20

def trigger2017(event,channel):
    if channel == 4:
      return event.HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg
    if channel == 6:
      return event.HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1

def triggerDefault(event,channel):
    if channel == 4:
      return event.HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg
    if channel == 6:
      return True
