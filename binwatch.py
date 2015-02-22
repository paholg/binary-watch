#!/usr/bin/env python3

import datetime, time
from pylab import *
import matplotlib
from matplotlib import rc
from matplotlib.lines import Line2D
# from matplotlib.patches import Circle

###############################################
# Tweakables:
matplotlib.rcParams.update({
    'font.size': 30,
    'font.weight': 'bold',
})

bg = "#222228"
watchc = "#c0c0c0"
hourc = "#ffd700"
minutec = hourc
secondc = hourc


watchwidth = 6
handsize = 12

arc = 2*pi*.65
from_end = .8

datex = -2.3
datey = 0

###############################################


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
    ax.add_artist(date)

def update():
    now = datetime.datetime.now()
    nowt = now.timetuple()

    hr_now = nowt.tm_hour
    min_now = nowt.tm_min
    sec_now = nowt.tm_sec

    day_str = now.strftime("%A")
    date_str = now.strftime("%b %d")
    date.set_text("{}\n{}".format(day_str, date_str))

    for (bit, line) in zip(to_bits(hr_now) + to_bits(min_now) + to_bits(sec_now), hours + minutes + seconds):
        if bit == 1:
            line.set_linestyle('-')
        else:
            line.set_linestyle('')




fig = figure(figsize=(10, 10), facecolor=bg)
ax = fig.add_subplot(111, aspect='equal')

xlim(-3.5, 3.5)
ylim(-3.5, 3.5)
xticks([])
yticks([])


phi0 = linspace(0, 2*pi, 1000)
phi = linspace(-arc/2, arc/2, 1000)
r_mid = 0
r_hr = 1
r_min = 2
r_sec = 3



r_cres = -r_sec/(2*cos(arc/2))


# Use this instead for pacman:
# plot([0, 3*cos(arc/2)], [0, 3*sin(arc/2)], color=watchc, linewidth = watchwidth)
# plot([0, 3*cos(-arc/2)], [0, 3*sin(-arc/2)], color=watchc, linewidth = watchwidth)

# rings
for r in [r_hr, r_min, r_sec]:
    plot(r*cos(phi), r*sin(phi), color=watchc, linewidth = watchwidth, zorder = 3)

ax.add_patch(Circle((-r_cres, 0), r_cres, fc = bg, ec = 'none', zorder = 4))

# arc for crescent:
arc_c = 2*arcsin(r_sec/r_cres*sin(arc/2))
phic = linspace(-arc_c/2, arc_c/2, 1000)
plot(r_cres*cos(phic) - r_cres, r_cres*sin(phic), linewidth = watchwidth, color = watchc, zorder = 5)

plot(r_sec*cos(phi0), r_sec*sin(phi0), '-.', color=watchc, linewidth = watchwidth, zorder = 5)



hours = []
minutes = []
seconds = []


nticks = 6
ticks = linspace(arc/2 - arc/nticks*from_end, -arc/2 + arc/nticks*from_end, nticks)
for (n, tick) in enumerate(ticks):
    # draw ticks
    rmin = 2.85
    rmax = 3.15
    textr = 3.35
    plot([rmin*cos(tick), rmax*cos(tick)], [rmin*sin(tick), rmax*sin(tick)], color=watchc)
    text(textr*cos(tick), textr*sin(tick), 2**n, ha="center", va="center", color=watchc)

    # create hands
    hours += [Line2D([r_mid*cos(tick), r_hr*cos(tick)], [r_mid*sin(tick), r_hr*sin(tick)], color=hourc, linewidth = handsize, solid_capstyle="butt")]
    minutes += [Line2D([r_hr*cos(tick), r_min*cos(tick)], [r_hr*sin(tick), r_min*sin(tick)], color=minutec, linewidth = handsize, solid_capstyle="butt")]
    seconds += [Line2D([r_min*cos(tick), r_sec*cos(tick)], [r_min*sin(tick), r_sec*sin(tick)], color=secondc, linewidth = handsize, solid_capstyle="butt")]

date = matplotlib.text.Text(datex, datey, color=watchc, va='center', zorder = 5)

ax.set_frame_on(False)
axis('off')

old_secs = 0


init()

update_time = time.time()
while True:
    update_time += 1
    update()
    pause(update_time - time.time())
