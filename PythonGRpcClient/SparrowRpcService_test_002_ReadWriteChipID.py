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


def ReadWriteChipID(sparrow: SparrowRpcService):


    strID = sparrow.ReadChipID()
    print(strID)

    info =  sparrow.GetErrorInfo(0)
    if len(info)>0:
        print (info[0].functionName)
        print (info[0].errorDescription)
    else:
        print ("No errors occurred.")
    
    status = sparrow.WriteChipID('A123456-B12-C2')

    info =  sparrow.GetErrorInfo(0)
    if len(info)>0:
        print (info[0].functionName)
        print (info[0].errorDescription)
    else:
        print ("No errors occurred.")

def run():
    print('\n\nSparrow Device TEST 002: Read Write Chip ID')
    sparrow = initialiseSparrow()
    ReadWriteChipID(sparrow)

    status = sparrow.ScanUSb()
    status = sparrow.GetDeviceConnectionStatus()
    if status:
        print('Device is active ...')
        sparrow.EnableAsic() 
        ReadWriteChipID(sparrow)
        sparrow.DisableAsic()



if __name__ == '__main__':
    logging.basicConfig()
    run()