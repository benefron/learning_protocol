## This function will run the experiment protocol

# imports
import time
#from Sparrow_com import *

# this class should hold functions to do the following:
# 1. Generate the sparrow configuration based on the yaml files
# 2. Stop the acquistion of data from sparrow
# 3. Run the acquistion protocol (threaded)
# 4. Run the calculations and visulaization based on the recorded data



class ExperimentControl:
    def __init__(self, experiment_gui):
        # Should read the yaml files and generate the sparrow configuration
        # what info is needed from the main GUI?
        self.GUI = experiment_gui
        self.cfg_basline = 'baseline'
        self.cfg_experiment = 'experiment'
        self.sparrow = 10#initialiseSparrow()
        self.chip_number ='SP101'#self.sparrow.ReadChipID()

    def get_comm(self):
        #self.sparrow.SetPrintInfo(True)
        appVersion = '1.0'#self.sparrow.GetAppVersion()
        rpcVersion = '2.0'#self.sparrow.GetRpcVersion() 
        #self.sparrow.SetPrintInfo(False)
        self.GUI.log_message('Sparrow App Version: ' + appVersion)
        self.GUI.log_message('Sparrow Rpc version: ' + rpcVersion)

    def generate_sparrow_cfg(self):
        # This function should read the yaml files and generate the sparrow configuration
        # Create a sparrow class object with the configuration from the yaml files and the cfg name 
        pass

    def run_basleine(self):
        # This function should run the baseline acquistion
        pass

    def run_experiment(self, choose_electrode):
        # This function should run the experiment acquistion should return chossen electrode numer if True
        pass
    def stop_acquistion(self):
        # This function should stop the acquistion of data from sparrow
        pass
    


        

            