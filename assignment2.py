import math
from numpy import *
import matplotlib.pyplot as plot
from neuron import IFNeuron, LIFNeuron, IzhikevichNeuron

fig = plot.figure()
ax1 = fig.add_subplot(1, 1, 1)

D     = 30    # ms
dt    = 0.025 # ms
time  = arange(0,D+dt,dt)

x = IzhikevichNeuron("x", a=0.02, b=0.2, c=-65, d=6, v=-70)
y = IzhikevichNeuron("y", a=0.02, b=0.2, c=-65, d=6, v=-70)

one_one = IzhikevichNeuron("one_one", a=0.02, b=0.2, c=-65, d=6, v=-70)
one_zero = IzhikevichNeuron("one_zero", a=0.02, b=0.2, c=-65, d=6, v=-70)
zero_one = IzhikevichNeuron("zero_one", a=0.02, b=0.2, c=-65, d=6, v=-70)
zero_zero = IzhikevichNeuron("zero_zero", a=0.02, b=0.2, c=-65, d=6, v=-70)

x_input = x.input(lambda t: 5)
y_input = y.input(lambda t: 10)

x.connect(one_one, 0.0)
y.connect(one_one, 0.0)

x.connect(one_zero, 1.0)
y.connect(one_zero, 1.0)

T = []
V = []
I = []
for i, t in enumerate(time):
    x.get(t)
    y.get(t)
    T.append(t)
    V.append(one_one.get(t))
    I.append(one_one.i(t))
    one_zero.get(t)
    #print one_one.i(t)

print "one_one: {} spikes/second".format((1000.0/D)*len(one_one.spikes))
print "one_zero: {} spikes/second".format((1000.0/D)*len(one_zero.spikes))

ax1.plot(T, V, T, I)
plot.xlabel("time (msec)")
plot.ylabel("membrane potential (mV)")
plot.title("Plot of an Izhikevich Neuron (tonic spiking)")

plot.show()