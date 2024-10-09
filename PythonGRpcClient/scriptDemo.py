from SparrowRpcService import *


sp = SparrowRpcService()

# Prep: Configuration
configA = sp.CreateEmptyConfiguration("ConfigA")
# Prep: MuxMap
mm1 = sp.CreateMuxMap("mm1", ElectrodePosition.E1)
sp.SetMuxMapWell(1, ElectrodePosition.TopLeft)
# Prep: RefMap
rm1 = sp.CreateRefElectrodeMap("rm1", WellReferenceFlag.AllInternal)
rm2 = sp.CreateRefElectrodeMap("rm2", WellReferenceFlag.Internal0|WellReferenceFlag.Internal1|WellReferenceFlag.Internal4|WellReferenceFlag.Internal5)
# Prep: Rec
rec = sp.CreateRecMode("rec1", True, RecGain.Gain1)
rc1 = sp.CreateRecConfigurationObject("rec11", False, RecGain.Gain2_5)
# Prep: VStim
v1 = sp.CreateVStimMode("v1",300,300,3,3,10)
v11 = sp.CreateVStimConfigurationObject("v11",  200, 200, 3,3,10)
# Prep: Cell Config Map
cc1 = sp.CreatePixelConfiguration("cc1")
sp.SetPixelMode(1, v1)
sp.SetPixelModeWell(8, rec)

sp.SetPixelModeColumn(8, 1, v1)
# Create Prog

progId = sp.CreateBatchProgram("prog1")

bv = sp.CreateBatchSweepVStim(v1, [v11], progId)
timelineID = sp.CreateTimeLine(bv)
sp.CreateTimeLineStimulationEvent(StimulationMode.Voltage, PulsePolarity.PositivePulseFirst, 20, timelineID)


sp.ExecuteBatchRun()