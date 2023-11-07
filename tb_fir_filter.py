# Simple tests for an fir_filter module

import cocotb
import random
from cocotb.clock import Clock
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge
from scipy.signal import lfilter
import numpy as np
import matplotlib.pyplot as plt

# Sample Wave Generator
def SampleWave (Amp, f, fs, clks): 
    clks = np.arange(0, clks)
    samplewave = np.rint(Amp*np.sin(2.0*np.pi*f/fs*clks))
    return samplewave

# Python Filter, output based on integer co-effecients we extracted
def PyFilter (signal,coeffs):
    output = lfilter(coeffs, 1.0, signal)
    return output

# Main Test
@cocotb.test()
async def filter_test(dut):
    #initialize
    dut.noisy_sig_i.value = 0
    fs         = 1              # Relative Sampling Frequence
    Amp        = 80
    no_of_clks = 512           
    nfft       = no_of_clks     # 512 point FFT
    f0         = 50*(1.0/nfft)  # Fundamental Frequency
    coeffs     = np.array([-1, 23, 33, 38, 33, 23, -1])  # Extracted from the python code fir_filter.py

    # Noisy input data
    # Adding a high frequency signal to a low frequency signal
    noisy_signal = SampleWave(Amp, f0, fs,no_of_clks) + SampleWave(Amp/2, 200.5*(1.0/nfft), fs, no_of_clks)

    # Python Result
    data_out_pred = PyFilter(noisy_signal, coeffs)

    # Start Clock
    cocotb.start_soon(Clock(dut.clk_i, 1, units="ns").start())

    # --------------- Reset DUT ------------------------
    await RisingEdge(dut.clk_i)
    await RisingEdge(dut.clk_i)
    dut.rst_n_i.value = 1
    dut.en_i.value = 0
    await RisingEdge(dut.clk_i)
    await RisingEdge(dut.clk_i)
    dut.rst_n_i.value = 0
    await RisingEdge(dut.clk_i)
    await RisingEdge(dut.clk_i)
    dut.en_i.value = 1 
    dut.rst_n_i.value = 1
    await RisingEdge(dut.clk_i)
    # --------------- Reset DUT ------------------------

    # Empty array 
    output_signal = np.zeros(no_of_clks)

    # Get data from each clock cycle
    for sample in range(no_of_clks):
        await RisingEdge(dut.clk_i)
        
        # Sample the output at the rising edge
        dut_data_out = dut.filtered_res_o.value.signed_integer

        # Enter the next sample
        dut.noisy_sig_i.value  = int(noisy_signal[sample])
        output_signal[sample] = dut_data_out
    
        
    # Displaing the results
    noisy_signal_fft    = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(noisy_signal, nfft))))
    filtered_fft        = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(output_signal[2:], nfft))))
    pyfilter_fft        = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(data_out_pred[:-2], nfft))))
    filter_resp_fft     = np.fft.fftshift(20*np.log10(np.abs(np.fft.fft(coeffs/sum(coeffs), nfft))))

    # For better visualization and consistency, let us normalize this
    noisy_signal_fft    = noisy_signal_fft - np.max(noisy_signal_fft)
    filtered_fft        = filtered_fft - np.max(filtered_fft)
    pyfilter_fft        = pyfilter_fft - np.max(pyfilter_fft)
    filter_resp_fft     = filter_resp_fft - np.max(filter_resp_fft)
    
    x_axis    = np.arange(-0.5, 0.5, 1/nfft)

    
    # plt.subplot(2,3,1)
    plt.figure(1)
    plt.plot(x_axis, noisy_signal_fft)
    plt.title('Fig1: Noisy Signal Input -- Frequency Domain')
    plt.savefig('Fig1.png')
    
    # plt.subplot(2,3,2)
    plt.figure(2)
    plt.plot(x_axis, filter_resp_fft)
    plt.title('Fig2: Filter Response -- Frequency Domain')
    plt.savefig('Fig2.png')
    
    # plt.subplot(2,3,3)
    plt.figure(3)
    plt.plot(x_axis, noisy_signal_fft)
    plt.plot(x_axis, filter_resp_fft)
    plt.title('Fig3: Noisy Signal and Filter Response in Frequency Domain')
    plt.savefig('Fig3.png')
    
    # plt.subplot(2,3,4)
    plt.figure(4)
    plt.plot(x_axis, filtered_fft, color = 'red')
    plt.title('Fig4: RTL Filter Response (Practical)')
    plt.savefig('Fig4.png')
    
   #  plt.subplot(2,3,5)
    plt.figure(5)
    plt.plot(x_axis, pyfilter_fft, color = 'blue')
    plt.title('Fig5: Python Filter Response (Theoretical)')
    plt.savefig('Fig5.png')
    
   #  plt.subplot(2,3,6)
    plt.figure(6)
    plt.plot(x_axis, filtered_fft, marker = 'x')
    plt.plot(x_axis, pyfilter_fft, marker = 'o')
    plt.title('Fig6: Practical and Theoretical Response Together')
    plt.savefig('Fig6.png')