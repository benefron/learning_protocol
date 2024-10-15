## This function will run the experiment protocol

# imports
import time
#from Sparrow_com import *
from SimulatedTrace import *
import matplotlib.pyplot as plt
import matplotlib

# this class should hold functions to do the following:
# 1. Generate the sparrow configuration based on the yaml files
# 2. Stop the acquistion of data from sparrow
# 3. Run the acquistion protocol (threaded)
# 4. Run the calculations and visulaization based on the recorded data
#matplotlib.use('macosx')
matplotlib.use('TkAgg')


class ExperimentControl:
    def __init__(self, experiment_gui):
        # Should read the yaml files and generate the sparrow configuration
        # what info is needed from the main GUI?
        self.GUI = experiment_gui
        #self.cfg_basline = 'baseline'
        #self.cfg_experiment = 'experiment'
        # self.sparrow = initialiseSparrow()
        self.chip_number ='SP101'#self.sparrow.ReadChipID()

    def get_comm(self):
        #self.sparrow.SetPrintInfo(True)
        appVersion = '1.0'#self.sparrow.GetAppVersion()
        rpcVersion = '2.0'#self.sparrow.GetRpcVersion() 
        #self.sparrow.SetPrintInfo(False)
        self.sparrow = 10 # place holder for simulation
        self.GUI.log_message('Sparrow App Version: ' + appVersion)
        self.GUI.log_message('Sparrow Rpc version: ' + rpcVersion)

    def generate_sparrow_cfg(self):
        # This function should read the yaml files and generate the sparrow configuration
        # Create a sparrow class object with the configuration from the yaml files and the cfg name 
        pass

    def run_basleine(self,stop_acq):
        baseline_runtime = 1/60 # in minutes
        baseline_runtime = int(baseline_runtime * 6); # convert to seconds 
        # This function should run the baseline acquistion
        # choose the basline configuration in the sparrow class
        #self.sparrow.SetConfigurationActive(self.cfg_basline)
        # Actviate chip
        #self.sparrow.EnableAsic()
        # upload configurations to chip
        #self.sparrow.UploadSettings()
        # start batch acquistion
        #self.sparrow.StartBatchRun()
        # wait until acquisition is done
        for i in range(baseline_runtime):
            if not stop_acq.is_set():
                time.sleep(1)
                k = 1
                if i % 60 == 0:
                    self.GUI.log_message(f'{k} minutes have passed')
                    k = k+1
            else:
                self.stop_acquistion()
                time.sleep(0.5)
                self.GUI.log_message('Baseline acquisition stopped')
                # Deactivate chip
                #self.sparrow.DisableAsic()
                break
        # move file to storage path
        
        # deactivate chip
        #self.sparrow.DisableAsic()
        

    def run_preExperiment_stimulation(self):
        #self.sparrow.SetConfigurationActive(self.cfg_experiment)
        # Actviate chip
        #self.sparrow.EnableAsic()
        # upload configurations to chip
        #self.sparrow.UploadSettings()
        #start batch acquistion
        #self.sparrow.StartBatchRun()

        # This is the stimulation of running the experiment
        for i in range(30):
            matrix = vector_to_matrix(30)
            # calculate if has a threshold crossing event at 40-60ms after the stimulation
            


        

    def run_preExperiment_stimulation(self):
        # This function should run the experiment acquistion 

        # choose the experiment configuration in the sparrow class

        # Actviate chip

        # upload configurations to chip

        # Run the batch in iteration with the right timings and monitor reaching the criteria

        pass

    def stop_acquistion(self):
        # This function should stop the acquistion of data from sparrow
        pass
    


        

            