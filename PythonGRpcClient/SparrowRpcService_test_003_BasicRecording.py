

import contracts_pb2
from SparrowRpcService import *
import time
import logging

def initialiseSparrow() -> SparrowRpcService:
    sparrow = SparrowRpcService('localhost', 443)
    sparrow.SetPrintInfo(True)
    appVersion = sparrow.GetAppVersion()
    rpcVersion = sparrow.GetRpcVersion() 
    sparrow.SetPrintInfo(False)
    print('Sparrow App Version: ' + appVersion)
    print('Sparrow Rpc version: ' + rpcVersion)
    return sparrow

def CreateBatchScript(sparrow: SparrowRpcService):
    sparrow.CreateEmptyConfiguration('demo configuration 4')
    
    ifRec1 = sparrow.CreateRecMode("Rec1", True, RecGain.Gain10)
    idVStim1 = sparrow.CreateVStimMode("VStim107", 10,-10,5,5,50)

    prog1Id = sparrow.CreateBatchProgram("prog 1")
    status = sparrow.SetBatchProgramActive(prog1Id)
    idConfMap8 = sparrow.CreatePixelConfiguration("Map3")
    st = sparrow.SetPixelModeRow(6, 2, idVStim1)
    st = sparrow.SetPixelModeRow(6, 3, idVStim1)
    idConfMap9 = sparrow.CreatePixelConfiguration("Map9")
    st = sparrow.SetPixelModeWell(5, idVStim1)
    sparrow.SetPixelConfigurationActive(idConfMap8)
    st = sparrow.SetPixelModeRow(6, 1, ifRec1)
    st = sparrow.SetPixelModeRow(6, 4, ifRec1)
    sparrow.SetPixelConfigurationActive(idConfMap9)
    st = sparrow.SetPixelModeRow(5, 1, ifRec1)
    st = sparrow.SetPixelModeRow(5, 16, ifRec1)

    idSweepCfgMap1 = sparrow.CreateBatchSweepCfgMap([idConfMap8, idConfMap9], False, prog1Id)

    idMuxMap10 = sparrow.CreateMuxMap("MuxMap10", ElectrodePosition.BottomRight)
    idMuxMap11 = sparrow.CreateMuxMap("MuxMap11", ElectrodePosition.E1)
    idSweepMuxMap2 = sparrow.CreateBatchSweepMuxMap([idMuxMap10, idMuxMap11], idSweepCfgMap1)

    idRef1 = sparrow.CreateRefElectrodeMap("Internal", WellReferenceFlag.AllInternal)
    idRef2 = sparrow.CreateRefElectrodeMap("External", WellReferenceFlag.External)
    idSweepRefMap1 = sparrow.CreateBatchSweepRefMap([idRef1, idRef2], idSweepMuxMap2)  

 

    rec10 = sparrow.CreateRecConfigurationObject(
        name='Rec10', 
        enableLowPassFilter=True, gain=RecGain.Gain5 )
    rec11 = sparrow.CreateRecConfigurationObject(
        name='Rec11', 
        enableLowPassFilter=True, gain=RecGain.Gain10 )
    idRecSweepSettings1 = sparrow.CreateBatchSweepRec(ifRec1, [rec10, rec11], idSweepRefMap1);

    tl6 = sparrow.CreateTimeLine(idRecSweepSettings1)
    idTlr1 = sparrow.CreateTimelineRepeat(5, tl6)

    sparrow.CreateTimeLineDelay(1000, idTlr1)
    sparrow.CreateTimeLineStimulationEvent(StimulationMode.Voltage, PulsePolarity.NegativePulseFirst, 10, idTlr1)
    idIm1 = sparrow.CreateTimelineImpedanceMonitor(ImpMonFrequency.Frequency1kHz, ImpMonAmplitude.Amplitude1nA, idTlr1)
    sparrow.CreateTimeLineDelay(3500, idIm1)
    idSd1 = sparrow.CreateTimelineSliceDefinition([Processor.Avg], idTlr1)
    sparrow.CreateTimeLineDelay(1000, idSd1)


def RunBatchScript(sparrow: SparrowRpcService):
    status = sparrow.ScanUSb()
    status = sparrow.GetDeviceConnectionStatus()
    if status:
        print('START Batch Recording session')
        sparrow.EnableAsic() 
        sparrow.UploadSettings() 
        time.sleep(1.0)
        
        # sparrow.StartBatchRun() 
        # time.sleep(10.0)
        # print('stop session after 10s')
        # sparrow.StopAcquisition()
        sparrow.ExecuteBatchRun()

        time.sleep(1.0)
        sparrow.DisableAsic() 
        print('END Batch Recording session')
    else:
        print('Device is NOT Connected')
        print('Batch Session cannot be started')


def run():
    print('\n\nSparrow Device TEST 001: SwitchBatchProg')
    sparrow = initialiseSparrow()
    CreateBatchScript(sparrow)
    RunBatchScript(sparrow)


if __name__ == '__main__':
    logging.basicConfig()
    run()