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


def ReadWriteChipId(sparrow: SparrowRpcService):
    sparrow.EnableAsic() 

    chipId = sparrow.ReadChipID()
    print('Chip ID: ' + chipId)

    # _status = sparrow.WriteChipID("P180288-X03-K3")
    # print('status "WriteChipID": ')
    # print(_status)

    info =  sparrow.GetErrorInfo(0)
    if len(info)>0:
        print (info[0].functionName)
        print (info[0].errorDescription)
    else:
        print ("No errors occurred.")

    chipId = sparrow.ReadChipID()
    print('Chip ID: ' + chipId)

    sparrow.DisableAsic() 


def run():
    print('\n\nSparrow Device DEMO 7: Read/Write Chip Id')
    sparrow = initialiseSparrow()
    ReadWriteChipId(sparrow)


if __name__ == '__main__':
    logging.basicConfig()
    run()