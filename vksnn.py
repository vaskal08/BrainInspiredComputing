from __future__ import division
from numpy import *
from pylab import *

class IFNeuron(object):

    def __init__(self, threshold):
        self.name = "name"
        self.Cm = 10.0   #capacitance (uF)
        self.threshold = threshold #threshold (mV)
        self.Vr = 2.0 #resting voltage (mV)
        self.voltage = self.Vr #neuron's current voltage (mV)
        self.time = 0.0 #neuron's current time (msec)
        self.inputFunctions = [] #(I(t) = function, t > starting)
        self.outputFunction = lambda t, d: 0
        self.leakTime = 5.0 #time to leak neurons potential (ms)
        self.synapses = []
        self.spikes = []
        self.round = 3

    def input(self, function, presynaptic="default", inp=-1.0):
        """Give this neuron an input signal function that takes affect where t > starting"""
        inputFunction = (function, presynaptic, self.name, inp)
        self.inputFunctions.append(inputFunction)
        return function

    def output(self, function):
        self.outputFunction = function

    def createInput(self, inputValue, starting, ending, default):
        return lambda t: inputValue if t > starting and t < ending else default

    def leak(self, time):
        dV = self.voltage - self.Vr
        dT = self.leakTime
        output = dV
        self.spikes.append(round(time, self.round))
        self.output(lambda t, d: -1*(dV/dT)*d if t > time and t < time+dT else 0)
        for synapse in self.synapses:
            postsynaptic = synapse[0]
            weight = synapse[1]
            postInput = (output*weight)/(dT)
            name = self.name
            function = lambda t: postInput if t > time and t < time+dT else 0
            postsynaptic.input(self.createInput(postInput, time, time+dT, 0), name, postInput)

    def o(self, time):
        totalV = 0.0
        dT = time - self.time

        v = self.outputFunction(time, dT)
        totalV += v

        return totalV

    def i(self, time):
        totalV = 0.0

        for inputFunction in self.inputFunctions:
            function = inputFunction[0]
            presynaptic = inputFunction[1]
            postsynaptic = inputFunction[2]
            inp = inputFunction[3]
            v = function(time)
            totalV += v

        return totalV

    def connect(self, postsynaptic, weight):
        #create a synapse connecting this neuron to a post synaptic neuron
        self.synapses.append((postsynaptic, weight))

    def get(self, time):
        #"""Get the voltage of this neuron at time"""

        output = self.o(time)
        if output < 0:
            self.voltage += output
        else:
            dT = time - self.time
            dV = (self.i(time) / self.Cm) * dT
            self.voltage += dV
            if self.voltage > self.threshold:
                self.leak(time)

        self.time = time
        return self.voltage

class IzhikevichNeuron(IFNeuron):
    def __init__(self, name, a, b, c, d, v, u=0):
        super(IzhikevichNeuron, self).__init__(30.0)
        self.inputFunctions = []
        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.Vr = c
        self.d = d
        self.voltage = v
        self.u = u
        self.time = 0.0

    def get(self, time):
        output = self.o(time)
        if output < 0:
            self.voltage += output
        else:
            dT = time - self.time

            dV = ((0.04*(self.voltage**2)) + (5*self.voltage) + 140 - self.u + self.i(time)) * dT
            dU = self.a*((self.b * self.voltage) - self.u)

            self.voltage += dV
            self.u += dU
            if self.voltage > self.threshold:
                #self.voltage = self.c
                self.leak(time)
                self.u += self.d

        self.time = time
        return self.voltage
