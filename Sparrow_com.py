# This will simulate the communication with the sparrow app

import time
from SparrowRpcService import *

def initialiseSparrow() -> SparrowRpcService:
    sparrow = SparrowRpcService('localhost', 443)
    return sparrow

def CreateBatchScript(sparrow: SparrowRpcService):
    pass
    
    

