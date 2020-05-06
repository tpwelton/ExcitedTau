#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ExcitedTau.ChannelAnalyzer import channel_tautau
postfix = "_chan4_tight"
p=PostProcessor(".",inputFiles(),modules=[channel_tautau()],provenance=True,fwkJobReport=True,postfix=postfix,jsonInput=runsAndLumis())
p.run()


