# SART
# Author: Nicolas Bruno

from psychopy import core, visual, data, event, gui
# from psychopy.preferences import prefs
from psychopy.hardware import keyboard

import random 
import os
import time

import sart_params
# import instructions


########################################################################
# GUI for subject information

# Form
info_dict = {
    'ID': 'S10',
    'Sesion': ['A', 'B'],
}

# Order of forms
order = ['ID', 'Sesion']

### UNCOMMENT THIS TO USE THE FORMS. It's commented for coding practicity.###
# Instantiate dialog box
my_dlg = gui.DlgFromDict(info_dict, title= sart_params.exp_name,
                            order=order)
if my_dlg.OK == False:
    core.quit()  # user pressed cancel

info_dict['date'] = data.getDateStr()
info_dict['exp_name'] = sart_params.exp_name

##########################################################################
##########################################################################
# Experiment data settings

# create folder to save experiment data for each subject
subject_folder = sart_params.results_folder + f"{info_dict['ID']}/"
os.makedirs(subject_folder, exist_ok=True)

# Name of .csv file to save the data
file_name = f"{info_dict['ID']}_sesion_{info_dict['Sesion']}_{sart_params.exp_name}_{info_dict['date']}"

# Create experiment handler
exp = data.ExperimentHandler(name=sart_params.exp_name,
                            extraInfo=info_dict,
                            runtimeInfo=True,
                            originPath='./',
                            savePickle=True,
                            saveWideText=True,
                            dataFileName=subject_folder + file_name)

##########################################################################
# Create a window
win = visual.Window(allowGUI=False,
                size=sart_params.display_size,
                monitor='testMonitor',
                winType='pyglet',
                useFBO=True,
                units=sart_params.window_units,
                fullscr=sart_params.fullscreen,
                color='black')

info_dict['frame_rate'] = win.getActualFrameRate()

############# TO RUN IN MAC AND LINUX ##############
from psychopy.iohub.client import launchHubServer
if os.name == 'posix':
    launchHubServer(window=win)
####################################################


