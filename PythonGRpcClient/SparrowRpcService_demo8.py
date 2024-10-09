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


def CreateAndCloseConfiguration(sparrow: SparrowRpcService):
    idConfig1 = sparrow.CreateEmptyConfiguration("MyTestConfig1")
    idConfig2 = sparrow.CreateEmptyConfiguration("MyTestConfig2")

    sparrow.CreatePixelConfiguration("pixConf");

    time.sleep(5.0)
    
    sparrow.CloseConfiguration(idConfig1);
    sparrow.CloseConfiguration(idConfig2);


def run():
    print('\n\nSparrow Device DEMO 8: remove Configuration')
    sparrow = initialiseSparrow()
    CreateAndCloseConfiguration(sparrow)


if __name__ == '__main__':
    logging.basicConfig()
    run()