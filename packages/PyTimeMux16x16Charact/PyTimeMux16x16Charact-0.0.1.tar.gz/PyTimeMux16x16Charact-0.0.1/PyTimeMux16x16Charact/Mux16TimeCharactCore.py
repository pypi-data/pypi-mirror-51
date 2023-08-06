# -*- coding: utf-8 -*-
"""
Created on Tue Oct 09 11:19:55 2018

@author: Javier
"""

import sys
import ctypes
import PyGFET.DataStructures as PyData
import PyDAQmx as Daq
from ctypes import byref, c_int32
import numpy as np
from scipy import signal

###############################################################################
######
###############################################################################


def GetDevName():
    print('ReadAnalog GetDevName')
    # Get Device Name of Daq Card
    n = 1024
    buff = ctypes.create_string_buffer(n)
    Daq.DAQmxGetSysDevNames(buff, n)
    if sys.version_info >= (3,):
        value = buff.value.decode()
    else:
        value = buff.value

    Dev = None
    value = value.replace(' ', '')
    for dev in value.split(','):
        if dev.startswith('Sim'):
            continue
        Dev = dev + '/{}'

    if Dev is None:
        print 'ERRROORR dev not found ', value

    return Dev


class ReadAnalog(Daq.Task):

    '''
    Class to read data from Daq card

    TODO - Implement the callback option to read data
    '''

#    Events list
    EveryNEvent = None
    DoneEvent = None

    ContSamps = False
    EverySamps = 1000

    def __init__(self, InChans, Range=5.0):

        Daq.Task.__init__(self)
        self.Channels = InChans

        Dev = GetDevName()
        for Ch in self.Channels:
            self.CreateAIVoltageChan(Dev.format(Ch), "",
                                     Daq.DAQmx_Val_RSE,
                                     -Range, Range,
                                     Daq.DAQmx_Val_Volts, None)

        self.AutoRegisterDoneEvent(0)

    def ReadData(self, Fs=1000, nSamps=10000, EverySamps=1000):

        self.Fs = Fs
        self.EverySamps = EverySamps

        self.data = np.ndarray([len(self.Channels), ])

        self.CfgSampClkTiming("", Fs, Daq.DAQmx_Val_Rising,
                              Daq.DAQmx_Val_FiniteSamps, nSamps)

        self.AutoRegisterEveryNSamplesEvent(Daq.DAQmx_Val_Acquired_Into_Buffer,
                                            self.EverySamps, 0)
        self.StartTask()

    def ReadContData(self, Fs=1000, EverySamps=1000):

        self.Fs = Fs
        self.EverySamps = np.int32(EverySamps)
        self.ContSamps = True  # TODO check it

        self.CfgSampClkTiming("", Fs, Daq.DAQmx_Val_Rising,
                              Daq.DAQmx_Val_ContSamps, self.EverySamps*100)

        self.AutoRegisterEveryNSamplesEvent(Daq.DAQmx_Val_Acquired_Into_Buffer,
                                            self.EverySamps, 0)

        self.StartTask()

    def StopContData(self):
        self.StopTask()
        self.ContSamps = False

    def EveryNCallback(self):
        read = c_int32()
        data = np.zeros((self.EverySamps, len(self.Channels)))
        self.ReadAnalogF64(self.EverySamps, 10.0,
                           Daq.DAQmx_Val_GroupByScanNumber,
                           data, data.size, byref(read), None)

        if not self.ContSamps:  # TODO check why stack here
            self.data = np.vstack((self.data, data))

        if self.EveryNEvent:
            self.EveryNEvent(data)

    def DoneCallback(self, status):
        self.StopTask()
        self.UnregisterEveryNSamplesEvent()

        if self.DoneEvent:
            self.DoneEvent(self.data[1:, :])  # TODO check why 1:

        return 0  # The function should return an integer

###############################################################################
#####
###############################################################################


class WriteAnalog(Daq.Task):

    '''
    Class to write data to Daq card
    '''
    def __init__(self, Channels):

        Daq.Task.__init__(self)
        Dev = GetDevName()
        for Ch in Channels:
            self.CreateAOVoltageChan(Dev.format(Ch), "",
                                     -5.0, 5.0, Daq.DAQmx_Val_Volts, None)
        self.DisableStartTrig()
        self.StopTask()

    def SetVal(self, value):

        self.StartTask()
        self.WriteAnalogScalarF64(1, -1, value, None)
        self.StopTask()

    def SetSignal(self, Signal, nSamps):

        read = c_int32()

        self.CfgSampClkTiming('ai/SampleClock', 1, Daq.DAQmx_Val_Rising,
                              Daq.DAQmx_Val_FiniteSamps, nSamps)

        self.CfgDigEdgeStartTrig('ai/StartTrigger', Daq.DAQmx_Val_Rising)
        self.WriteAnalogF64(nSamps, False, -1, Daq.DAQmx_Val_GroupByChannel,
                            Signal, byref(read), None)
        self.StartTask()

    def SetContSignal(self, Signal, nSamps):
        read = c_int32()

        self.CfgSampClkTiming('ai/SampleClock', 1, Daq.DAQmx_Val_Rising,
                              Daq.DAQmx_Val_ContSamps, nSamps)

        self.CfgDigEdgeStartTrig('ai/StartTrigger', Daq.DAQmx_Val_Rising)
        self.WriteAnalogF64(nSamps, False, -1, Daq.DAQmx_Val_GroupByChannel,
                            Signal, byref(read), None)
        self.StartTask()

###############################################################################
#####
###############################################################################


class WriteDigital(Daq.Task):

    '''
    Class to write data to Daq card
    '''
    def __init__(self, Channels):
        Daq.Task.__init__(self)
        Dev = GetDevName()
        for Ch in Channels:
            self.CreateDOChan(Dev.format(Ch), "",
                              Daq.DAQmx_Val_ChanForAllLines)

        self.DisableStartTrig()
        self.StopTask()

    def SetDigitalSignal(self, Signal):
        Sig = np.array(Signal, dtype=np.uint8)
        self.WriteDigitalLines(1, 1, 10.0, Daq.DAQmx_Val_GroupByChannel,
                               Sig, None, None)


###############################################################################
#####
###############################################################################

class ChannelsConfig():
    # Daq card connections mapping 'Chname' : (DCout, ACout)
    aiChannels = {'Ch01': ('ai0', 'ai8'),
                  'Ch02': ('ai1', 'ai9'),
                  'Ch03': ('ai2', 'ai10'),
                  'Ch04': ('ai3', 'ai11'),
                  'Ch05': ('ai4', 'ai12'),
                  'Ch06': ('ai5', 'ai13'),
                  'Ch07': ('ai6', 'ai14'),
                  'Ch08': ('ai7', 'ai15'),
                  'Ch09': ('ai16', 'ai24'),
                  'Ch10': ('ai17', 'ai25'),
                  'Ch11': ('ai18', 'ai26'),
                  'Ch12': ('ai19', 'ai27'),
                  'Ch13': ('ai20', 'ai28'),
                  'Ch14': ('ai21', 'ai29'),
                  'Ch15': ('ai22', 'ai30'),
                  'Ch16': ('ai23', 'ai31')}

    # Daq card digital connections mapping 'Column name':(VsControl, VdControl)
    doColumns = {'Col01': ('line1', ),
                 'Col02': ('line2', ),
                 'Col03': ('line3', ),
                 'Col04': ('line0', ),
                 'Col05': ('line5', ),
                 'Col06': ('line7', ),
                 'Col07': ('line6', ),
                 'Col08': ('line4', ),
                 'Col09': ('line8', ),
                 'Col10': ('line11', ),
                 'Col11': ('line10', ),
                 'Col12': ('line9', ),
                 'Col13': ('line12', ),
                 'Col14': ('line15', ),
                 'Col15': ('line14', ),
                 'Col16': ('line13', ),
                 }



# ChannelIndex = {'Ch01': (0-31, 0-15)}-->> {Chname: (input index, sort index)}
    DCChannelIndex = None
    ACChannelIndex = None
    GateChannelIndex = None

    ChNamesList = None
    # ReadAnalog class with all channels
    Inputs = None
    InitConfig = None

    # Events list
    DCDataDoneEvent = None
    DCDataEveryNEvent = None
    ACDataDoneEvent = None
    ACDataEveryNEvent = None
    GateDataDoneEvent = None
    GateDataEveryNEvent = None

    def DelInputs(self):
        self.Inputs.ClearTask()

    def InitInputs(self, Channels, GateChannel=None, Configuration='Both'):
        if self.Inputs is not None:
            self.DelInputs()

        InChans = []

        self.ChNamesList = sorted(Channels)
        self.DCChannelIndex = {}
        self.ACChannelIndex = {}
        index = 0
        sortindex = 0
        for ch in sorted(Channels):
            if Configuration in ('DC', 'Both'):
                InChans.append(self.aiChannels[ch][0])
                self.DCChannelIndex[ch] = (index, sortindex)
                index += 1
            if Configuration in ('AC', 'Both'):
                InChans.append(self.aiChannels[ch][1])
                self.ACChannelIndex[ch] = (index, sortindex)
                index += 1
            sortindex += 1

        if GateChannel:
            self.GateChannelIndex = {GateChannel: (index, 0)}
            InChans.append(self.aiChannels[GateChannel][0])
        else:
            self.GateChannelIndex = None

        print 'Channels configurtation'
        print 'Gate', self.GateChannelIndex
        print 'Channels ', len(self.ChNamesList)
        for ch in sorted(Channels):
            if Configuration == 'DC':
                print(ch, ' DC -> ',
                      self.aiChannels[ch][0], self.DCChannelIndex[ch])
                self.ACChannelIndex = self.DCChannelIndex
            elif Configuration == 'AC':
                print(ch, ' AC -> ',
                      self.aiChannels[ch][1], self.ACChannelIndex[ch])
                self.DCChannelIndex = self.ACChannelIndex
            else:
                print(ch, ' DC -> ',
                      self.aiChannels[ch][0], self.DCChannelIndex[ch])
                print(ch, ' AC -> ',
                      self.aiChannels[ch][1], self.ACChannelIndex[ch])

        self.Inputs = ReadAnalog(InChans=InChans)
        # events linking
        self.Inputs.EveryNEvent = self.EveryNEventCallBack
        self.Inputs.DoneEvent = self.DoneEventCallBack

    def InitDigitalChannels(self, DigColumns=None):
        self.ClearSig = np.zeros((1, len(DigColumns)),
                                 dtype=np.bool).astype(np.uint8)
        DOChannels = []
        self.DigColumns = sorted(DigColumns)

        for digc in sorted(self.DigColumns):
            DOChannels.append(self.doColumns[digc][0])
#            DOChannels.append(self.doColumns[digc][1])

        self.ColumnsControl = WriteDigital(Channels=DOChannels)

        ChannelNames = []
        for nRow in range(len(self.ChNamesList)):
            for nCol in range(len(DigColumns)):
                ChannelNames.append(self.ChNamesList[nRow]+DigColumns[nCol])
        self.ChannelNames = sorted(ChannelNames)

    def __init__(self, Channels, GateChannel=None, Configuration='Both',
                 ChVg='ao2', ChVs='ao1', ChVds='ao0', ChVsig='ao3'):

        self.InitConfig = {}
        self.InitConfig['Channels'] = Channels
        self.InitConfig['GateChannel'] = GateChannel
        self.InitConfig['Configuration'] = Configuration

        self.InitInputs(Channels=Channels,
                        GateChannel=GateChannel,
                        Configuration=Configuration)

        # Output Channels
        self.VsOut = WriteAnalog((ChVs,))
        self.VdsOut = WriteAnalog((ChVds,))
        self.VgOut = WriteAnalog((ChVg,))

    def SetBias(self, Vds, Vgs):
        print 'ChannelsConfig SetBias Vgs ->', Vgs, 'Vds ->', Vds
        self.VdsOut.SetVal(Vds)
        self.VsOut.SetVal(-Vgs)
        self.BiasVd = Vds-Vgs
        self.Vgs = Vgs
        self.Vds = Vds

    def SetSignal(self, Signal, nSamps):
        if not self.VgOut:
            self.VgOut = WriteAnalog(('ao2',))
        self.VgOut.DisableStartTrig()
        self.VgOut.SetSignal(Signal=Signal,
                             nSamps=nSamps)

    def GenerateDigitalSignal(self):
        DOut = np.array([], dtype=np.bool)

        for nCol in range(len(self.DigColumns)):
            Lout = np.zeros((1, len(self.DigColumns)), dtype=np.bool)
            Lout[0, nCol:  (nCol + 1)] = True
            Cout = np.vstack((Lout))
#            Cout = np.vstack((Lout, ~Lout))
            DOut = np.vstack((DOut, Cout)) if DOut.size else Cout

        DOut.astype(np.uint8)

        return DOut.astype(np.uint8)

    def _SortChannels(self, data, SortDict):
        (samps, inch) = data.shape
        sData = np.zeros((samps, len(SortDict)))
        for chn, inds in SortDict.iteritems():
            sData[:, inds[1]] = data[:, inds[0]]
        return sData

    def EveryNEventCallBack(self, Data):
        _DCDataEveryNEvent = self.DCDataEveryNEvent
        _GateDataEveryNEvent = self.GateDataEveryNEvent
        _ACDataEveryNEvent = self.ACDataEveryNEvent

        if _GateDataEveryNEvent:
            _GateDataEveryNEvent(self._SortChannels(Data,
                                                    self.GateChannelIndex))
        if _DCDataEveryNEvent:
            _DCDataEveryNEvent(self._SortChannels(Data,
                                                  self.DCChannelIndex))
        if _ACDataEveryNEvent:
            _ACDataEveryNEvent(self._SortChannels(Data,
                                                  self.ACChannelIndex))

    def DoneEventCallBack(self, Data):
        if self.VgOut:
            self.VgOut.StopTask()

        _DCDataDoneEvent = self.DCDataDoneEvent
        _GateDataDoneEvent = self.GateDataDoneEvent
        _ACDataDoneEvent = self.ACDataDoneEvent

        if _GateDataDoneEvent:
            _GateDataDoneEvent(self._SortChannels(Data,
                                                  self.GateChannelIndex))
        if _DCDataDoneEvent:
            _DCDataDoneEvent(self._SortChannels(Data,
                                                self.DCChannelIndex))
        if _ACDataDoneEvent:
            _ACDataDoneEvent(self._SortChannels(Data,
                                                self.ACChannelIndex))

    def ReadChannelsData(self, Fs=1000, nSamps=10000, EverySamps=1000):
        self.Inputs.ReadData(Fs=Fs,
                             nSamps=nSamps,
                             EverySamps=EverySamps)

    def __del__(self):
        print 'Delete class'
        if self.VgOut:
            self.VgOut.ClearTask()
        self.VdsOut.ClearTask()
        self.VsOut.ClearTask()
        self.Inputs.ClearTask()

###############################################################################
#####
###############################################################################


class FFTConfig():
    Freqs = None
    Fs = None
    nFFT = None
    Finds = None
    AcqSequential = False


class FFTTestSignal():

    FsH = 2e6
    FsL = 1000
    FMinLow = 1  # Lowest freq to acquire in 1 time
    FThres = 10  # For two times adq split freq

    FFTconfs = [FFTConfig(), ]

    Fsweep = None
    FFTAmps = None

    BodeDuration = [None, None]
    Vpp = [None, None]
    AddnFFT = 2
    nAvg = 2
    Arms = 1e-3
    EventFFTDebug = None

    def __init__(self, FreqMin, FreqMax, nFreqs, Arms, nAvg):

        self.nAvg = nAvg
        self.Arms = Arms

        if FreqMax > self.FsH/2:
            FreqMax = self.FsH/2 - 1

        if FreqMax <= self.FThres:
            FreqMax = self.FThres + 1

        fsweep = np.logspace(np.log10(FreqMin), np.log10(FreqMax), nFreqs)
        if np.any(fsweep < self.FMinLow) and nFreqs > 1:  # TODO Check this
            self.FFTconfs.append(FFTConfig())

            self.FFTconfs[0].nFFT = int(2**((np.around(np.log2(self.FsH/self.FThres))+1)+self.AddnFFT))
            self.FFTconfs[1].nFFT = int(2**((np.around(np.log2(self.FsL/FreqMin))+1)+self.AddnFFT))
            self.FFTconfs[0].Fs = self.FsH
            self.FFTconfs[1].Fs = self.FsL

            # LowFrequencies
            FreqsL, indsL = self.CalcCoherentSweepFreqs(FreqMin=FreqMin,
                                                        FreqMax=np.max(fsweep[np.where(self.FThres>fsweep)]),
                                                        nFreqs=np.sum(fsweep < self.FThres),
                                                        Fs=self.FFTconfs[1].Fs,
                                                        nFFT=self.FFTconfs[1].nFFT)

            # HighFrequencies
            FreqsH, indsH = self.CalcCoherentSweepFreqs(FreqMin=np.min(fsweep[np.where(fsweep>self.FThres)]),
                                                        FreqMax=FreqMax,
                                                        nFreqs=np.sum(self.FThres < fsweep),
                                                        Fs=self.FFTconfs[0].Fs,
                                                        nFFT=self.FFTconfs[0].nFFT)
            self.FFTconfs[0].Finds = indsH
            self.FFTconfs[0].Freqs = FreqsH

            self.FFTconfs[1].Finds = indsL
            self.FFTconfs[1].Freqs = FreqsL

            self.Fsweep = np.hstack((self.FFTconfs[1].Freqs,
                                     self.FFTconfs[0].Freqs))

            self.FFTconfs[0].AcqSequential = True

            self.BodeDuration = [self.FFTconfs[0].nFFT*(1/float(self.FFTconfs[0].Fs))*self.nAvg,
                                 self.FFTconfs[1].nFFT*(1/float(self.FFTconfs[1].Fs))*self.nAvg]

        else:
            if len(self.FFTconfs) > 1:
                del(self.FFTconfs[1])
            self.FFTconfs[0].nFFT = int(2**((np.around(np.log2(self.FsH/FreqMin))+1)+self.AddnFFT))
            self.FFTconfs[0].Fs = self.FsH

            FreqsH, indsH = self.CalcCoherentSweepFreqs(FreqMin=FreqMin,
                                                        FreqMax=FreqMax,
                                                        nFreqs=nFreqs,
                                                        Fs=self.FFTconfs[0].Fs,
                                                        nFFT=self.FFTconfs[0].nFFT)
            self.FFTconfs[0].Finds = indsH
            self.FFTconfs[0].Freqs = FreqsH

            self.Fsweep = self.FFTconfs[0].Freqs
            self.FFTconfs[0].AcqSequential = True
            self.BodeDuration = [self.FFTconfs[0].nFFT*(1/float(self.FFTconfs[0].Fs))*self.nAvg, None]

    def CalcCoherentSweepFreqs(self, FreqMin, FreqMax, nFreqs, Fs, nFFT):
        nmin = (FreqMin*(nFFT))/Fs
        nmax = (FreqMax*(nFFT))/Fs
        freqs = np.round(
                np.logspace(np.log10(nmin), np.log10(nmax), nFreqs), 0)
        Freqs = (float(Fs)/(nFFT))*np.unique(freqs)

        # Calc Indexes
        freqs = np.fft.rfftfreq(nFFT, 1/float(Fs))
#        freqs = [np.round(x, 7) for x in freq]
#        Freqs = [np.round(x, 7) for x in Freqs]
#        freqs = np.array(freqs)
#        Freqs = np.array(Freqs)
        Inds = np.where(np.in1d(freqs, Freqs))[0]

        return Freqs, Inds

    def GenSignal(self, Ind=0, Delay=0):

        FFTconf = self.FFTconfs[Ind]

        Ts = 1/float(FFTconf.Fs)
        Ps = FFTconf.nFFT * self.nAvg * Ts

        Amp = self.Arms*np.sqrt(2)
        t = np.arange(0, Ps, Ts) + Delay
        out = np.zeros(t.size)
        for f in np.nditer(FFTconf.Freqs):
            s = Amp*np.sin(f*2*np.pi*(t))
            out = out + s

        self.FFTAmps = (2*np.fft.rfft(
                out, FFTconf.nFFT)/FFTconf.nFFT)[FFTconf.Finds]
        self.Vpp[Ind] = np.max(out) + np.abs(np.min(out))
#        self.FFTconfs[Ind].Vpp = np.max(out) + np.abs(np.min(out))

        out[-1] = 0

        return out, t

    def CalcFFT(self, Data, Ind):
        FFTconf = self.FFTconfs[Ind]

        a = Data.reshape((self.nAvg, FFTconf.nFFT))
        acc = np.zeros(((FFTconf.nFFT/2)+1))
        for w in a:
            acc = acc + (2 * np.fft.rfft(w, FFTconf.nFFT) / FFTconf.nFFT)

        Out = (acc/self.nAvg)[FFTconf.Finds]

        if self.EventFFTDebug is not None:
            self.EventFFTDebug(acc/self.nAvg)

        return Out

###############################################################################
#####
###############################################################################


class FFTBodeAnalysis():

    BodeRh = None
    BodeRhardware = 150e3
    BodeSignal = None
    RemoveDC = None

    AdqDelay = -5.8e-7

    def SetBodeConfig(self, FreqMin=0.1, FreqMax=15000, nFreqs=10, Arms=10e-3,
                      nAvg=1, BodeRh=False, BodeOut=False, RemoveDC=False):

        self.BodeSignal = FFTTestSignal(FreqMin=FreqMin,
                                        FreqMax=FreqMax,
                                        nFreqs=nFreqs,
                                        Arms=Arms,
                                        nAvg=nAvg)

        self.BodeRh = BodeRh
        self.BodeOut = BodeOut
        self.RemoveDC = RemoveDC

    def SetContSig(self, FreqMin=0.1, FreqMax=15000, nFreqs=10, Arms=10e-3):

        self.ContSig = FFTTestSignal(FreqMin=FreqMin,
                                     FreqMax=FreqMax,
                                     nFreqs=nFreqs,
                                     Arms=Arms,
                                     nAvg=1)
        self.ContSig.FMinLow = None
        self.ContSig.FsH = 1000
        self.ContSig.__init__(FreqMin=FreqMin,
                              FreqMax=FreqMax,
                              nFreqs=nFreqs,
                              Arms=Arms,
                              nAvg=1)

    def CalcBode(self, Data, Ind, IVGainAC, ChIndexes):

        if self.BodeRh or self.BodeOut:
            x = Data
        else:
            x = Data / IVGainAC

        if self.RemoveDC:

            for chk, chi, in sorted(ChIndexes.iteritems()):
                Data[:, chi[1]] = Data[:, chi[1]] - np.mean(Data[:, chi[1]])

        FFTconf = self.BodeSignal.FFTconfs[Ind]

        (samps, inch) = x.shape
        Gm = np.ones((len(FFTconf.Finds),
                      inch))*np.complex(np.nan)

        for chk, chi, in sorted(ChIndexes.iteritems()):
            Out = self.BodeSignal.CalcFFT(Data=x[:, chi[1]],
                                          Ind=Ind)

#            Delay = self.AdqDelay*chi[0]  ## TODO check this time finer
            self.BodeSignal.GenSignal(Ind=Ind, Delay=self.AdqDelay)

            if self.BodeRh:
                Iin = -self.BodeSignal.FFTAmps/self.BodeRhardware
                gm = Out/Iin
                Gm[:, chi[1]] = gm
            else:
                Gm[:, chi[1]] = Out/self.BodeSignal.FFTAmps

        return Gm


###############################################################################
#####
###############################################################################


class DataProcess(ChannelsConfig, FFTBodeAnalysis):

    # Variables list Continuous
    DCFs = 1000
    DCnSamps = 1000
    IVGainDC = 10e3
    IVGainAC = 1e6
    IVGainGate = 2e6
    DevCondition = 5e-8

    # Variables list Charact
    PSDDuration = None
    GenTestSig = None
    ContSig = None
    OldConfig = None
    GmH = None
    Gm = None
    iConf = 0
    SeqIndex = 0

    # Events list Continuous
    EventContAcDone = None
    EventContDcDone = None
    EventContGateDone = None

    # Events list Charact
    EventBiasDone = None
    EventBiasAttempt = None
    EventBodeDone = None
    EventPSDDone = None
    EventAcDataAcq = None
    EventSetBodeLabel = None

    def ClearEventsCallBacks(self):
        self.DCDataDoneEvent = None
        self.DCDataEveryNEvent = None
        self.ACDataDoneEvent = None
        self.ACDataEveryNEvent = None
        self.GateDataDoneEvent = None
        self.GateDataEveryNEvent = None

    # DC
    def GetBiasCurrent(self, Vds, Vgs):
        self.ClearEventsCallBacks()
        self.SetBias(Vds, Vgs)
        self.DCDataDoneEvent = self.CalcBiasData
        if self.GateChannelIndex is not None:
            self.GateDataDoneEvent = self.CalcGateData
        self.ReadChannelsData(Fs=self.DCFs,
                              nSamps=self.DCnSamps,
                              EverySamps=self.DCnSamps)

    def CalcBiasData(self, Data):
        data = Data
        r, c = data.shape
        x = np.arange(0, r)
        mm, oo = np.polyfit(x, data, 1)
        Dev = np.abs(np.mean(mm))
        print 'DataProcess Attempt ', Dev
        if self.EventBiasAttempt:
            Ids = (data-self.BiasVd)/self.IVGainDC
            if not self.EventBiasAttempt(Ids,
                                         x*(1/np.float32(self.Inputs.Fs)),
                                         Dev):
                return  # Cancel execution

        if (Dev < self.DevCondition):
            Ids = (oo-self.BiasVd)/self.IVGainDC
            if self.EventBiasDone:
                self.EventBiasDone(Ids)
            return

        # try next attempt
        self.ReadChannelsData(Fs=self.DCFs,
                              nSamps=self.DCnSamps,
                              EverySamps=self.DCnSamps)

    def CalcGateData(self, Data):
        data = Data[1:, :]
        r, c = data.shape
        x = np.arange(0, r)
        mm, oo = np.polyfit(x, data, 1)
        Igs = oo/self.IVGainGate
        if self.EventGateDone:
            self.EventGateDone(Igs)
        return

    # AC
    ####
    def GetSeqBode(self, SeqConf):
        FFTconf = self.BodeSignal.FFTconfs[self.iConf]

        if SeqConf:
            print 'InitInptuns', SeqConf
            self.InitInputs(**SeqConf)

        signal, _ = self.BodeSignal.GenSignal(Ind=self.iConf)
        self.SetSignal(Signal=signal, nSamps=signal.size)

        if self.EventSetBodeLabel:
            self.EventSetBodeLabel(Vpp=self.BodeSignal.Vpp)

        print('Acquire Bode data for ',
              self.BodeSignal.BodeDuration[self.iConf], ' Seconds')

        self.ReadChannelsData(Fs=FFTconf.Fs,
                              nSamps=FFTconf.nFFT*self.BodeSignal.nAvg,
                              EverySamps=FFTconf.nFFT)

    def NextChannelAcq(self):
        FFTconf = self.BodeSignal.FFTconfs[self.iConf]

        SeqConf = self.InitConfig.copy()
        if self.InitConfig['Configuration'] == 'Both':
            SeqConf['Configuration'] = 'AC'

        if self.InitConfig['GateChannel'] is not None:
            SeqConf['GateChannel'] = None

        if FFTconf.AcqSequential is True:

            if self.SeqIndex <= len(self.InitConfig['Channels']) - 1:
                Channel = [sorted(self.InitConfig['Channels'])[self.SeqIndex], ]
                print 'Channel -->', Channel
                SeqConf['Channels'] = Channel
                self.SeqIndex += 1

            else:
                self.SeqIndex = 0
                if len(self.BodeSignal.FFTconfs) > 1 and self.iConf == 0:
                    self.iConf += 1
                else:
                    self.iConf = 0
                    if self.OldConfig:
                        self.InitInputs(**self.OldConfig)

                    if self.EventBodeDone:
                        self.EventBodeDone(self.Gm, self.BodeSignal.Fsweep)
                    return

        else:
            self.iConf = 0
            if self.OldConfig:
                self.InitInputs(**self.OldConfig)

            if self.EventBodeDone:
                self.EventBodeDone(self.Gm, self.BodeSignal.Fsweep)
            return

        self.GetSeqBode(SeqConf)

    def GetBode(self):
        self.OldConfig = self.InitConfig.copy()
        if self.InitConfig['Configuration'] == 'Both':
            self.OldConfig = self.InitConfig.copy()
            conf = self.InitConfig.copy()
            conf['Configuration'] = 'AC'
            self.InitInputs(**conf)

        self.ClearEventsCallBacks()
        self.ACDataDoneEvent = self.CalcBodeData
        self.ACDataEveryNEvent = self.EventDataAcq

        ##
        if len(self.BodeSignal.FFTconfs) > 1:
            self.GmH = np.ones((len(self.BodeSignal.FFTconfs[0].Freqs),
                                len(self.ACChannelIndex.items())))*np.complex(np.nan)

        self.Gm = np.ones((len(self.BodeSignal.Fsweep),
                           len(self.ACChannelIndex.items())))*np.complex(np.nan)
        ##
        self.NextChannelAcq()

    def CalcBodeData(self, Data):
        FFTconf = self.BodeSignal.FFTconfs[self.iConf]

        if FFTconf.AcqSequential is True:
            GmSeq = self.CalcBode(Data=Data,
                                  Ind=self.iConf,
                                  IVGainAC=self.IVGainAC,
                                  ChIndexes=self.ACChannelIndex)

            if len(self.BodeSignal.FFTconfs) > 1:
                self.GmH[:, self.SeqIndex - 1] = GmSeq[:, 0]
            else:
                self.Gm[:, self.SeqIndex - 1] = GmSeq[:, 0]

            self.NextChannelAcq()

            return

        else:
            GmL = self.CalcBode(Data=Data,
                                Ind=self.iConf,
                                IVGainAC=self.IVGainAC,
                                ChIndexes=self.ACChannelIndex)

            self.Gm = np.vstack((GmL, self.GmH))

        self.NextChannelAcq()

    def GetPSD(self):
        self.ClearEventsCallBacks()
        self.ACDataEveryNEvent = self.EventDataAcq
        if not self.PSDDuration:
            self.PSDDuration = self.PSDnFFT*self.PSDnAvg*(1/self.PSDFs)
        print 'DataProcess Acquire PSD data for ', self.PSDDuration, 'seconds'
        self.ACDataDoneEvent = self.CalcPSDData
        self.ReadChannelsData(Fs=self.PSDFs,
                              nSamps=self.PSDnFFT*self.PSDnAvg,
                              EverySamps=self.PSDnFFT)

    def CalcPSDData(self, Data):
        data = Data/self.IVGainAC

        ff, psd = signal.welch(x=data,
                               fs=self.PSDFs,
                               window='hanning',
                               nperseg=self.PSDnFFT,
                               scaling='density', axis=0)
        if self.EventPSDDone:
            self.EventPSDDone(psd, ff, data)

    def EventDataAcq(self, Data):
        r, c = Data.shape
        x = np.arange(0, r)
        if self.EventAcDataAcq:

            self.EventAcDataAcq(Data/self.IVGainAC,
                                x*(1/np.float32(self.Inputs.Fs)))

###############################################################################
#####
###############################################################################


class Charact(DataProcess):

    # Sweep points
    SwVdsVals = None
    SwVdsInd = None
    SwVgsVals = None
    SwVgsInd = None
    SwDigInd = None
    DevACVals = None

    # Status vars
    CharactRunning = False
    RunningConfig = False
    GateChannel = None

    # events list
    EventCharSweepDone = None
    EventCharBiasDone = None
    EventCharBiasAttempt = None
    EventCharAcDataAcq = None
    EventFFTDone = None

    def InitSweep(self, VdsVals, VgsVals, PSD=False, Bode=False):
        self.SwVgsVals = VgsVals
        self.SwVdsVals = VdsVals
        self.Bode = Bode
        self.PSD = PSD
        self.SwVgsInd = 0
        self.SwVdsInd = 0
        self.SwDigInd = 0

        self.EventBiasAttempt = self.BiasAttemptCallBack
        self.EventBiasDone = self.BiasDoneCallBack
        self.EventGateDone = self.GateDoneCallBack
        if self.Bode:
            self.EventBodeDone = self.BodeDoneCallBack
            self.BodeSignal.EventFFTDebug = self.EventFFT
        if self.PSD:
            self.EventPSDDone = self.PSDDoneCallBack
        self.EventAcDataAcq = self.AcAcqCallBack

        self.CharactRunning = True

        # Init Dictionaries
        self.InitDictionaries()
        self.DO = self.GenerateDigitalSignal()
        print self.DO
        self.ColumnsControl.SetDigitalSignal(Signal=self.DO[:, self.SwDigInd])
        self.ApplyBiasPoint()

    def InitDictionaries(self):
        # DC dictionaries
        if self.GateChannelIndex is None:
            Gate = False
        else:
            Gate = True

        self.DevACVals = None
        print self.ChannelNames
        self.DevDCVals = PyData.InitDCRecord(nVds=self.SwVdsVals,
                                             nVgs=self.SwVgsVals,
                                             ChNames=self.ChannelNames,
                                             Gate=Gate)
        # AC dictionaries
        if self.Bode or self.PSD:
            if self.PSD:
                Fpsd = np.fft.rfftfreq(self.PSDnFFT, 1/self.PSDFs)
            else:
                Fpsd = np.array([])

            if self.Bode:
                nFgm = self.BodeSignal.Fsweep
            else:
                nFgm = np.array([])

            self.DevACVals = PyData.InitACRecord(nVds=self.SwVdsVals,
                                                 nVgs=self.SwVgsVals,
                                                 nFgm=nFgm,
                                                 nFpsd=Fpsd,
                                                 ChNames=self.ChannelNames)

    def ApplyNextBias(self):
        if self.SwVdsInd < len(self.SwVdsVals)-1:
            self.SwVdsInd += 1
        else:
            self.SwVdsInd = 0
            if self.SwVgsInd < len(self.SwVgsVals)-1:
                self.SwVgsInd += 1
            else:
                self.SwVgsInd = 0

                if self.SwDigInd < len(self.DigColumns)-1:
                    self.SwDigInd += 1
                    self.ApplyNextDigital()
                else:
                    self.SwDigInd = 0

                    if self.EventCharSweepDone:
                        self.EventCharSweepDone(self.DevDCVals, self.DevACVals)
                    return

        if self.CharactRunning:
            self.ApplyBiasPoint()
        else:
            self.StopCharac()

    def ApplyBiasPoint(self):
        self.GetBiasCurrent(Vds=self.SwVdsVals[self.SwVdsInd],
                            Vgs=self.SwVgsVals[self.SwVgsInd])

        if self.EventSetLabel:
            self.EventSetLabel(self.SwVdsVals[self.SwVdsInd],
                               self.SwVgsVals[self.SwVgsInd])

    def ApplyNextDigital(self):
        print 'ApplyNextDigital'
        self.ColumnsControl.SetDigitalSignal(Signal=self.DO[:, self.SwDigInd])

    def BiasAttemptCallBack(self, Ids, time, Dev):
        if self.EventCharBiasAttempt:
            self.EventCharBiasAttempt(Ids, time, Dev)

        return self.CharactRunning

    def AcAcqCallBack(self, Ids, time):
        if self.EventCharAcDataAcq:
            self.EventCharAcDataAcq(Ids, time)
        else:
            self.StopCharac()

    def BiasDoneCallBack(self, Ids):
        print 'BiasDoneCallback', Ids.shape, self.DigColumns[self.SwDigInd]
        j = 0
        for chi, chn in enumerate(self.ChannelNames):
            if chn.endswith(self.DigColumns[self.SwDigInd]):
                self.DevDCVals[chn]['Ids'][self.SwVgsInd,
                                           self.SwVdsInd] = Ids[j]
                j += 1

        if self.EventCharBiasDone:
            self.EventCharBiasDone(self.DevDCVals)
        # Measure AC Data
        if self.CharactRunning:
            if self.PSD:
                self.GetPSD()
            elif self.Bode:
                self.GetBode()
            else:
                self.ApplyNextBias()

    def GateDoneCallBack(self, Igs):
        for chn, inds in self.GateChannelIndex.iteritems():
            self.DevDCVals['Gate']['Ig'][self.SwVgsInd, self.SwVdsInd] = Igs

    def BodeDoneCallBack(self, Gm, SigFreqs):
        j = 0
        for chi, chn in enumerate(self.ChannelNames):
            if chn.endswith(self.DigColumns[self.SwDigInd]):
                self.DevACVals[chn]['gm']['Vd{}'.format(self.SwVdsInd)][
                        self.SwVgsInd] = Gm[:, j]
                self.DevACVals[chn]['Fgm'] = SigFreqs
                j += 1

        if self.EventCharACDone:
            self.EventCharACDone(self.DevACVals)

        self.ApplyNextBias()

    def PSDDoneCallBack(self, psd, ff, data):
        j = 0
        for chi, chn in enumerate(self.ChannelNames):
            if chn.endswith(self.DigColumns[self.SwDigInd]):
                self.DevACVals[chn]['PSD']['Vd{}'.format(self.SwVdsInd)][
                        self.SwVgsInd] = psd[:, j]
                self.DevACVals[chn]['Fpsd'] = ff
                j += 1

        if self.EventCharACDone:
            self.EventCharACDone(self.DevACVals)

        if self.CharactRunning:
            if self.Bode:
                self.GetBode()
            else:
                self.ApplyNextBias()
        else:
            self.StopCharac()

    def EventFFT(self, FFT):
        if self.EventFFTDone:
            self.EventFFTDone(FFT)

    def StopCharac(self):
        print 'STOP'
        self.ColumnsControl.SetDigitalSignal(Signal=self.ClearSig)
        self.CharactRunning = False
#        self.Inputs.ClearTask()
