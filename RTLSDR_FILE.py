# -*- coding: utf-8 -*-
import csv

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz, decimate
import scipy.signal


def butter_lowpass_filter(data, cutoff, fs, order=5): 
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a



with open(r'C:\Users\samdi\OneDrive - Vrije Universiteit Brussel\EDU3\Netwerken\file100.txt' , 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
        
for i in range(0, len(row)):
    row[i] = complex(row[i])
     
samples = np.copy((row))


demod = decimate(samples, 10) #Decimate
demod = np.arctan2(np.imag(demod), np.real(demod))
demod = np.unwrap(demod) # fix bgtan
demod = demod[:-1] - demod[1:]
demod = butter_lowpass_filter(demod, 15000, 2.205e6/50, 5)
demod = decimate(demod, 5)



demod *= 10000 / np.max(np.abs(demod))
demod.astype("int16").tofile("mono100.raw")


plt.plot(demod)
plt.xlabel('Frequency (MHz)')
plt.ylabel('Relative Power (dB)')