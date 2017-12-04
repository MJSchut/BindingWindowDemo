__author__ = 'Martijn Schut'

import os.path
import math

BLOCKNAME                   = 'P41'

DIR                         = os.path.dirname(__file__)

SCREENNR                    = 0
DISPTYPE                    = 'psychopy'
DISPSIZE                    = (2560, 1440)              # Screen resolution
DIAGONAL                    = 68.58                     # in cm
SCREENSIZE                  = (
                              (DISPSIZE[0]/ DISPSIZE[1]) * DISPSIZE[1] * (DIAGONAL / math.sqrt(DISPSIZE[0]**2 + DISPSIZE[1]**2)),
                               DISPSIZE[1] * (DIAGONAL / math.sqrt(DISPSIZE[0]**2 + DISPSIZE[1]**2))
                               )   # Size of screen

SCREENDIST                  = 70                        # Distance of screen in cm
CENTERX                     = DISPSIZE[0]/2
CENTERY                     = DISPSIZE[1]/2

FULLSCREEN                  = True

BGC                         = (0,0,0)
FGC                         = (255,255,255)
TEXTSIZE                    = 24

TRACKERTYPE                 = 'eyelink'
EYELINKCALBEEP              = False
DUMMYMODE                   = True
