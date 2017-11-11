import math
from numpy import *
import matplotlib.pyplot as plot
import matplotlib.animation as animation
from neuron import IFNeuron, LIFNeuron, HHNeuron, IzhikevichNeuron

fig = plot.figure()
ax1 = fig.add_subplot(1, 1, 1)

neuron_1 = LIFNeuron(10.0, 5.0)
input_1 = neuron_1.input(lambda t: 20.0)

izhNeuron = IzhikevichNeuron(a=0.02, b=0.2, c=-65, d=6, v=-70)
izhInput = izhNeuron.input(lambda t: 30 if t > 10 and t < 40 else 0)
#izhInput2 = izhNeuron.input(lambda t:6 if t > 20 and t < 40 else 0)
izhInput3 = izhNeuron.input(lambda t: 10 if t > 60 and t < 80 else 0)

dt    = 0.1 # ms

T = []
V = []

def animate(i):
    T.append(i*dt)
    V.append(izhNeuron.get(i*dt))
    ax1.clear()
    ax1.plot(T, V)

ani = animation.FuncAnimation(fig, animate, interval=100)
plot.show()