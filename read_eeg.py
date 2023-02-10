
import mne
import os


file = os.path.relpath('results\S01\S107_compasion_pre_RS.vhdr')
raw = mne.io.read_raw_brainvision(vhdr_fname = file)

raw.plot()
