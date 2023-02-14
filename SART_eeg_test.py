# SART
# Author: Nicolas Bruno

from psychopy import core, visual, data, event, gui
# from psychopy.preferences import prefs
from psychopy.hardware import keyboard

from psychopy import logging
from psychopy.hardware import brainproducts

import random 
import os
import time

import sart_params
from instructions import instructions_text


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
# Experiment data settings
##########################################################################

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
# Initialize EEG
##########################################################################

rcs = brainproducts.RemoteControlServer()
rcs.amplifier =  'BrainAmp Family'
rcs.open(sart_params.exp_name,
         workspace='C:/Users/cocud/Documents/wandering-mind/test_workspace.rwksp',
         participant=f"{info_dict['ID']}_sesion_{info_dict['Sesion']}")
rcs.openRecorder()
rcs.mode = 'monitor' # or 'impedance', or 'default'
rcs.startRecording()

##########################################################################
# Create a window
##########################################################################
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

#setting keyboard
kb = keyboard.Keyboard()
#set q for quit
event.globalKeys.add(key='q', func=core.quit)

########################################################################
################        Experiment Started        ######################
########################################################################

#create text for instructions
instruction_begin = visual.TextStim(win=win,
                                    height = sart_params.text_height,
                                    units = 'cm',
                                    pos=(0, 0),
                                    text=instructions_text['initial_text'],
                                    wrapWidth=30
                                    )

instruction_begin.draw()      

win.flip()                    

#wait until space is pressed
event.waitKeys(keyList=['space'], timeStamped=False)

###############
#### Trial ####
###############
trials = data.TrialHandler(trialList=data.importConditions('sart_trials.csv'), 
                            nReps=1, method='random', name = 'test')

exp.addLoop(trials)
for trial in trials:
    
    if event.getKeys('q'):
        win.close()
        core.quit()

    # Create fixation cross 2
    fixation = visual.GratingStim(win, color=1, colorSpace='rgb',
                                    tex=None, mask='cross', size=2, units = 'cm')
    
    stim = visual.TextStim(win=win,
                        text=trial['stim'], 
                        height= sart_params.stim_height, 
                        pos=(0,0))

    # Draw fixation
    fixation.draw()
    rcs.sendAnnotation('fixation', 'FIXATION')
    win.flip()             
    core.wait(sart_params.fixation_time) 

    # Draw the visual stimuli faces and fixation cross
    stim.draw()
    rcs.sendAnnotation(trial['stim'], 'GO')
    # Flush the buffers
    kb.clearEvents()
    # Clock reset
    time_resp_clock = core.Clock()
    win.flip()
    core.wait(sart_params.stim_time)
    response = event.getKeys(keyList=['space'], timeStamped=time_resp_clock)

    if not response:
        time_to_save = None
        thisKey = None 

    else:
        time_to_save = response[0][1]
        thisKey = response[0][0]
        if thisKey in ['q']:
            core.quit() #abort experiment
    trials.addData('RT_space', time_to_save)
    
    

    # Inter Trial Interval(ITI) with blank screen
    win.flip()

    core.wait(sart_params.iti)
    
    exp.nextEntry()
    
###############
#### Probe ####
###############
#create text for instructions
probe_instructions = visual.TextStim(win=win,
                                    height = sart_params.text_height,
                                    units = 'cm',
                                    pos=(0, 0),
                                    text=instructions_text['probe_text'],
                                    wrapWidth=30
                                    )

probe_instructions.draw()      
# Clock reset
time_resp_clock = core.Clock()

rcs.sendAnnotation('TUT', 'PROBE')
win.flip()
# Flush the buffers
kb.clearEvents() 

#wait until space is pressed
key, rt = event.waitKeys(keyList=['1', '2'], timeStamped=time_resp_clock)[0]
exp.addData('probe_key', key)
exp.addData('probe_rt', rt)
if key == '1':
    exp.addData('probe_response', 'on-task')
    rcs.sendAnnotation('on-task', 'PROBE_RESPONSE')
elif key == '2':
    exp.addData('probe_response', 'MW')
    rcs.sendAnnotation('on-task', 'PROBE_RESPONSE')
    
    

exp.nextEntry()

#stop recording
rcs.stopRecording()
rcs.mode = 'default'  # stops monitoring mode
time.sleep(1)
# Task shutdown
win.close()
core.quit()


