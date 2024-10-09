from __future__ import print_function
from asyncio.windows_events import NULL
from distutils.spawn import spawn
from fileinput import filename

import logging
import time
from datetime import datetime
from tokenize import Double
from unicodedata import name
from urllib import response
from warnings import catch_warnings
from enum import IntFlag
from enum import IntEnum

import grpc
import contracts_pb2
import contracts_pb2_grpc


class ElectrodePosition(IntEnum):
   E1 = 0
   E2 = 1
   E3 = 2
   E4 = 3
   TopLeft = 4
   TopRight = 5
   BottomLeft = 6
   BottomRight = 7

class PulsePolarity(IntEnum):
   PositivePulseFirst = 0
   NegativePulseFirst = 1

class IStepValues(IntEnum):
   IStep_2pA = 0
   IStep_6pA = 1
   IStep_500pA = 2
   IStep_1500pA = 3

class RecGain(IntEnum):
   Gain1 = 0
   Gain2_5 = 1
   Gain5 = 2
   Gain10 = 3
   Gain20 = 4
   Gain30 = 5
   Gain40 = 6
   Gain60 = 7      

class ImpSpecFreq(IntEnum):
   Freq_9Hz6 = 0x00
   Freq_19Hz2 = 0x01
   Freq_48Hz = 0x02
   Freq_96Hz = 0x03
   Freq_192Hz = 0x04
   Freq_480Hz = 0x05
   Freq_960Hz = 0x06
   Freq_1920Hz = 0x07
   Freq_4800Hz = 0x08
   Freq_9600Hz = 0x09
   Freq_19200Hz = 0x0A
   Freq_48kHz = 0x0B
   Freq_96kHz = 0x0C
   Freq_192kHz = 0x0D
   Freq_480kHz = 0x0E
   Freq_960kHz = 0x0F

class WellReferenceFlag(IntFlag):
   NoFlag = 0x00
   External = 0x01
   Internal0 = 0x02
   Internal1 = 0x04
   Internal2 = 0x08
   Internal3 = 0x10
   Internal4 = 0x20
   Internal5 = 0x40
   Internal6 = 0x80
   Internal7 = 0x100
   AllInternal = 0x1FE

class ImpMonFrequency(IntEnum):
   Frequency1kHz = 0
   Frequency10kHz = 1

class ImpMonAmplitude(IntEnum):
   Amplitude1nA = 0
   Amplitude10nA = 1

class StimulationMode(IntEnum):
   Voltage = 0
   Current = 1
   VoltageAndCurrent = 2

class Processor(IntEnum):
   StdDev = 0
   Avg = 1
   PeakToPeak = 2
   ZMon = 3
   VRms = 4


class SparrowRpcService(object):

   __printInfoActive:bool = False
   __stub:contracts_pb2_grpc.RpcServiceStub



   def __init__(self, host: str = "localhost", portNr: int = 443):
      channel = grpc.insecure_channel("{host}:{portNr}".format(host=host, portNr=portNr))
      self.__stub = contracts_pb2_grpc.RpcServiceStub(channel)


   def __PrintInfo(self, info: str):
      ''' Private function to print the given info with a timestamp
         All functions in the SparrowRpcService class print execution info if activated

         Parameters:
            **info (string):** info to print

         Returns:
            -
         '''
      if self.__printInfoActive:
         print(datetime.now().strftime('%H:%M:%S,%f') + ' : ' + info)   

   def SetPrintInfo(self, onOff: bool):
      ''' Set PrintInfo functionality on or off. 

         Parameters:
            **onOff (bool):** 

         Returns:
            -
         '''
      self.__printInfoActive = onOff

   def GetAppVersion(self) -> str:
      ''' Get Version of the SparrowApp
         Parameters:
            -

         Returns:
            **str:** version info
         '''
      response:contracts_pb2.StringReply = self.__stub.GetAppVersion(contracts_pb2.EmptyMessage())
      self.__PrintInfo("Get App Version = " + response.value)   
      return response.value         

   def GetRpcVersion(self) -> str:
      ''' Get Version of the SparrowApp

         Parameters:
            -

         Returns:
            **str:** version info
         '''
      response:contracts_pb2.StringReply = self.__stub.GetRpcVersion(contracts_pb2.EmptyMessage())
      self.__PrintInfo("Get Rpc Version = " + response.value)   
      return response.value

   def ScanUSb(self) -> bool:
      ''' Scan USB bus to search for Sparrow setup

         Parameters:
            -

         Returns:
            **bool:** true if Sparrow setup is present
         '''
      response = self.__stub.ScanUSb(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Scan USb > status = " + str(response.value))  
      return response.value

   def GetDeviceConnectionStatus(self) -> bool:
      ''' Get Sparrow setup connection status

         Parameters:
            -

         Returns:
            **bool:** true if Sparrow setup is present
         '''
      response = self.__stub.GetDeviceConnectionStatus(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Get Device Connection Status > status = " + str(response.value))  
      return response.value

   def EnableAsic (self) -> bool:
      ''' Enable Sparrow chip (power on)

         Parameters:
            -

         Returns:
            **bool:** true if function succeeded
         '''
      response = self.__stub.EnableAsic(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Enable Asic > status = " + str(response.value)) 
      return response.value

   def DisableAsic (self) -> bool:
      ''' Disable Sparrow chip (power off)

         Parameters:
            -

         Returns:
            **bool:** true if function succeeded
         '''
      response = self.__stub.DisableAsic(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Disable Asic > status = " + str(response.value)) 
      return response.value

   def ResetAsic (self) -> bool:
      ''' Reset Sparrow chip

         Parameters:
            -

         Returns:
            **bool:** true if function succeeded
         '''
      response = self.__stub.ResetAsic(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Reset Asic > status = " + str(response.value)) 
      return response.value

   def WriteChipID (self, ID: str) -> bool:
      ''' Write serial number into MEAP

         Parameters:
            **ChipID (str):** serial number

         Returns:
            **bool:** true if function succeeded
         '''
      cid = contracts_pb2.ChipID()
      cid.chipid = ID     
      response = self.__stub.WriteChipID(cid)
      self.__PrintInfo(" Write Chip ID '" + ID + "' > status = " + str(response.value))
      return response.value

   def ReadChipID(self) -> str:
      ''' Read serial number from MEAP

         Parameters:
            -

         Returns:
            **str:** serial number
         '''
      response:contracts_pb2.StringReply = self.__stub.ReadChipID(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Read Chip ID = " + response.value)   
      return response.value         


   def DisableADCCalibration(self) -> bool:
      ''' Disable ADC Calibration

         Parameters:
            -

         Returns:
            **bool:** true if function succeeded
         '''
      response = self.__stub.DisableADCCalibration(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Disable ADC Calibration > status = " + str(response.value)) 
      return response.value

   def LoadADCCalibrationFile(self, fullFilename: str) -> bool:
      ''' Load ADC Calibration file

         Parameters:
            **fullFilename (str):** full path and filename (*.sparrowpack)

         Returns:
            **bool:** true if function succeeded
         '''
      req = contracts_pb2.File(filename=fullFilename)
      response = self.__stub.LoadADCCalibrationFile(req)
      self.__PrintInfo(" Load ADC Calibration File > status = " + str(response.value)) 
      return response.value

   def LoadConfigurationFile(self, fullFilename: str) -> int:
      ''' Load Configuration file
         This will be the active configuration if the function succeeds

         Parameters:
            **fullFilename (str):** full path and filename (*.sparrowcfg)

         Returns:
            **int:** id of the Configuration
         '''
      f = contracts_pb2.File(filename=fullFilename)
      response = self.__stub.LoadConfigurationFile(f)
      self.__PrintInfo(" Load Configuration File '" + fullFilename + "' > id = " + str(response.value))
      return response.value

   def CreateEmptyConfiguration(self, name: str) -> int:
      ''' Create Empty Configuration
         This will be the active configuration if the function succeeds

         Parameters:
            **name (str):** name for the configuration, this will also be the filename to save the configuration to.

         Returns:
            **int:** id of the Configuration
         '''
      config = contracts_pb2.ConfigurationNew()
      config.name = name     
      response = self.__stub.CreateEmptyConfiguration(config)
      self.__PrintInfo(" Create Empty Configuration '" + name + "' > id = " + str(response.value))
      return response.value

   def ClearConfiguration (self, id: int = -1) -> bool:
      ''' Clear Configuration

         Parameters:
            **id (int)(optional):** id of the configuration, if omitted, the active configuration is used

         Returns:
            **bool:** true if function succeeded
         '''
      response = self.__stub.ClearConfiguration(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Clear Configuration > status = " + str(response.value))   
      return response.value

   def CloseConfiguration(self, save: bool, id: int = -1) -> bool:
      ''' Close Configuration

         Parameters:
            **save (bool):** True if changes have to be saved, otherwise changes are discarded. If a new file has an already existing name, it will not be saved or closed
            
            **id (int)(optional):** id of the configuration, if omitted, the active configuration is used

         Returns:
            **bool:** true if function succeeded
         '''
      req = contracts_pb2.ConfigurationClose()
      req.id = id     
      req.save = save     

      response = self.__stub.CloseConfiguration(req)
      self.__PrintInfo(" Close Configuration > status = " + str(response.value)) 
      return response.value

   def SetConfigurationActive(self, id: int) -> bool:
      ''' Set Configuration Active

         Parameters:
            **id (int):** id of the configuration 

         Returns:
            **bool:** true if function succeeded
         '''
      req = contracts_pb2.Id(value = id)
      response = self.__stub.SetConfigurationActive(req)
      self.__PrintInfo(" Set Configuration Active > status = " + str(response.value)) 
      return response.value


   def CreateMuxMap (self, name: str, electrodePos: ElectrodePosition) -> int:
      ''' Create MuxMap in the active Configuration

         Parameters:
            name (str): name for the MuxMap

            electrodePos (ElectrodePosition): one of the predefined ElectrodePosition values

         Returns:
            int: id of the MuxMap
         '''
      electrodeMuxMap = contracts_pb2.MuxMapNew()
      electrodeMuxMap.name = name
      electrodeMuxMap.electrodePos = electrodePos
      response = self.__stub.CreateMuxMap(electrodeMuxMap)
      self.__PrintInfo(" Create Mux Map '" + name + "' > id = " + str(response.value )) 
      return response.value
  
   def SetMuxMapActive (self, id: int) -> bool:
      ''' Set MuxMap as the active one

         Parameters:
            **id (int):** id of the MuxMap

         Returns:
            **bool:** true if function succeeded
         '''
      req = contracts_pb2.Id(value = id)
      response = self.__stub.SetMuxMapActive(req)
      self.__PrintInfo(" Set Mux Map Active > status = " + str(response.value))
      return response.value

   def SetMuxMap (self, electrodePos: ElectrodePosition) -> bool:
      ''' Set ElectrodePosition of entire MuxMap

         Parameters:
            **electrodePos (ElectrodePosition):** one of the predefined ElectrodePosition values

         Returns:
            **bool:** true if function succeeded
         '''
      electrodeMuxMap = contracts_pb2.MuxMap()
      electrodeMuxMap.electrodePos = electrodePos
      response = self.__stub.SetMuxMap(electrodeMuxMap)
      self.__PrintInfo(" Set Mux Map > status " + str(response.value))  
      return response.value

   def SetMuxMapWell (self, wellNr: int, electrodePos: ElectrodePosition) -> bool:
      ''' Set ElectrodePosition of one Well in the MuxMap

         Parameters:
            **wellNr (int):** nr of the Well

            **electrodePos (ElectrodePosition):** one of the predefined ElectrodePosition values

         Returns:
            **bool:** true if function succeeded
         '''
      electrodeMuxWell = contracts_pb2.MuxMapWell()
      electrodeMuxWell.wellNr = wellNr
      electrodeMuxWell.electrodePos = electrodePos
      response = self.__stub.SetMuxMapWell(electrodeMuxWell)
      self.__PrintInfo(" Set Mux Map Well > status " + str(response.value))  
      return response.value

   def SetMuxMapPixel (self, pixelNr: int, electrodePos: ElectrodePosition) -> bool:
      ''' Set ElectrodePosition of one Pixel in the MuxMap

         Parameters:
            **pixelNr (int):** nr of the Pixel

            **electrodePos (ElectrodePosition):** one of the predefined ElectrodePosition values

         Returns:
            **bool:** true if function succeeded
         '''
      electrodeMuxPixel = contracts_pb2.MuxMapPixel()
      electrodeMuxPixel.pixelNr = pixelNr
      electrodeMuxPixel.electrodePos = electrodePos
      response = self.__stub.SetMuxMapPixel(electrodeMuxPixel)
      self.__PrintInfo(" Set Mux Map Pixel > status " + str(response.value))  
      return response.value

   def CreateRefElectrodeMap (self, name: str, reference: WellReferenceFlag) -> int:
      ''' Create RefElectrodeMap in the active Configuration

         Parameters:
            **name (str):** name for the RefElectrodeMap

            **reference (WellReferenceFlag):** WellReferenceFlag to apply on all wells

         Returns:
            **int:** id of the RefElectrodeMap
         '''
      wellReferenceSet = contracts_pb2.WellRefSetNew()
      wellReferenceSet.name = name
      wellReferenceSet.reference = reference
      response = self.__stub.CreateRefElectrodeMap(wellReferenceSet)
      self.__PrintInfo(" Create Ref Electrode Map '" + name + "' > id = " + str(response.value))
      return response.value

   def SetRefElectrodeMapActive (self, id) -> bool:
      ''' Set RefElectrodeMap as the active one

         Parameters:
            **id (int):** id of the RefElectrodeMap
 
         Returns:
            **bool:** true if function succeeded
         '''
      req = contracts_pb2.Id(value = id)
      response = self.__stub.SetRefElectrodeMapActive(req)
      self.__PrintInfo(" Set Ref Electrode Map Active > status = " + str(response.value))
      return response.value

   def SetRefElectrodeMap (self, reference: WellReferenceFlag) -> bool:
      ''' Set well reference configuration in the active RefElectrodeMap

         Parameters:
            **reference (WellReferenceFlag):** WellReferenceFlag to apply on all wells

         Returns:
            **bool:** true if function succeeded
         '''
      wellReferenceSet = contracts_pb2.WellRefSet()
      wellReferenceSet.reference = reference
      response = self.__stub.SetRefElectrodeMap(wellReferenceSet)
      self.__PrintInfo(" Set Ref Electrode Map > status = " + str(response.value))
      return response.value

   def SetRefElectrodeWell (self, wellNr, reference: WellReferenceFlag) -> bool:
      ''' Set well reference configuration in a single well in the active RefElectrodeMap

         Parameters:
            **wellNr (int):** nr of the Well

            **reference (WellReferenceFlag):** WellReferenceFlag to apply on all wells

         Returns:
            **bool:** true if function succeeded
         '''
      wellReference = contracts_pb2.WellRef()
      wellReference.reference = reference
      wellReference.wellNr = wellNr
      response = self.__stub.SetRefElectrodeWell(wellReference)
      self.__PrintInfo(" Set Ref Electrode Well > status = " + str(response.value))
      return response.value

   def CreateVStimMode (self, name: str, pulse1VoltagemV: float, pulse2VoltagemV: float, pulse1DurationmS: int, pulse2DurationmS: int, pulseTotalDurationmS: int) -> int:
      ''' Create Voltage Stimulation Mode in the active configuration

         Parameters:
            **name (str):** 

            **pulse1VoltagemV (float):** first pulse voltage in mV

            **pulse2VoltagemV (float):** second pulse voltage in mV

            **pulse1DurationmS (int):** first pulse duration in ms

            **pulse2DurationmS (int):** second pulse duration in ms

            **pulseTotalDurationmS (int):** total duration in ms

         Returns:
            **int:** id of the Voltage Stimulation Mode
         '''
      vStim = contracts_pb2.VStimConfiguration()
      vStim.name = name
      vStim.Pulse1VoltagemV = pulse1VoltagemV
      vStim.Pulse2VoltagemV = pulse2VoltagemV
      vStim.Pulse1DurationmS = pulse1DurationmS
      vStim.Pulse2DurationmS = pulse2DurationmS
      vStim.PulseTotalDurationmS = pulseTotalDurationmS
      response = self.__stub.CreateVStimMode(vStim)
      self.__PrintInfo(" Create VStim Mode '" + name + "' > id = " + str(response.value))
      return response.value

   def CreateIStimMode (self, name: str, currentStepValue: IStepValues, pulse1CurrentpA: float, pulse2CurrentpA: float, pulse1DurationmS: int, pulse2DurationmS: int, pulseTotalDurationmS) -> int:
      ''' Create Current Stimulation Mode in the active configuration

         Parameters:
            **name (str):** 

            **currentStepValue (IStepValues):** current step size

            **pulse1CurrentpA (float):** first pulse current in pA

            **pulse2CurrentpA (float):** second pulse current in pA

            **pulse1DurationmS (int):** first pulse duration in ms

            **pulse2DurationmS (int):** second pulse duration in ms

            **pulseTotalDurationmS (int):** total duration in ms

         Returns:
            **int:** id of the Current Stimulation Mode
         '''
      iStim = contracts_pb2.IStimConfiguration()
      iStim.name = name
      iStim.CurrentStepValue = currentStepValue
      iStim.Pulse1CurrentpA = pulse1CurrentpA
      iStim.Pulse2CurrentpA = pulse2CurrentpA
      iStim.Pulse1DurationmS = pulse1DurationmS
      iStim.Pulse2DurationmS = pulse2DurationmS
      iStim.PulseTotalDurationmS = pulseTotalDurationmS
      response = self.__stub.CreateIStimMode(iStim)
      self.__PrintInfo(" Create IStim Mode '" + name + "' > id = " + str(response.value))
      return response.value

   def CreateRecMode(self, name: str, enableLowPassFilter: bool, gain: RecGain) -> int:
      ''' Create Recording Mode in the active configuration

         Parameters:
            name (str): reference name

            enableLowPassFilter (bool):

            gain (RecGain): Select gain from Gain1 to Gain60

         Returns:
            int: id of the Current Recording Mode
         '''
      recMode = contracts_pb2.RecConfiguration()
      recMode.name = name
      recMode.EnableLowPassFilter = enableLowPassFilter
      recMode.Gain = gain
      response = self.__stub.CreateRecMode(recMode)
      self.__PrintInfo(" Create Rec Mode '" + name + "' > id = " + str(response.value))
      return response.value

   def CreateImpSpecFreqConfiguration(self, frequency: ImpSpecFreq, currentStepValue: IStepValues, currentMultiplier: int) -> contracts_pb2.ImpSpecFreqConfiguration:
      ''' Create an Impedance Spectroscopy Configuration, to be used with CreateImpSpecMode

         Parameters:
            frequency (ImpSpecFreq): frequency

            currentStepValue (IStepValues): current Step Value to be used by the DAC

            currentMultiplier (int): multiplier x stepValue determines the total current
        
         Returns:
            contracts_pb2.ImpSpecFreqConfiguration: Impedance Spectroscopy Configuration, to be used with function CreateImpSpecMode
         '''
      impSpecFreqConfiguration = contracts_pb2.ImpSpecFreqConfiguration()
      impSpecFreqConfiguration.Frequency = frequency
      impSpecFreqConfiguration.CurrentStepValue = currentStepValue
      impSpecFreqConfiguration.CurrentMultiplier = currentMultiplier
      return impSpecFreqConfiguration

   def CreateImpSpecMode(self, name: str, lstImpSpecFreqConfiguration: list[contracts_pb2.ImpSpecFreqConfiguration]) -> int:
      impSpecMode = contracts_pb2.ImpSpecConfiguration()
      impSpecMode.name = name
      impSpecMode.lstImpSpecFreqConfiguration.extend(lstImpSpecFreqConfiguration)
      response = self.__stub.CreateImpSpecMode(impSpecMode)
      self.__PrintInfo(" Create Impedance Spectroscopy Mode '" + name + "' > id = " + str(response.value))
      return response.value

   def CreatePixelConfiguration(self, name: str) -> int:
      ''' Create Pixel configuration in the active configuration

         Parameters:
            name (str): reference name

         Returns:
            int: id of the PixelConfiguration
         '''
      confMap = contracts_pb2.PixelConfigurationNew()
      confMap.name = name
      response = self.__stub.CreatePixelConfiguration(confMap)
      self.__PrintInfo(" Create Pixel Configuration '" + name + "' > id = " + str(response.value))
      return response.value

   def SetPixelConfigurationActive(self, id: int) -> bool:
      ''' Set Pixel configuration as the active one

         Parameters:
            id (int): id of the pixel configuration

         Returns:
            bool: true if the function succeeds
         '''
      req = contracts_pb2.Id(value = id)
      response = self.__stub.SetPixelConfigurationActive(req)
      self.__PrintInfo(" Set Pixel Configuration Active > status = " + str(response.value))
      return response.value

   def SetPixelMode (self, pixelNr: int, modeId: int) -> bool:
      ''' Set Pixel Mode in a single pixel

         Parameters:
            pixelNr (int): nr between 1 .. 4096

            modeId (int): id of the VStim, IStim or Rec mode, enter 0 to disable the pixel

         Returns:
            bool: true if the function succeeds
         '''
      confMap = contracts_pb2.PixelMode()
      confMap.pixelNr = pixelNr
      confMap.modeId = modeId
      response = self.__stub.SetPixelMode(confMap)
      self.__PrintInfo(" Set Pixel Mode > status = " + str(response.value))
      return response.value

   def SetPixelModeWell(self, wellNr: int, modeId: int) -> bool:
      ''' Set Pixel Mode in a complete Well

         Parameters:
            wellNr (int): nr between 1 .. 16

            modeId (int): id of the VStim, IStim or Rec mode, enter 0 to disable all pixels in the well

         Returns:
            bool: true if the function succeeds
         '''
      confMap = contracts_pb2.PixelModeWell()
      confMap.wellNr = wellNr
      confMap.modeId = modeId
      response = self.__stub.SetPixelModeWell(confMap)
      self.__PrintInfo(" Set Pixel Mode Well > status = " + str(response.value))
      return response.value

   def SetPixelModeRow(self, wellNr: int, rowNr: int, modeId: int) -> bool:
      ''' Set Pixel Mode in one row

         Parameters:
            wellNr (int): nr between 1 .. 16

            rowNr (int): nr between 1 .. 16
            
            modeId (int): id of the VStim, IStim or Rec mode, enter 0 to disable all pixels in the row

         Returns:
            bool: true if the function succeeds
         '''
      confMap = contracts_pb2.PixelModeRow()
      confMap.wellNr = wellNr
      confMap.rowNr = rowNr
      confMap.modeId = modeId
      response = self.__stub.SetPixelModeRow(confMap)
      self.__PrintInfo(" Set Pixel Mode Row > status = " + str(response.value))
      return response.value

   def SetPixelModeColumn(self, wellNr: int, columnNr: int, modeId: int) -> bool:
      ''' Set Pixel Mode in one column

         Parameters:
            wellNr (int): nr between 1 .. 16

            columnNr (int): nr between 1 .. 16

            modeId (int): id of the VStim, IStim or Rec mode, enter 0 to disable all pixels in the column

         Returns:
            bool: true if the function succeeds
         '''
      confMap = contracts_pb2.PixelModeColumn()
      confMap.wellNr = wellNr
      confMap.columnNr = columnNr
      confMap.modeId = modeId
      response = self.__stub.SetPixelModeColumn(confMap)
      self.__PrintInfo(" Set Pixel Mode Column > status = " + str(response.value))
      return response.value

   def SetPixelModeRange(self, pixelNrFrom: int, pixelNrTo: int, modeId: int) -> bool:
      ''' Set Pixel Mode in a range of pixels

         Parameters:
            pixelNrFrom (int): first pixel in range to set to chosen mode

            pixelNrTo (int): last pixel in range to set to chosen mode

            modeId (int): id of the VStim, IStim or Rec mode, enter 0 to disable all pixels in the range

         Returns:
            bool: true if the function succeeds
         '''
      confMap = contracts_pb2.PixelModeRange()
      confMap.pixelNrFrom = pixelNrFrom
      confMap.pixelNrTo = pixelNrTo
      confMap.modeId = modeId
      response = self.__stub.SetPixelModeRange(confMap)
      self.__PrintInfo(" Set Pixel Mode Range > status = " + str(response.value))
      return response.value

   def UploadSettings (self) -> bool:
      ''' Upload the active configuration to the Sparrow system

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.UploadSettings(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Upload Settings > status = " + str(response.value))   
      return response.value

   def ExecuteImpedanceSpectroscopy(self) -> bool:
      ''' Execute a complete Impedance Spectroscopy measurement. The function returns when the measurement ends

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.ExecuteImpedanceSpectroscopy(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Execute Impedance Spectroscopy measurement > status = " + str(response.value))   
      return response.value

   def StartAcquisition (self) -> bool:
      ''' Start a manual acquisition. The function returns immediately

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.StartAcquisition(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Start Acquisition > status = " + str(response.value))   
      return response.value

   def StartBatchRun (self) -> bool:
      ''' Start a batch run. The function returns immediately

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.StartBatchRun(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Start Batch Run > status = " + str(response.value))   
      return response.value

   def ExecuteBatchRun (self) -> bool:
      ''' Execute a batch run. The function returns when the batch run ends

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.ExecuteBatchRun(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Execute Batch Run > status = " + str(response.value))   
      return response.value

   def StopAcquisition (self) -> bool:
      ''' Stop a manual acquisition or a batch run.

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.StopAcquisition(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Stop Acquisition > status = " + str(response.value))   
      return response.value

   def ExportMeasurementData(self, fullFilename: str)-> bool:
      ''' Export Measurement Data

         Parameters:
            fullFilename (str): full path and filename (*.csv)

         Returns:
            bool: true if function succeeded
         '''
      req = contracts_pb2.File(filename=fullFilename)
      response = self.__stub.ExportMeasurementData(req)
      self.__PrintInfo(" Export Measurement Data > status = " + str(response.value)) 
      return response.value

   def StartStimulationSequence(self, pulseCount: int, polarity: PulsePolarity, voltageStimulation: bool, currentStimulation: bool) -> bool:
      ''' Start a stimulation sequence manually. The function returns immediately

         Parameters:
            pulseCount (int)
            
            polarity (PulsePolarity)
            
            voltageStimulation (bool)
            
            currentStimulation (bool)

         Returns:
            bool: true if the function succeeds
         '''
      stimulation = contracts_pb2.StimulationSequence()
      stimulation.pulseCount = pulseCount
      stimulation.polarity = polarity
      stimulation.voltageStimulation = voltageStimulation
      stimulation.currentStimulation = currentStimulation
      response = self.__stub.StartStimulationSequence(stimulation)
      self.__PrintInfo(" Start Stimulation Sequence > status = " + str(response.value))   
      return response.value

   def StartImpedanceMonitoring(self, frequency: ImpMonFrequency, amplitude: ImpMonAmplitude) -> bool:
      ''' Start an impedance monitoring measurement manually. The function returns immediately

         Parameters:
            frequency (ImpMonFrequency) 
            
            amplitude (ImpMonAmplitude)

         Returns:
            bool: true if the function succeeds
         '''
      impMon = contracts_pb2.ImpedanceMonitoring()
      impMon.frequency = frequency
      impMon.amplitude = amplitude
      response = self.__stub.StartImpedanceMonitoring(impMon)
      self.__PrintInfo(" Start Impedance Monitoring > status = " + str(response.value))   
      return response.value

   def StopImpedanceMonitoring(self) -> bool: 
      ''' Stop an ongoing impedance monitoring measurement

         Parameters:
            -

         Returns:
            bool: true if the function succeeds
         '''
      response = self.__stub.StopImpedanceMonitoring(contracts_pb2.EmptyMessage())
      self.__PrintInfo(" Stop Impedance Monitoring > status = " + str(response.value))   
      return response.value

   def CreateBatchProgram(self, name: str) -> int:
      ''' Create an new empty BatchProgram. This BatchProgram will be the active one

         Parameters:
            name (str): name of the batch program

         Returns:
            int: id of the BatchSweepRefMap, use this to add items
         '''
      batchProgSettings = contracts_pb2.BatchProgramNew()
      batchProgSettings.name = name
      response = self.__stub.CreateBatchProgram(batchProgSettings)
      self.__PrintInfo(" Create Batch Program > id = " + str(response.value))   
      return response.value

   def SetBatchProgramActive(self, id: int) -> int:
      ''' Set a BatchProgram to be the active one

         Parameters:
            id (int): id of a batch program

         Returns:
            bool: true if the function succeeds
         '''
      batchProgSettings = contracts_pb2.Id(value = id)
      response = self.__stub.SetBatchProgramActive(batchProgSettings)
      self.__PrintInfo(" Set Batch Program Active > status = " + str(response.value))   
      return response.value

   def CreateBatchSweepCfgMap(self, lstCfgMapId: list[int], sweepmuxes: bool, parentId: int) -> int:
      ''' Create a CfgMap Batch sweep

         Parameters:
            lstCfgMapId: list[int]: list of CfgMap id, as created with CreatePixelConfiguration

            sweepmuxes (bool): if true, repeat the timeline for each of the 4 electrodes of a pixel.

            parentId (int): id of the parent item
         
         Returns:
            int: id of the BatchSweepMuxMap, use this to add items
         '''
      sweepData = contracts_pb2.BatchSweepCfgMap()
      sweepData.lstCfgMapId.extend(lstCfgMapId)
      sweepData.sweepmuxes = sweepmuxes
      sweepData.parentId = parentId
      response = self.__stub.CreateBatchSweepCfgMap(sweepData)
      self.__PrintInfo(" Create Batch Sweep CfgMap > status = " + str(response.value))   
      return response.value

   def CreateBatchSweepMuxMap(self, lstMuxMapId: list[int], parentId: int) -> int:
      ''' Create a MuxMap Batch sweep

         Parameters:
            lstMuxMapId: list[int]: list of MuxMap id, as created with CreateMuxMap

            parentId (int): id of the parent item
         
         Returns:
            int: id of the BatchSweepMuxMap, use this to add items
         '''
      sweepData = contracts_pb2.BatchSweepMuxMap()
      sweepData.lstMuxMapId.extend(lstMuxMapId)
      sweepData.parentId = parentId
      response = self.__stub.CreateBatchSweepMuxMap(sweepData)
      self.__PrintInfo(" Create Batch Sweep MuxMap > status = " + str(response.value))   
      return response.value

   def CreateBatchSweepRefMap(self, lstRefMapId: list[int], parentId: int) -> int:
      ''' Create a RefMap Batch sweep

         Parameters:
            lstRefMapId: list[int]: list of RefMap id, as created with CreateRefElectrodeMap

            parentId (int): id of the parent item
         
         Returns:
            int: id of the BatchSweepRefMap, use this to add items
         '''
      sweepData = contracts_pb2.BatchSweepRefMap()
      sweepData.lstRefMapId.extend(lstRefMapId)
      sweepData.parentId = parentId
      response = self.__stub.CreateBatchSweepRefMap(sweepData)
      self.__PrintInfo(" Create Batch Sweep RefMap > status = " + str(response.value))   
      return response.value

   def CreateBatchSweepVStim(self, idVStim, lstVStimConfiguration: list[contracts_pb2.VStimConfiguration], parentId: int) -> int:
      ''' Create a V-stimulation Batch sweep

         Parameters:
            idVStim (int): id of V-stim definition to be used

            lstVStimConfiguration (list[contracts_pb2.VStimConfiguration]): list of VStimConfigurations, as created with CreateVStimConfigurationObject

            parentId (int): id of the parent item
         
         Returns:
            int: id of the BatchSweepVStim, use this to add items
         '''
      sweepData = contracts_pb2.BatchSweepVStimSettings()
      sweepData.idVStim = idVStim;
      sweepData.lstVStimConfiguration.extend(lstVStimConfiguration)
      sweepData.parentId = parentId
      response = self.__stub.CreateBatchSweepVStim(sweepData)
      self.__PrintInfo(" Create Batch Sweep VStim )) > status = " + str(response.value))   
      return response.value

   def CreateVStimConfigurationObject (self, name, pulse1VoltagemV: float, pulse2VoltagemV: float, pulse1DurationmS: int, pulse2DurationmS: int, pulseTotalDurationmS: int) -> contracts_pb2.VStimConfiguration:
      ''' Create a V-stimulation Configuration, to be used with CreateBatchSweepVStim

         Parameters:
            name (str): reference name

            pulse1VoltagemV (float): pulse strength in milliVolt

            pulse2VoltagemV (float): pulse strengthin milliVolt

            pulse1DurationmS (int): pulse duration in ms

            pulse2DurationmS (int): pulse duration in ms

            pulseTotalDurationmS (int): total duration in ms
         
         Returns:
            contracts_pb2.VStimConfiguration: V-stimulation Configuration, use this with function CreateBatchSweepVStim
         '''
      vStim = contracts_pb2.VStimConfiguration()
      vStim.name = name
      vStim.Pulse1VoltagemV = pulse1VoltagemV
      vStim.Pulse2VoltagemV = pulse2VoltagemV
      vStim.Pulse1DurationmS = pulse1DurationmS
      vStim.Pulse2DurationmS = pulse2DurationmS
      vStim.PulseTotalDurationmS = pulseTotalDurationmS
      return vStim

   def CreateBatchSweepIStim(self, idIStim, lstIStimConfiguration: list[contracts_pb2.IStimConfiguration], parentId: int) -> int:
      ''' Create I-stim sweep

         Parameters:
            idIStim (int): id of I-stim definition to be used

            lstIStimConfiguration (list[contracts_pb2.IStimConfiguration]): list of IStimConfiguration objects, see function 'CreateIStimConfigurationObject'

            parentId (int): id of the parent item
      
         Returns:
            int: id of the BatchSweepIStim, use this to add items
         '''
      sweepData = contracts_pb2.BatchSweepIStimSettings()
      sweepData.idIStim = idIStim;
      sweepData.lstIStimConfiguration.extend(lstIStimConfiguration)
      sweepData.parentId = parentId
      response = self.__stub.CreateBatchSweepIStim(sweepData)
      self.__PrintInfo(" Create Batch Sweep IStim )) > status = " + str(response.value))   
      return response.value

   def CreateIStimConfigurationObject (self, name: str, currentStepValue: IStepValues, pulse1CurrentpA: float, pulse2CurrentpA: float, pulse1DurationmS: int, pulse2DurationmS: int, pulseTotalDurationmS) -> contracts_pb2.IStimConfiguration:
      ''' Create an I-stimulation Configuration, to be used with CreateBatchSweepIStim

         Parameters:
            name (str): reference name

            currentStepValue (IStepValues): current step size

            pulse1CurrentpA (float): in picoA

            pulse2CurrentpA (float): in picoA

            pulse1DurationmS (int): in ms

            pulse2DurationmS (int): in ms

            pulseTotalDurationmS (int): in ms
      
         Returns:
            contracts_pb2.IStimConfiguration: I-stimulation Configuration, use this with function CreateBatchSweepIStim
         '''
      iStim = contracts_pb2.IStimConfiguration()
      iStim.name = name
      iStim.CurrentStepValue = currentStepValue
      iStim.Pulse1CurrentpA = pulse1CurrentpA
      iStim.Pulse2CurrentpA = pulse2CurrentpA
      iStim.Pulse1DurationmS = pulse1DurationmS
      iStim.Pulse2DurationmS = pulse2DurationmS
      iStim.PulseTotalDurationmS = pulseTotalDurationmS
      return iStim

   def CreateBatchSweepRec(self, idRec, lstRecConfiguration: list[contracts_pb2.RecConfiguration], parentId: int) -> int:
      ''' Create Recording sweep

         Parameters:
            idRec (int): id of recording definition to be used

            lstRecConfiguration (list[contracts_pb2.RecConfiguration]): list of RecConfiguration objects, see function 'CreateRecConfigurationObject'

            parentId (int): id of the parent item
      
         Returns:
            int: id of the BatchSweepRec, use this to add items
         '''
      sweepData = contracts_pb2.BatchSweepRecSettings()
      sweepData.idRec = idRec
      sweepData.lstRecConfiguration.extend(lstRecConfiguration)
      sweepData.parentId = parentId
      response = self.__stub.CreateBatchSweepRec(sweepData)
      self.__PrintInfo(" Create Batch Sweep Rec)) > id = " + str(response.value))   
      return response.value

   def CreateRecConfigurationObject (self, name: str, enableLowPassFilter: bool, gain: RecGain) -> contracts_pb2.RecConfiguration:
      ''' Create Recording Configuration, to be used with CreateBatchSweepRec

         Parameters:
            name (str): reference name

            enableLowPassFilter (bool): if true, low pass filter is enabled

            gain (RecGain): Select gain from Gain1 to Gain60
   
         Returns:
            contracts_pb2.RecConfiguration: Recording Configuration, use this with function CreateBatchSweepRec
         '''
      recMode = contracts_pb2.RecConfiguration()
      recMode.name = name
      recMode.EnableLowPassFilter = enableLowPassFilter
      recMode.Gain = gain
      return recMode

   def CreateTimeLine(self, parentId: int) -> int:
      ''' Create TimeLine

         Parameters:
            parentId (int): id of the parent item

         Returns:
            int: id of the TimeLine, use this to add items to the TimeLine
         '''
      timeLineSettings = contracts_pb2.TimeLineSettings()
      timeLineSettings.parentId = parentId
      response = self.__stub.CreateTimeLine(timeLineSettings)
      self.__PrintInfo(" Create TimeLine)) > id = " + str(response.value))   
      return response.value

   def CreateTimeLineDelay(self, delayMs: int, parentId: int) -> bool:
      ''' Create Delay in a TimeLine

         Parameters:
            delayMs (int): delay in ms

            parentId (int): id of the TimeLine

         Returns:
            bool: Return True if successful
         '''
      settings = contracts_pb2.TimeLineDelaySettings()
      settings.delayMs = delayMs
      settings.parentId = parentId
      response = self.__stub.CreateTimeLineDelay(settings)
      self.__PrintInfo(" Create TimeLine Delay > status = " + str(response.value))   
      return response.value

   def CreateTimeLineStimulationEvent(self, stimulationMode: StimulationMode, pulsePolarity: PulsePolarity, pulseCount:int, parentId: int) -> bool:
      ''' Create StimulationEvent in a TimeLine

         Parameters:
            stimulationMode (StimulationMode): Choose for Voltage, Current or VoltageAndCurrent

            pulsePolarity (PulsePolarity)

            pulseCount (int): nr of pulses

            parentId (int): id of the TimeLine

         Returns:
            bool: Return True if successful
         '''
      settings = contracts_pb2.TimeLineStimulationEventSettings()
      settings.stimulationMode = stimulationMode
      settings.pulsePolarity = pulsePolarity
      settings.pulseCount = pulseCount
      settings.parentId = parentId
      response = self.__stub.CreateTimeLineStimulationEvent(settings)
      self.__PrintInfo(" Create TimeLine Stimulation Event > status = " + str(response.value))   
      return response.value

   def CreateTimelineRepeat(self, nrRepeats: int, parentId: int) -> int:
      ''' Create Repeat loop in a TimeLine

         Parameters:
            nrRepeats (int): nr of repeats

            parentId (int): id of the TimeLine

         Returns:
            int: id of the TimeLine in the , use this to add items to the TimeLine
         '''
      settings = contracts_pb2.TimelineRepeatSettings()
      settings.nrRepeats = nrRepeats
      settings.parentId = parentId
      response = self.__stub.CreateTimelineRepeat(settings)
      self.__PrintInfo(" Create Timeline Repeat)) > id = " + str(response.value))   
      return response.value

   def CreateTimelineImpedanceMonitor(self, frequency: ImpMonFrequency, amplitude: ImpMonAmplitude, parentId: int ) -> int:
      ''' Create ImpedanceMonitor in a TimeLine

         Parameters:
            frequency (ImpMonFrequency): Frequency1kHz or Frequency10kHz

            amplitude (ImpMonAmplitude): Amplitude1nA or Amplitude10nA

            parentId (int): id of the TimeLine

         Returns:
            int: id of the TimeLine in the , use this to add items to the TimeLine
         '''
      settings = contracts_pb2.TimelineImpedanceMonitorSettings()
      settings.frequency = frequency
      settings.amplitude = amplitude
      settings.parentId = parentId
      response = self.__stub.CreateTimelineImpedanceMonitor(settings)
      self.__PrintInfo(" Create Timeline Impedance Monitor > id = " + str(response.value))   
      return response.value  

   # TimelineImpedanceMonitor automatically contains TimelineSliceDefinition with ZMon Processor (=Impedance Monitor)
   def CreateTimelineSliceDefinition(self, lstProcessors: list[Processor], parentId: int) -> int:
      ''' Create SliceDefinition in a Timeline

         Parameters:
            lstProcessors (list[Processor]): List with one or more Processors
                        
            parentId (int): id of the TimeLine

         Returns:
            int: id of the TimeLine in the , use this to add items to the TimeLine
         '''
      settings = contracts_pb2.TimelineSliceDefinitionSettings()
      settings.processors.extend(lstProcessors)
      settings.parentId = parentId
      response = self.__stub.CreateTimelineSliceDefinition(settings)
      self.__PrintInfo(" Create Timeline Slice Definition > id = " + str(response.value))   
      return response.value

   def GetErrorInfo(self, nrErrorMsgs: int) -> list[contracts_pb2.ErrorInfo]: 
      ''' Get Error Info

         Parameters:
            nrErrorMsgs (int): Accepts 0 to 100. If 0 is passed, only the error messages related to the last function call are returned. Otherwise the number of requested error messages is returned. The returned list can be shorter, depending on the nr of available messages. The maximum is 100.
         
         Returns:
            list[contracts_pb2.ErrorInfo]: A list of ErrorInfo objects
         '''

      settings = contracts_pb2.ErrorInfoRequest()
      settings.nrOfMsg = nrErrorMsgs
      response = self.__stub.GetErrorInfo(settings)
      self.__PrintInfo(" Get Error Info > nr msgs = " + str(len(response.errorInfo)))   
      return response.errorInfo
   
   def SetRecordWaitTimesOnOff(self, onOff: bool) -> bool:
      ''' Set Record WaitTimes OnOff

         Parameters:
            onOff (bool): Select whether waiting times in a program, have to be recorded or not.
         
         Returns:
            bool: true if the function succeeds
         '''

      settings = contracts_pb2.RecordWaitTimesOnOffSettings()
      settings.onOff = onOff
      response = self.__stub.SetRecordWaitTimesOnOff(settings)
      self.__PrintInfo(" Set Record WaitTimes OnOff > status = " + str(response.value))   
      return response.value

