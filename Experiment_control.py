## This function will run the experiment protocol

# imports
import time
#FIXMEfrom Sparrow_com import *
from SimulatedTrace import *
import matplotlib.pyplot as plt
import matplotlib
from Calculations_functions import *

# this class should hold functions to do the following:
# 1. Generate the sparrow configuration based on the yaml files
# 2. Stop the acquistion of data from sparrow
# 3. Run the acquistion protocol (threaded)
# 4. Run the calculations and visulaization based on the recorded data
#matplotlib.use('macosx')
#matplotlib.use('Qt5Agg')


class ExperimentControl:
    def __init__(self, experiment_gui):
        # Should read the yaml files and generate the sparrow configuration
        # what info is needed from the main GUI?
        self.GUI = experiment_gui
        #FIXME#self.cfg_basline = 'baseline'
        #FIXME#self.cfg_experiment = 'experiment'
        #FIXME self.sparrow = initialiseSparrow()
        self.chip_number ='SP101'#self.sparrow.ReadChipID()

    def get_comm(self):
        #FIXMEself.sparrow.SetPrintInfo(True)
        appVersion = '1.0'#FIXMEself.sparrow.GetAppVersion()
        rpcVersion = '2.0'#FIXMEself.sparrow.GetRpcVersion() 
        #FIXMEself.sparrow.SetPrintInfo(False)
        self.sparrow = 10 # FIXMEplace holder for simulation
        self.GUI.log_message(f'Sparrow App Version: {appVersion}')
        self.GUI.log_message(f'Sparrow Rpc version: {rpcVersion}')

    def generate_sparrow_cfg(self):
        #TODO This function should read the yaml files and generate the sparrow configuration
        # Create a sparrow class object with the configuration from the yaml files and the cfg name 
        pass

    def run_basleine(self,stop_acq):
        baseline_runtime = 1/60 # in minutes
        baseline_runtime = int(baseline_runtime * 6); # convert to seconds 
        # This function should run the baseline acquistion
        # choose the basline configuration in the sparrow class
        #FIXMEself.sparrow.SetConfigurationActive(self.cfg_basline)
        # Actviate chip
        #FIXMEself.sparrow.EnableAsic()
        # upload configurations to chip
        #FIXMEself.sparrow.UploadSettings()
        # start batch acquistion
        #FIXMEself.sparrow.StartBatchRun()
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
                #FIXMEself.sparrow.DisableAsic()
                break
        # move file to storage path
        
        # deactivate chip
        #FIXMEself.sparrow.DisableAsic()
        

    def run_preExperiment_stimulation(self):
        #self.sparrow.SetConfigurationActive(self.cfg_experiment)
        # Actviate chip
        #FIXMEself.sparrow.EnableAsic()
        # upload configurations to chip
        #FIXMEself.sparrow.UploadSettings()
        #start batch acquistion
        #FIXMEself.sparrow.StartBatchRun()

        #TODO This is the stimulation of running the experiment
        vector = Single_electrode(20,80)
        self.GUI.plot_queue.put(('preExp',vector))
        time.sleep(5)
        
            


        

    def run_Experiment_stimulation(self,stop_acq):
        #TODO This function should run the experiment acquistion 

        # choose the experiment configuration in the sparrow class

        # Actviate chip

        # upload configurations to chip

        # Run the batch in iteration with the right timings and monitor reaching the criteria

        #TODO simulation of running the experiment
        for iteration in range(30):
            if not stop_acq.is_set():
                criteria_count = []
                repition_number = 3000;
                for t in range(repition_number):
                    if stop_acq.is_set():
                        break
                    vector = Single_electrode(t,iteration)
                    if self.GUI.experiment_type.get() == 'Control':
                        vector = Single_electrode(0,75)
                    yaml_path = self.GUI.yaml_recording.get()
                    event_in_time = check_crossing(yaml_path, vector)
                    # calculate if has a threshold crossing event at 40-60ms after the stimulation
                    if len(criteria_count) >= 10:
                        criteria_count.pop(0)
                    criteria_count.append(event_in_time)
                    criteria_count_np = np.array(criteria_count).sum()
                    if criteria_count_np/10 >= self.GUI.criterion.get()/10:
                        self.GUI.log_message(f'Criteria reached after {t} seconds')
                        data = [iteration, t]
                        self.GUI.plot_queue.put(('experiment',data))
                        break
                    elif t == repition_number - 1:
                        self.GUI.log_message('Criteria not reached in time')
                time.sleep(1)
            else:
                self.stop_acquistion()
                time.sleep(0.5)
                self.GUI.log_message('Experiment stopped')
                break           
        

    def stop_acquistion(self):
        #TODO This function should stop the acquistion of data from sparrow
        pass
    


        

            