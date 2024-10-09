
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

def CreateBatchScript(sparrow: SparrowRpcService):
    sparrow.CreateEmptyConfiguration('demo configuration 4')

    prog1Id = sparrow.CreateBatchProgram("prog 1")
    prog2Id = sparrow.CreateBatchProgram("prog 2")
    status = sparrow.SetBatchProgramActive(prog1Id)

    idConfMap8 = sparrow.CreatePixelConfiguration("Map8")
    idConfMap9 = sparrow.CreatePixelConfiguration("Map9")
    idSweepCfgMap1 = sparrow.CreateBatchSweepCfgMap([idConfMap8, idConfMap9], False, prog1Id)

    
    idMuxMap10 = sparrow.CreateMuxMap("MuxMap10", ElectrodePosition.BottomRight)
    idMuxMap11 = sparrow.CreateMuxMap("MuxMap11", ElectrodePosition.E1)
    idSweepMuxMap1 = sparrow.CreateBatchSweepMuxMap([idMuxMap10, idMuxMap11], prog1Id)
    idSweepMuxMap2 = sparrow.CreateBatchSweepMuxMap([idMuxMap10, idMuxMap11], idSweepCfgMap1)

    idRef1 = sparrow.CreateRefElectrodeMap("Internal", WellReferenceFlag.AllInternal)
    idRef2 = sparrow.CreateRefElectrodeMap("External", WellReferenceFlag.External)
    idSweepRefMap1 = sparrow.CreateBatchSweepRefMap([idRef1, idRef2], idSweepMuxMap2)

    idVStim1 = sparrow.CreateVStimMode("VStim107", 10,-10,5,5,50)
    sparrow.SetPixelConfigurationActive(idConfMap8)
    st = sparrow.SetPixelModeRow(6, 2, idVStim1)
    st = sparrow.SetPixelModeRow(6, 3, idVStim1)
    sparrow.SetPixelConfigurationActive(idConfMap9)
    st = sparrow.SetPixelModeWell(5, idVStim1)
  
    v1 = sparrow.CreateVStimConfigurationObject(
        name = 'V1', 
        pulse1VoltagemV = 22, pulse2VoltagemV = 22, 
        pulse1DurationmS = 10, pulse2DurationmS = 10, pulseTotalDurationmS = 40)
    v2 = sparrow.CreateVStimConfigurationObject(
        name = 'V1', 
        pulse1VoltagemV = 33, pulse2VoltagemV = 33,  
        pulse1DurationmS = 25, pulse2DurationmS = 25, pulseTotalDurationmS = 100)
    #idVStimSweepSettings1 = sparrow.CreateBatchSweepVStim(idVStim1, [v1, v2], idSweepRefMap1);
    idVStimSweepSettings1 = sparrow.CreateBatchSweepVStim(idVStim1, [], idSweepRefMap1);

 
    ifRec1 = sparrow.CreateRecMode("Rec1", True, RecGain.Gain10)
    sparrow.SetPixelConfigurationActive(idConfMap8)
    st = sparrow.SetPixelModeRow(6, 1, ifRec1)
    st = sparrow.SetPixelModeRow(6, 4, ifRec1)
    sparrow.SetPixelConfigurationActive(idConfMap9)
    st = sparrow.SetPixelModeRow(5, 1, ifRec1)
    st = sparrow.SetPixelModeRow(5, 16, ifRec1)

    rec10 = sparrow.CreateRecConfigurationObject(
        name='Rec10', 
        enableLowPassFilter=True, gain=RecGain.Gain2_5 )
    rec11 = sparrow.CreateRecConfigurationObject(
        name='Rec11', 
        enableLowPassFilter=True, gain=RecGain.Gain10 )
    idRecSweepSettings1 = sparrow.CreateBatchSweepRec(ifRec1, [rec10, rec11], idVStimSweepSettings1);

    tl6 = sparrow.CreateTimeLine(idRecSweepSettings1)
    idTlr1 = sparrow.CreateTimelineRepeat(5, tl6)

    sparrow.CreateTimeLineDelay(2000, idTlr1)
    sparrow.CreateTimeLineStimulationEvent(StimulationMode.Voltage, PulsePolarity.PositivePulseFirst, 10, idTlr1)


def RunBatchScript(sparrow: SparrowRpcService):
    status = sparrow.ScanUSb()
    status = sparrow.GetDeviceConnectionStatus()
    if status:
        print('START Batch Recording session')
        sparrow.SetPrintInfo(True)
        sparrow.EnableAsic() 
        sparrow.UploadSettings() 
        time.sleep(1.0)
        sparrow.ExecuteBatchRun() 
        sparrow.DisableAsic() 
        sparrow.SetPrintInfo(False)
        print('END Batch Recording session')
    else:
        print('Device is NOT Connected')
        print('Batch Session cannot be started')

def ExportMeasurementData(sparrow: SparrowRpcService):
    sparrow.ExportMeasurementData("C:\\TestSparrowApp\\dataexport.csv")

def run():
    print('\n\nSparrow Device DEMO 5')
    sparrow = initialiseSparrow()
    CreateBatchScript(sparrow)
    RunBatchScript(sparrow)
    ExportMeasurementData(sparrow)

if __name__ == '__main__':
    logging.basicConfig()
    run()