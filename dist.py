import numpy as np
from rtlsdr  import RtlSdr
import os, sys
#import matplotlib
#import matplotlib.pyplot as plt
np.set_printoptions(threshold=1024)

print("\nFALCON-B Tracking and Monitoring Software v0.0.1.")
print("Created by Ian Carney, Michael Krzystowczyk, William Lee, and Frank Palermo.")
print("Louisiana Tech University")
print("This program is for technical demonstration only and is not for use\nin any commercial, industrial, or operational environments.\n")



#print(len(sys.argv))
#print(sys.argv[0])

#configuring the device
sdr = RtlSdr(serial_number='0000101')
sdr.sample_rate =1.024e6
sdr.bandwidth = 512e3
if len(sys.argv)==2:
    sdr.center_freq = sys.argv[1]
else:
    sdr.center_freq = 462562500
print("Current Frequency: ", sdr.center_freq)
sdr.freq_correction=1
sdr.gain=10
#time = 21
snr_vals = []

#num_samples = int(sdr.sample_rate*time)
#print("Collecting ", num_samples, " samples")

#while(1):
    
    
    #for i in range(5):
while(1):

    values = sdr.read_samples(1024000)
    #Calculate Signal Power
    #SigPower = 20*np.log10(abs(values)/32768)
    SigPower = 10*np.log10(10*((values.real**2)+(values.imag**2)))
    #FFT = np.fft.fft(values)
    #print(FFT)
    #print('\n')
    mean = np.mean(SigPower)
    st_dev = np.std(SigPower)
    dist_mean = abs(SigPower-mean)
    max_dev = 1
    not_outlier = dist_mean < (max_dev * st_dev)
    no_outliers = SigPower[not_outlier]
    Pmax = max(no_outliers)
    floor = -36
    Pmin = min(no_outliers)
    SNR = Pmax-floor
    #snr_vals[i] = SNR
    #print("The SNR is ", SNR)

    snr_vals = np.append(snr_vals, SNR)

#mean_snr = np.mean(snr_vals[1:])
#print(snr_vals)
    if(SNR != 0 and SNR > 1): # and SNR > 5 and SNR < 40 ):
        print(SNR)
        x = SNR 
        ColdDist = 0.1245*(x**2)-10.659*x+212.36
        WarmDist = -0.0857*(x**3)+6.2553*(x**2)-155.33*(x)+1342.8
	frank = .0177*(x**3)-.9015*(x**2)+10.86*(x)+27.934
	ian = .0195*(x**3)-1.0075*(x**2)+12.906*(x)+14.742
	will = (frank + ian)/2
	mike = .0174*(x**3)-.8964*(x**2)+10.857*(x)+29.338
	print("eq1", frank)
	print("eq2", ian)
	print("eq3 ", will)
	print("The distance is between", mike-2, "and", mike+2,"ft. away")
       # print("Cold Distance: ", ColdDist)
       # print("Warm Distance: ", WarmDist)
	print('\n')
        
    
#mean_snr = 0
#print(mean_snr)


#avgSNR = np.mean(snr_vals)
#print("The SNR is ", SNR)

