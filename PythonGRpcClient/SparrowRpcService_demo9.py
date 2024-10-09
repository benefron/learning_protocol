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

    time.sleep(2.0)
 
    res1 = sparrow.CreatePixelConfiguration("pixConf");
    res2 = sparrow.CloseConfiguration(True);

    
    res3 = sparrow.CloseConfiguration(True, idConfig1);
    res4 = sparrow.CloseConfiguration(True, idConfig2);

    configId = sparrow.LoadConfigurationFile("test.sparrowcfg")
    print('loadResult: id=' + str(configId))
    

def run():
    print('\n\nSparrow Device DEMO 9: Test Configuration')
    sparrow = initialiseSparrow()
    CreateAndCloseConfiguration(sparrow)


if __name__ == '__main__':
    logging.basicConfig()
    run()