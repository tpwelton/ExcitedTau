# ExcitedTau
This is a repository where I keep my code for the Excited Tau analysis.

The preliminary processing uses https://github.com/cms-nanoAOD/nanoAOD-tools with some extra personal files added in. The NanoAODTools are part of CMSSW (CMS Software), so the files I added in are integrated into that structure, so the files in NanoAODTools_copy/ are hard-linked to the files in that structure that I added. The most important is KeepAllEventSelection.py, which should be added as a module in NanoAODTools by putting the file in $CMSSW_BASE/src/PhysicsTools/NanoAODTools/python/postprocessing/modules/ExcitedTau. I recommend putting any modules you want to run using CRAB3 (grid processing) in this location. For using crab, the configuration and scripts I use to run those jobs is in NanoAODTools_copy/crab. The real place to put them in your file system is $CMSSW_BASE/src/PhysicsTools/NanoAODTools/crab.

Crab jobs produce many files in an output dataset, which you can find on https://cmsweb.cern.ch/das. You must have a grid certificate installed in your (Firefox) browser to access CMS DAS. You can also aggregate the output of your job using a shell command:
  
  dasgoclient -query="file dataset=/nameOfDataset/On/DAS instance=prod/phys03" >> output_file.txt
  
If you are querying files that are centrally produced datasets (like MC), then those are likely on the global instance of the database and you can leave out the "instance=prod/phys03" part of the query. The name of the dataset that you produced using crab can be found by typing the command "crab status /nameOfJobDirectory" and looking for the Output Dataset.

The meat of the postprocessing happens in Processed_NanoAOD. The current files doing the plotting are MCSignal.py for Taustar signal files and Sideband.py for the embedded samples and background MC when applicable. I use the dasgoclient query command to make text files of all the files I want the postprocessing scripts to run over. The lists of files can be found in the associated year folder in Processed_NanoAOD. The postprocessing files are written in PyROOT, which takes the ROOT language that particle physicists use and wraps it in python to make it easier to write and to use. 
