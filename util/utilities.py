'''
Utility functions go here.

SpiceBucks
'''

#------------------------------------------------------------------

import sys
import pyaudio
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

def beep(volume=0.5,     # range [0.0, 1.0]
         fs=44100,       # sampling rate, Hz, must be integer
         duration=1.0,   # in seconds, may be float
         f=440.0,        # sine frequency, Hz, may be float)
         ):
    p = pyaudio.PyAudio()
    # generate samples, note conversion to float32 array
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    stream.write(volume*samples)
    stream.stop_stream()
    stream.close()
    p.terminate()
