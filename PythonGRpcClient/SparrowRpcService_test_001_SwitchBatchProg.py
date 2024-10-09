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


def CreateProg1(sparrow: SparrowRpcService, idRec: int) -> int:
    idPix1 = sparrow.CreatePixelConfiguration("pix1");
    sparrow.SetPixelModeWell(4, idRec)

    idP1 = sparrow.CreateBatchProgram('p1')
    idPixmapSweep1 = sparrow.CreateBatchSweepCfgMap([idPix1],False,idP1)
    idRecSweep1 = sparrow.CreateBatchSweepRec(idRec, [], idPixmapSweep1)
    idTimeline1 = sparrow.CreateTimeLine(idRecSweep1)
    idImpMon1 = sparrow.CreateTimelineImpedanceMonitor(ImpMonFrequency.Frequency10kHz, ImpMonAmplitude.Amplitude1nA, idTimeline1)
    sparrow.CreateTimeLineDelay(10000, idImpMon1)
    return idP1

def CreateProg2(sparrow: SparrowRpcService, idRec: int) -> int:
    idPix2 = sparrow.CreatePixelConfiguration("pix2");
    sparrow.SetPixelModeWell(8, idRec)
    sparrow.SetPixelModeWell(16, idRec)

    idP2 = sparrow.CreateBatchProgram('p2')
    idPixmapSweep2 = sparrow.CreateBatchSweepCfgMap([idPix2],False,idP2)
    idRecSweep2 = sparrow.CreateBatchSweepRec(idRec, [], idPixmapSweep2)
    idTimeline2 = sparrow.CreateTimeLine(idRecSweep2)
    idSd1 = sparrow.CreateTimelineSliceDefinition([Processor.Avg, Processor.StdDev], idTimeline2)
    sparrow.CreateTimeLineDelay(15000, idSd1)
    return idP2

def CreateProg3(sparrow: SparrowRpcService, idRec: int) -> int:
    idPix3 = sparrow.CreatePixelConfiguration("pix1");
    sparrow.SetPixelModeWell(4, idRec)
    sparrow.SetPixelModeWell(1, idRec)
    sparrow.SetPixelModeWell(15, idRec)

    idP3 = sparrow.CreateBatchProgram('p1')
    idPixmapSweep1 = sparrow.CreateBatchSweepCfgMap([idPix3],False,idP3)
    idRecSweep1 = sparrow.CreateBatchSweepRec(idRec, [], idPixmapSweep1)
    idTimeline1 = sparrow.CreateTimeLine(idRecSweep1)
    idImpMon1 = sparrow.CreateTimelineImpedanceMonitor(ImpMonFrequency.Frequency10kHz, ImpMonAmplitude.Amplitude1nA, idTimeline1)
    sparrow.CreateTimeLineDelay(10000, idImpMon1)
    return idP3


def CreateProg4(sparrow: SparrowRpcService, idRec: int) -> int:
    idPix4 = sparrow.CreatePixelConfiguration("pix2");
    sparrow.SetPixelModeWell(8, idRec)
    sparrow.SetPixelModeWell(16, idRec)
    sparrow.SetPixelModeWell(2, idRec)
    sparrow.SetPixelModeWell(3, idRec)

    idP4 = sparrow.CreateBatchProgram('p2')
    idPixmapSweep2 = sparrow.CreateBatchSweepCfgMap([idPix4],False,idP4)
    idRecSweep2 = sparrow.CreateBatchSweepRec(idRec, [], idPixmapSweep2)
    idTimeline2 = sparrow.CreateTimeLine(idRecSweep2)
    idSd1 = sparrow.CreateTimelineSliceDefinition([Processor.Avg, Processor.StdDev], idTimeline2)
    sparrow.CreateTimeLineDelay(15000, idSd1)
    return idP4

def CreateAndRunBatchPrograms(sparrow: SparrowRpcService):
    idConfig1 = sparrow.CreateEmptyConfiguration("MyTestConfig1")
    idRec1 = sparrow.CreateRecMode('rec1', False, RecGain.Gain1);
    
    idP1_1 = CreateProg1(sparrow, idRec1)
    idP1_2 = CreateProg2(sparrow, idRec1)

    idConfig2 = sparrow.CreateEmptyConfiguration("MyTestConfig2")
    idRec2 = sparrow.CreateRecMode('rec2', False, RecGain.Gain1);
    
    idP2_1 = CreateProg3(sparrow, idRec2)
    idP2_2 = CreateProg4(sparrow, idRec2)

    sparrow.SetConfigurationActive(idConfig1)
    sparrow.SetBatchProgramActive(idP1_1)
    time.sleep(2);

    sparrow.SetConfigurationActive(idConfig1)
    sparrow.SetBatchProgramActive(idP1_2)
    time.sleep(2);

    sparrow.SetConfigurationActive(idConfig2)
    sparrow.SetBatchProgramActive(idP2_1)
    time.sleep(2);

    sparrow.SetConfigurationActive(idConfig2)
    sparrow.SetBatchProgramActive(idP2_2)
    time.sleep(2);


    status = sparrow.ScanUSb()
    status = sparrow.GetDeviceConnectionStatus()
    if status:
        print('START Batch Recording session')
    
        resultOK:bool = True;   
        if resultOK:
            resultOK = sparrow.EnableAsic() 
        if resultOK:
            resultOK = sparrow.UploadSettings() 
            time.sleep(1.0)     

        if resultOK:
            resultOK = RunProgram(sparrow, idConfig1, idP1_1, "C:\\TestSparrowApp3\\Export_Prog11_1.csv")
            time.sleep(2)
        if resultOK:
            resultOK = RunProgram(sparrow, idConfig1, idP1_2, "C:\\TestSparrowApp3\\Export_Prog12_1.csv")
            time.sleep(2)
        if resultOK:
            resultOK = RunProgram(sparrow, idConfig2, idP2_1, "C:\\TestSparrowApp3\\Export_Prog21_1.csv")
            time.sleep(2)
        if resultOK:
            resultOK = RunProgram(sparrow, idConfig2, idP2_2, "C:\\TestSparrowApp3\\Export_Prog22_1.csv")
            time.sleep(2)
        if resultOK:
            resultOK = RunProgram(sparrow, idConfig1, idP1_1, "C:\\TestSparrowApp3\\Export_Prog11_2.csv")
            time.sleep(2)
        if resultOK:
            resultOK = RunProgram(sparrow, idConfig1, idP1_2, "C:\\TestSparrowApp3\\Export_Prog12_2.csv")
            time.sleep(2)

        sparrow.DisableAsic() 
        print('END Batch Recording session')
    else:
        print('Device is NOT Connected')
        print('Batch Session cannot be started')

    sparrow.CloseConfiguration(False, idConfig1)
    sparrow.CloseConfiguration(False, idConfig2)

def RunProgram(sparrow: SparrowRpcService, idConfig:int, idProg:int, filename:str) -> bool:
    resultOK: bool = True; 
    if resultOK: 
        sparrow.SetConfigurationActive(idConfig)
        resultOK = CheckResult(sparrow)
    if resultOK: 
        sparrow.SetBatchProgramActive(idProg)
        resultOK = CheckResult(sparrow)
    if resultOK: 
        sparrow.ExecuteBatchRun()
        resultOK = CheckResult(sparrow)
    if resultOK: 
        sparrow.ExportMeasurementData(filename)
        resultOK = CheckResult(sparrow)
    if resultOK: 
        print('Prog run Done -> OK')
    else:
        print('Prog run Done -> ERROR')
    return resultOK

def CheckResult(sparrow: SparrowRpcService) -> bool:
    info =  sparrow.GetErrorInfo(0)
    result = True;
    if len(info)>0:
        print (info[0].functionName)
        print (info[0].errorDescription)
        result = False

    
    return result
 
    
def run():
    print('\n\nSparrow Device TEST 001: SwitchBatchProg')
    sparrow = initialiseSparrow()
    CreateAndRunBatchPrograms(sparrow)


if __name__ == '__main__':
    logging.basicConfig()
    run()