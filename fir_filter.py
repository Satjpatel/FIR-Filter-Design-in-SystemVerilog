# Python Code to get co-effecients for a 5 tap FIR Filter
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

passband_bw     = 0.1
transition_bw   = 0.1
no_of_taps      = 7
fs              = 1  # Normalized Sampling Rate

# Getting the co-efficients
fir_coeffs = signal.remez(no_of_taps, [0, passband_bw, passband_bw+transition_bw, 0.5*fs], [1,0], fs = fs)

# Converting the filter co-effecients in 8 bit format
fir_coeffs_int = np.round(fir_coeffs * (2**7-1)).astype(int)
print(fir_coeffs_int)

fir_coeffs_int_hex = [hex(x) for x in fir_coeffs_int]

# Write into file
f = open("co_eff_7tap.txt", "w")
for i in range(0, no_of_taps):
    x = str(fir_coeffs_int_hex[i])[2:]
    f.write(x+'\n') # Go to the next line
f.close()


# Plotting the filter response
n_fft = 1000

# With Real Values
normalized_coeffs = fir_coeffs/np.sum(fir_coeffs)
fft_1 = np.fft.fft(normalized_coeffs, n_fft)
# In dB
x_fft = np.fft.fftshift(20*np.log10(np.abs(fft_1)))

# With Integer Values
normalized_coeffs_int = fir_coeffs_int/np.sum(fir_coeffs_int)
fft_2 = np.fft.fft(normalized_coeffs_int, n_fft)
# In dB
x_int_fft = np.fft.fftshift(20*np.log10(np.abs(fft_2)))


x_axis = np.arange(-0.5, 0.5, 1/n_fft)
# print(x_axis)

plt.figure(1)
plt.plot(x_axis, x_fft, color = 'red')
plt.title("Filter Response with Real Values")
plt.savefig('FilterResponseWithRealValues.png')


plt.figure(2)
plt.plot(x_axis, x_int_fft, color = 'blue')
plt.title("Filter Response with Integer Values")
plt.savefig('FilterResponseWithIntegerValues.png')

plt.figure(3)
plt.plot(x_axis, x_int_fft, color = 'blue', marker = '+')
plt.plot(x_axis, x_fft, color = 'red', marker = '*')
plt.legend(['integer', 'real'])
plt.title("Comparing the Filter Response Co-effecients with Superposition")
plt.savefig('Co_eff_Comparison.png')