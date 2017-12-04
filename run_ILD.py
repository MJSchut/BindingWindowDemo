import pygaze
from pygaze import libscreen
from pygaze import libinput
from pygaze import libtime

from psychopy import visual
from psychopy import core
import matplotlib.pyplot as plt

import os
import constants
import Waveforms_v2 as wf

import numpy as np

disp = libscreen.Display()

kb_space = libinput.Keyboard(keylist = ['space'], timeout = None)
kb_response = libinput.Keyboard(keylist = ['s', 'd', 'q'], timeout = None)

scr = libscreen.Screen()
scr.draw_text('Starting the ILD demo!\n\nPress s for sound left\n\nPress d for sound right\n\n--Space bar to start--',
              fontsize = 24)
disp.fill(scr)
disp.show()
kb_space.get_key()

ITD_array = np.linspace(-0.75, 0.75, num = 80)
np.random.shuffle(ITD_array)
response_array = []

box = visual.Circle(pygaze.expdisplay, radius = 50)

for itd in ITD_array:
    disp.show()

    visual_jitter = np.random.randint(-200, 200)
    auditory_jitter = float(visual_jitter) / float(constants.DISPSIZE[0])
    print visual_jitter, auditory_jitter, itd

    sound = wf.waveform(wavetype='wn', duration=0.1, pan = itd + auditory_jitter)
    box.pos = [visual_jitter, 0]
    libtime.pause(100 + np.random.uniform(0, 300))

    box_time = 400 + libtime.get_time()
    sound_time = 400 + libtime.get_time()

    box_shown = 0
    sound_played = 0

    scr = libscreen.Screen()
    scr.clear()

    starttime = libtime.get_time()
    maxtrialtime = 600

    while libtime.get_time() < starttime + maxtrialtime:
        time = libtime.get_time()
        if time > box_time and box_shown == 0:
            scr.screen.append(box)
            box_shown = 1

        if time > box_time + 100 and box_shown == 1:
            scr.clear()

        if time > sound_time and sound_played == 0:
            sound.play()
            sound_played = 1

        disp.fill(scr)
        disp.show()

    key, t = kb_response.get_key()

    if key == 'q':
        break
    elif key == 's':
        response_array.append(0)
    elif key == 'd':
        response_array.append(1)

# finishing up
results_dir = os.path.join(constants.DIR, 'results')
fig_dir = os.path.join(results_dir, 'figures')
csv_dir = os.path.join(results_dir, 'csv')

# plot
fig, ax = plt.subplots()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')
ax.plot(ITD_array, response_array, 'k.')

from scipy.optimize import curve_fit

def sigmoid(x, x0, k):
    y = 0.01 + (1 - 0.01 - 0.01) / (1 + np.exp(-k * (x - x0)))
    return y

popt, pcov = curve_fit(sigmoid, ITD_array, response_array)
print popt, pcov
nx = np.linspace(-0.75, 0.75, num = 500)
ny = sigmoid(nx, *popt)
ax.plot(nx, ny, 'k-', label='fit')
bias = popt[0]
bw = np.log(popt[1])
ax.text(0.25, 0.1, 'bias = %s' %bias)
ax.text(0.25, 0.2, 'binding window = %s' %bw)
ax.axhline(y = 0.5, xmin = -1, xmax = 1, color = 'k', ls = 'dashed')
ax.axhline(y = 0.25, xmin = -1, xmax = 1, color = 'k', ls = 'dashed')
ax.axhline(y = 0.75, xmin = -1, xmax = 1, color = 'k', ls = 'dashed')

import time
fig.savefig(fig_dir + '/' + str(time.clock()) + '_ILD.png')

