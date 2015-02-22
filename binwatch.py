#!/usr/bin/env python3

import datetime, time
from pylab import *
import matplotlib
from matplotlib import rc
from matplotlib.lines import Line2D
from matplotlib import animation

rc('font', family='serif', serif ='Computer Modern')
rc('text', usetex=True)
matplotlib.rcParams.update({'font.size': 26})

# ion()

# convert an integer to a list of bits. Only does the least significant 6 bits, as
# that's what the watch uses
def to_bits(n):
    bits = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        bits[i] = n%2
        n //= 2
    return bits

def init():
    for line in hours + minutes + seconds:
        ax.add_line(line)

def animate(i):
    now = datetime.datetime.now().timetuple()
    hr_now = now.tm_hour
    min_now = now.tm_min
    sec_now = now.tm_sec

    for (bit, line) in zip(to_bits(hr_now) + to_bits(min_now) + to_bits(sec_now), hours + minutes + seconds):
        if bit == 1:
            line.set_linestyle('-')
        else:
            line.set_linestyle('')


watchwidth = 2
handsize = 5


fig = figure(figsize=(20, 20))
ax = fig.add_subplot(111, aspect='equal')

xlim(-3.5, 3.5)
ylim(-3.5, 3.5)
xticks([])
yticks([])

arc = 2*pi*.75

phi = linspace(-arc/2, arc/2, 1000)

hours = []
minutes = []
seconds = []

nticks = 6
ticks = linspace(arc/2 - arc/2/nticks, -arc/2 + arc/2/nticks, nticks)
for (n, tick) in enumerate(ticks):
    # draw ticks
    rmin = 2.85
    rmax = 3.15
    textr = 3.35
    plot([rmin*cos(tick), rmax*cos(tick)], [rmin*sin(tick), rmax*sin(tick)], 'k')
    text(textr*cos(tick), textr*sin(tick), 2**n, ha="center", va="center")

    # create hands
    hours += [Line2D([0, 1*cos(tick)], [0, 1*sin(tick)], color='k', linewidth = handsize)]
    minutes += [Line2D([1*cos(tick), 2*cos(tick)], [1*sin(tick), 2*sin(tick)], color='k', linewidth = handsize)]
    seconds += [Line2D([2*cos(tick), 3*cos(tick)], [2*sin(tick), 3*sin(tick)], color='k', linewidth = handsize)]

for r in [1, 2, 3]:
    plot(r*cos(phi), r*sin(phi), 'k', linewidth = watchwidth)

plot([0, 3*cos(arc/2)], [0, 3*sin(arc/2)], 'k', linewidth = watchwidth)
plot([0, 3*cos(-arc/2)], [0, 3*sin(-arc/2)], 'k', linewidth = watchwidth)



init()
while True:
    animate(0)
    pause(1.0)
    # draw()
    # time.sleep(1)
