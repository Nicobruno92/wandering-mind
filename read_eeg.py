#%%
import mne
import os


file = os.path.relpath(r'results\SART_S10_sesion_A.vhdr')
raw = mne.io.read_raw_brainvision(vhdr_fname = file)

print(raw.info)
raw.plot()

#%%
