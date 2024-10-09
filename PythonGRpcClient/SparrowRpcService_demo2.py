
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

def run():
    print('\n\nSparrow Device DEMO 2')
    sparrow = initialiseSparrow()





if __name__ == '__main__':
    logging.basicConfig()
    run()