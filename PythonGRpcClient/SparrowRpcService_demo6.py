

import logging
#import contracts_pb2 
from SparrowRpcService import *
import time

def initialiseSparrow() -> SparrowRpcService:
    sparrow = SparrowRpcService('localhost', 443)
    sparrow.SetPrintInfo(True)
    appVersion = sparrow.GetAppVersion()
    rpcVersion = sparrow.GetRpcVersion() 
    sparrow.SetPrintInfo(False)
    print('Sparrow App Version: ' + appVersion)
    print('Sparrow Rpc version: ' + rpcVersion)
    return sparrow

def CreateImpSpecConfiguration(sparrow: SparrowRpcService):
    sparrow.CreateEmptyConfiguration('demo configuration 6')
    idMuxMap1 = sparrow.CreateMuxMap("MuxMap1", ElectrodePosition.BottomRight)
    idRef1 = sparrow.CreateRefElectrodeMap("Internal", WellReferenceFlag.AllInternal)
    idConfMap1 = sparrow.CreatePixelConfiguration("Map1")

    is_4800 = sparrow.CreateImpSpecFreqConfiguration( ImpSpecFreq.Freq_4800Hz, IStepValues.IStep_2pA, 4)
    is_9600 = sparrow.CreateImpSpecFreqConfiguration( ImpSpecFreq.Freq_9600Hz, IStepValues.IStep_6pA, 3)
    idImpSpec1 = sparrow.CreateImpSpecMode("ImpSpec101", [is_4800, is_9600])

    sparrow.SetPixelConfigurationActive(idConfMap1)
    sparrow.SetPixelModeRow(6, 2, idImpSpec1)
    sparrow.SetPixelModeRow(6, 3, idImpSpec1)

def RunImpSpecMeasurement(sparrow: SparrowRpcService):
    status = sparrow.ScanUSb()
    status = sparrow.GetDeviceConnectionStatus()
    if status:
        print('START Impedance Spectroscopy measurement')
        sparrow.SetPrintInfo(True)
        sparrow.EnableAsic() 

        # sparrow.UploadSettings() 
        # time.sleep(1.0)
        
        result = sparrow.ExecuteImpedanceSpectroscopy()
        print(result)

        sparrow.DisableAsic() 
        sparrow.SetPrintInfo(False)
        print('END Impedance Spectroscopy measurement')
    else:
        print('Device is NOT Connected')
        print('Batch Session cannot be started')

def run():
    print('\n\nSparrow Device DEMO 6: Impedance Spectroscopy')
    sparrow = initialiseSparrow()
    CreateImpSpecConfiguration(sparrow)
    RunImpSpecMeasurement(sparrow)



if __name__ == '__main__':
    logging.basicConfig()
    run()