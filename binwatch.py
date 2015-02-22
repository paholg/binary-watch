#!/usr/bin/env python2

import datetime, time
from pylab import *
import matplotlib
from matplotlib import rc
from matplotlib.lines import Line2D


rc('font', family='serif', serif ='Computer Modern')
rc('text', usetex=True)
matplotlib.rcParams.update({'font.size': 26})

watchc = "#dddddd"
hourc = "#dddd66"
minutec = "#dddd66"
secondc = "#dddd66"


watchwidth = 4
handsize = 12


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

def update():
    now = datetime.datetime.now().timetuple()
    hr_now = now.tm_hour
    min_now = now.tm_min
    sec_now = now.tm_sec

    for (bit, line) in zip(to_bits(hr_now) + to_bits(min_now) + to_bits(sec_now), hours + minutes + seconds):
        if bit == 1:
            line.set_linestyle('-')
        else:
            line.set_linestyle('')




fig = figure(figsize=(20, 20), facecolor='#121218')
ax = fig.add_subplot(111, aspect='equal')

xlim(-3.5, 3.5)
ylim(-3.5, 3.5)
xticks([])
yticks([])

arc = 2*pi*.75

phi = linspace(-arc/2, arc/2, 1000)


for r in [1, 2, 3]:
    plot(r*cos(phi), r*sin(phi), color=watchc, linewidth = watchwidth)

plot([0, 3*cos(arc/2)], [0, 3*sin(arc/2)], color=watchc, linewidth = watchwidth)
plot([0, 3*cos(-arc/2)], [0, 3*sin(-arc/2)], color=watchc, linewidth = watchwidth)


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
    plot([rmin*cos(tick), rmax*cos(tick)], [rmin*sin(tick), rmax*sin(tick)], color=watchc)
    text(textr*cos(tick), textr*sin(tick), 2**n, ha="center", va="center", color=watchc)

    # create hands
    r_mid = 0
    r_hr = 1
    r_min = 2
    r_sec = 3

    plot(0, 0, '.', markersize = handsize*2)

    hours += [Line2D([r_mid*cos(tick), r_hr*cos(tick)], [r_mid*sin(tick), r_hr*sin(tick)], color=hourc, linewidth = handsize, solid_capstyle="butt")]
    minutes += [Line2D([r_hr*cos(tick), r_min*cos(tick)], [r_hr*sin(tick), r_min*sin(tick)], color=minutec, linewidth = handsize, solid_capstyle="butt")]
    seconds += [Line2D([r_min*cos(tick), r_sec*cos(tick)], [r_min*sin(tick), r_sec*sin(tick)], color=secondc, linewidth = handsize, solid_capstyle="butt")]



ax.set_frame_on(False)
axis('off')

old_secs = 0


init()

update_time = time.time()
while True:
    update_time += 1
    update()
    pause(update_time - time.time())
