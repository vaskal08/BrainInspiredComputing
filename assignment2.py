import math
from numpy import *
import matplotlib.pyplot as plot
from vksnn import IFNeuron, IzhikevichNeuron

def xor (inputX, inputY):
    inpX = (inputX*50)+50
    inpY = (inputY*50)+50

    D     = 250    # ms
    dt    = 0.025 # ms
    time  = arange(0,D+dt,dt)

    x = IzhikevichNeuron("x", a=0.02, b=0.2, c=-65, d=6, v=-70)
    y = IzhikevichNeuron("y", a=0.02, b=0.2, c=-65, d=6, v=-70)

    one_zero = IzhikevichNeuron("one_zero", a=0.02, b=0.2, c=-65, d=6, v=-70)
    zero_one = IzhikevichNeuron("zero_one", a=0.02, b=0.2, c=-65, d=6, v=-70)

    same = IzhikevichNeuron("same", a=0.02, b=0.2, c=-65, d=6, v=-70)

    output = IzhikevichNeuron("same", a=0.02, b=0.2, c=-65, d=6, v=-70)

    x_input = x.input(x.createInput(inpX, 0, D+10, inpX), x.name, inpX)
    y_input = y.input(y.createInput(inpY, 0, D+10, inpY), y.name, inpY)

    y.connect(zero_one, 0.4)

    x.connect(one_zero, 0.4)

    x.connect(same, 0.22)
    y.connect(same, 0.22)

    one_zero.connect(output, 1.0)
    zero_one.connect(output, 1.0)
    same.connect(output, 0.2)

    T = []
    V = []
    I = []
    for i, t in enumerate(time):
        T.append(t)
        x.get(t)
        y.get(t)

        zero_one.get(t)
        one_zero.get(t)
        same.get(t)
        output.get(t)
    
    if len(output.spikes) < 22:
        return 0
    else:
        return 1

x = int(raw_input("x: "))
y = int(raw_input("y: "))

ans = xor(x, y)
print ans
