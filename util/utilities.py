'''
Utility functions go here.

SpiceBucks
'''

#------------------------------------------------------------------

import sys
import pygame
import numpy as np

from util.message import message

#------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# system functions
#----------------------------------------z-------------------------------------------------

def exit(code):
    '''
	Exit the program, 0 is failure, 1 is success.
	'''
    if not isinstance(code, int):
        message.logError('Exit code must be an interger.')
        exit(0)
    if code == 0:
        message.logError('Exiting program with failure status.')
    elif code == 1:
        message.logDebug('Exiting program with success status.')
    else:
        message.logError('Exiting program with unknown error status ('+str(code)+')')
    sys.exit()

#-----------------------------------------------------------------------------------------
# sound functions
#----------------------------------------z-------------------------------------------------

def beep(file_name):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(file_name)
    sound.play()
