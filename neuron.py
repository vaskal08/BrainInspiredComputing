from __future__ import division
from numpy import *
from pylab import *
class IFNeuron(object):

    def __init__(self, threshold):
        self.Cm = 10.0   #capacitance (uF)
        self.threshold = threshold #threshold (mV)
        self.Vr = 2.0 #resting voltage (mV)
        self.voltage = self.Vr #neuron's current voltage (mV)
        self.time = 0.0 #neuron's current time (msec)
        self.inputFunctions = [] #(I(t) = function, t > starting)

    def input(self, function, starting):
        """Give this neuron an input signal function that takes affect where t > starting"""
        inputFunction = (function, starting)
        self.inputFunctions.append(inputFunction)
        return inputFunction

    def get(self, time):
        #"""Get the voltage of this neuron at time"""
        for inputFunction in self.inputFunctions:
            if time > inputFunction[1]:
                dT = time - self.time

                dV = (inputFunction[0](time) / self.Cm) * dT
                self.voltage += dV

                if self.voltage > self.threshold:
                    self.voltage = self.Vr

        self.time = time
        return self.voltage


class LIFNeuron(IFNeuron):

    def __init__(self, threshold, resistance):
        super(LIFNeuron, self).__init__(threshold)
        self.Rm = resistance #resistance (kOhm)
        self.time = 0.0

    def get(self, time):
        for inputFunction in self.inputFunctions:
            if time > inputFunction[1]:
                dT = time - self.time

                TAUm = self.Rm * self.Cm
                dV = (((-1*self.voltage) + (self.Rm * inputFunction[0](time)))/(TAUm))*dT
                self.voltage += dV

                if self.voltage > self.threshold:
                    self.voltage = self.Vr

        self.time = time
        return self.voltage

class IzhikevichNeuron(IFNeuron):
    def __init__(self, a, b, c, d, v, u=0):
        super(IzhikevichNeuron, self).__init__(30.0)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.voltage = v
        self.u = u
        self.time = 0.0

    def get(self, time):
        for inputFunction in self.inputFunctions:
            if time > inputFunction[1]:
                dT = time - self.time

                I = inputFunction[0](time)
                dV = ((0.04*(self.voltage**2)) + (5*self.voltage) + 140 - self.u + I) * dT
                dU = self.a*((self.b * self.voltage) - self.u)

                self.voltage += dV
                self.u += dU

                if self.voltage > self.threshold:
                    self.voltage = self.c
                    self.u += self.d

        self.time = time
        return self.voltage

class HHNeuron(IFNeuron):
    def __init__(self):
        super(HHNeuron, self).__init__(0.0)
        self.alpha_n = vectorize(lambda v: 0.01*(-v + 10)/(exp((-v + 10)/10) - 1) if v != 10 else 0.1)
        self.beta_n  = lambda v: 0.125*exp(-v/80)
        self.n_inf   = lambda v: self.alpha_n(v)/(self.alpha_n(v) + self.beta_n(v))

        # Na channel (activating)
        self.alpha_m = vectorize(lambda v: 0.1*(-v + 25)/(exp((-v + 25)/10) - 1) if v != 25 else 1)
        self.beta_m  = lambda v: 4*exp(-v/18)
        self.m_inf   = lambda v: self.alpha_m(v)/(self.alpha_m(v) + self.beta_m(v))

        # Na channel (inactivating)
        self.alpha_h = lambda v: 0.07*exp(-v/20)
        self.beta_h  = lambda v: 1/(exp((-v + 30)/10) + 1)
        self.h_inf   = lambda v: self.alpha_h(v)/(self.alpha_h(v) + self.beta_h(v))

        ## HH Parameters
        self.Vr = 0      # mV
        self.Cm = 1      # uF/cm2
        self.gbar_Na = 120    # mS/cm2
        self.gbar_K = 36     # mS/cm2
        self.gbar_l = 0.3    # mS/cm2
        self.E_Na = 115    # mV
        self.E_K = -12    # mV
        self.E_l = 10.613 # mV

        self.m = self.m_inf(self.Vr)      
        self.h = self.h_inf(self.Vr)
        self.n = self.n_inf(self.Vr)

        self.time = 0.0

    def get(self, time):
        for inputFunction in self.inputFunctions:
            if time > inputFunction[1]:
                dT = time - self.time

                g_Na = self.gbar_Na*(self.m**3)*self.h
                g_K  = self.gbar_K*(self.n**4)
                g_l  = self.gbar_l  
                  
                self.m += (self.alpha_m(self.voltage)*(1 - self.m) - self.beta_m(self.voltage)*self.m) * dT
                self.h += (self.alpha_h(self.voltage)*(1 - self.h) - self.beta_h(self.voltage)*self.h) * dT
                self.n += (self.alpha_n(self.voltage)*(1 - self.n) - self.beta_n(self.voltage)*self.n) * dT

                I = inputFunction[0](time)

                dV = self.voltage + (I - g_Na*(self.voltage - self.E_Na) - g_K*(self.voltage - self.E_K) - g_l*(self.voltage - self.E_l)) / self.Cm * dT
                self.voltage += dV
        
        self.time = time
        return self.voltage
