#!/usr/bin/python
import time
import logging
import contracts_pb2
from SparrowRpcService import *

def initialiseSparrow() -> SparrowRpcService:
    sparrow = SparrowRpcService('localhost', 443)
    sparrow.SetPrintInfo(True)
    appVersion = sparrow.GetAppVersion()
    rpcVersion = sparrow.GetRpcVersion() 
    sparrow.SetPrintInfo(False)
    print('Sparrow App Version: ' + appVersion)
    print('Sparrow Rpc version: ' + rpcVersion)
    return sparrow

def CreateTestConfiguration(sparrow: SparrowRpcService):
    sparrow.CreateEmptyConfiguration('demo configuration 3')

    idRef3 = sparrow.CreateRefElectrodeMap("RefElectrodeMap1", WellReferenceFlag.Internal1|WellReferenceFlag.Internal3|WellReferenceFlag.Internal5|WellReferenceFlag.Internal7)
    sparrow.CreateRefElectrodeMap('sdf', WellReferenceFlag.Internal0|WellReferenceFlag.Internal1)

    id1 = sparrow.CreateMuxMap("MuxMap1", ElectrodePosition.BottomRight)

    vStim1Id = sparrow.CreateVStimMode("VStim1", 10,-10,5,5,50)
    vStim2Id = sparrow.CreateVStimMode("VStim2", 25,-25,50,50,150)
    iStim1Id = sparrow.CreateIStimMode("IStim1", IStepValues.IStep_2pA, 40,-40,15,15,200)
    iStim2Id = sparrow.CreateIStimMode("IStim2", IStepValues.IStep_2pA, 30,-30,35,35,200)
    rec1Id = sparrow.CreateRecMode("Rec1", True, RecGain.Gain1)
    rec12d = sparrow.CreateRecMode("Rec2", True, RecGain.Gain5)

    idConfMap1 = sparrow.CreatePixelConfiguration("Map1")

    st = sparrow.SetPixelMode(1, rec1Id)
    st = sparrow.SetPixelMode(2, vStim1Id)
    st = sparrow.SetPixelMode(6, iStim1Id)

    for x in range(100):
        st = sparrow.SetPixelMode(x+1025, vStim1Id)
    st = sparrow.SetPixelModeRange(1125, 1225, vStim2Id)

    st = sparrow.SetPixelModeWell(9, vStim2Id)
    st = sparrow.SetPixelModeRow(6, 2, vStim2Id)
    st = sparrow.SetPixelModeRow(6, 3, rec1Id)
    for x in range(1,16,2):
        st = sparrow.SetPixelModeColumn(4, x, vStim2Id)
        st = sparrow.SetPixelModeColumn(4, x+1, rec1Id)
   
    st = sparrow.SetPixelModeRange(3585, 3712, rec1Id)
    return idConfMap1

def RunManualRecording(sparrow: SparrowRpcService):

    status = sparrow.GetDeviceConnectionStatus()
    if status:
        print('START Manual Recording session')
        sparrow.EnableAsic() 
        sparrow.UploadSettings() 
        time.sleep(1.0)
        sparrow.StartAcquisition() 
        time.sleep(2.0)
        sparrow.StartStimulationSequence(10,PulsePolarity.NegativePulseFirst, True, False)
        sparrow.StartImpedanceMonitoring(ImpMonFrequency.Frequency10kHz, ImpMonAmplitude.Amplitude10nA)
        time.sleep(5.0)
        sparrow.StopImpedanceMonitoring()
        sparrow.StopAcquisition()
        time.sleep(1.0)
        sparrow.DisableAsic() 
        print('END Manual Recording session')
    else:
        print('Device is NOT Connected')
        print('Manual Recording cannot be started')

    info =  sparrow.GetErrorInfo(0)
    if len(info)>0:
        print (info[0].functionName)
        print (info[0].errorDescription)
    else:
        print ("No errors occurred.")

def run():
    print('\n\nSparrow Device DEMO 3')
    sparrow = initialiseSparrow()
    CreateTestConfiguration(sparrow)
    RunManualRecording(sparrow)


if __name__ == '__main__':
    logging.basicConfig()
    run()