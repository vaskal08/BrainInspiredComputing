import math
from numpy import *
import matplotlib.pyplot as plot
from neuron import IFNeuron, LIFNeuron, HHNeuron, IzhikevichNeuron

# To use the script:
# matplotlib is required
# uncomment the lines creating the plot for the programming task you wish to see
# make sure the lines creating the plot for all other programming tasks are commented out as they are currently


fig = plot.figure()
ax1 = fig.add_subplot(1, 1, 1)

# Programming task 1 - Plotting LIF neurons with different input currents
neuron_1 = IFNeuron(50)
input_1 = neuron_1.input(lambda t: 8)

neuron_2 = LIFNeuron(50, 6.0)
#input_2 = neuron_2.input(lambda t:6 if t > 20 and t < 40 else 0)
input_4 = neuron_2.input(lambda t:20.0)

neuron_3 = LIFNeuron(50, 20.0)

neuron_2.connect(neuron_3, 1.0)

D     = 500    # ms
dt    = 0.025 # ms
time  = arange(0,D+dt,dt)

T = []
V = []
V2 = []
V3 = []

for i, t in enumerate(time):
    T.append(t)
    V.append(neuron_1.get(t))
    V2.append(neuron_2.get(t))
    V3.append(neuron_3.get(t))

#uncomment the following lines to show programming task #1

#ax1.plot(T, V2, T, V3)
#plot.xlabel("time (msec)")
#plot.ylabel("membrane potential (mV)")
#plot.title("LIF neurons of resistance 10kOhm with different input currents")
#plot.legend(("8mv", "6mv", "4mv"))


# Programming task 3 - Plotting the firing rate as a function of the input current

input_currents = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
fire_rates = []

for input_current in input_currents:
    neuron = LIFNeuron(50, 10.0)
    neuron_input = neuron.input(lambda t: input_current)
    fire_rate = 0
    for i, t in enumerate(time):
        volt = neuron.get(t)
        if volt <= neuron.Vr:
            fire_rate+=1
    fire_rates.append(fire_rate)

#uncomment the following lines to show programming task #3

#plot.plot(input_currents, fire_rates)
#plot.xlabel("input currents (mV)")
#plot.ylabel("fire rates")
#plot.title("Fire rate of an LIF neuron as a function of the input current")

# Programming task 4 - Plotting a Izhikevich neuron

izhNeuron = IzhikevichNeuron(a=0.02, b=0.2, c=-65, d=6, v=-70)
izhInput = izhNeuron.input(lambda t: 30 if t > 10 and t < 40 else 0)

izhInput2 = izhNeuron.input(lambda t: 100 if t > 60 and t < 63 else 0)
izhInput3 = izhNeuron.input(lambda t: 100 if t > 64 and t < 67 else 0)
izhInput4 = izhNeuron.input(lambda t: 100 if t > 68 and t < 71 else 0)

#izhInput2 = izhNeuron.input(lambda t:6 if t > 20 and t < 40 else 0)
#izhInput3 = izhNeuron.input(lambda t: 10 if t > 60 and t < 90 else 0)

izhNeuron2 = IzhikevichNeuron(a=0.02, b=0.2, c=-65, d=6, v=-70)

izhNeuron.connect(izhNeuron2, 0.05)

T = []
V = []
V2 = []
V3 = []

D     = 120    # ms
dt    = 0.025 # ms
time  = arange(0,D+dt,dt)

for i, t in enumerate(time):
    T.append(t)
    V.append(izhNeuron.get(t))
    V2.append(izhNeuron2.i(t))
    V3.append(izhNeuron2.get(t))

#uncomment the following lines to show programming task #4

ax1.plot(T, V, T, V2, T, V3)
plot.xlabel("time (msec)")
plot.ylabel("membrane potential (mV)")
plot.title("Plot of an Izhikevich Neuron (tonic spiking)")

# Programming task 5 - Plotting a Hodgkin-Huxley neuron

hhNeuron = HHNeuron()
hhInput = hhNeuron.input(lambda t: 20 if t > 10 and t< 20 else 0)

T = []
V = []

D     = 30    # ms
dt    = 0.025 # ms
time  = arange(0,D+dt,dt)

for i, t in enumerate(time):
    T.append(t)
    V.append(hhNeuron.get(t))

#uncomment the following lines to show programming task #5

#ax1.plot(T, V)
#plot.xlabel("time (msec)")
#plot.ylabel("membrane potential (mV)")
#plot.title("Plot of a Hodgkin-Huxley Neuron")

plot.show()
