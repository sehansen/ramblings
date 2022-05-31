#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

def lowpass(signal):
    return (signal[1:] + signal[:-1]) / 2

signal_length = 10000
noise_scale = 32

signal_ref = np.zeros((signal_length, ))
signal_ref[int(np.floor(signal_length/2)):] = np.ones((int(np.ceil(signal_length/2)), ))

plt.figure(1)
plt.subplot(1, 3, 1)
plt.plot(signal_ref)
plt.title("Original signal")

noise = noise_scale * (2 * np.random.random((signal_length)) - 1)
plt.subplot(1, 3, 2)
plt.plot(noise)
plt.title("Noise")

signal = signal_ref + noise
plt.subplot(1, 3, 3)
plt.plot(signal)
plt.title("Realized signal")

print(np.mean(signal[:int(np.floor(signal_length/2))]))
print(np.mean(signal[int(np.floor(signal_length/2)):]))

plt.figure(2)
plt.plot(signal)
plt.plot(lowpass(signal))
plt.plot(lowpass(lowpass(signal)))
plt.plot(lowpass(lowpass(lowpass(signal))))
plt.plot(lowpass(lowpass(lowpass(lowpass(signal)))))
plt.plot(lowpass(lowpass(lowpass(lowpass(lowpass(signal))))))
plt.plot(signal_ref)

plt.show()
