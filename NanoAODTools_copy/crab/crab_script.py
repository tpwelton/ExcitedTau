#!/usr/bin/env python
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import * 

#this takes care of converting the input files from CRAB
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

from  PhysicsTools.NanoAODTools.postprocessing.modules.ExcitedTau.EventSelection import event_selection_min#,signalCollinearCheck
p=PostProcessor(".",inputFiles(),cut=None,modules=[event_selection_min()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())#,signalCollinearCheck()],provenance=True,fwkJobReport=True,jsonInput=runsAndLumis())
p.run()

print "DONE"

