import numpy as np
from rtlsdr  import RtlSdr
import os, sys
import threading
#import matplotlib
#import matplotlib.pyplot as plt
#np.set_printoptions(threshold=sys.maxsize)

print("\nFALCON-B Tracking and Monitoring Software v0.0.2.")
print("Created by Ian Carney, Michael Krzystowczyk, William Lee, and Frank Palermo.")
print("Louisiana Tech University")
print("This program is for technical demonstration only and is not for use\nin any commercial, industrial, or operational environments.\n")

print("Version Notes: Adds ability to coordinate direction with multiple antennas.\n Multithreading has also been enabled for faster data collection\n")

sdrgain = 27
global snr1, snr2, snr3, snr4

#print(len(sys.argv))
#print(sys.argv[0])

#Configures SDR1
sdr1 = RtlSdr(serial_number='00000001')
sdr1.sample_rate =1.024e6
sdr1.bandwidth = 512e3
if len(sys.argv)==2:
    sdr1.center_freq = sys.argv[1]
else:
    sdr1.center_freq = 99.3e6
print("Current Frequency: ", sdr1.center_freq)
sdr1.freq_correction=1
sdr1.gain=sdrgain
snr_vals = []

#Configures SDR2
sdr2 = RtlSdr(serial_number='00000002')
sdr2.sample_rate =1.024e6
sdr2.bandwidth = 512e3
if len(sys.argv)==2:
    sdr2.center_freq = sys.argv[1]
else:
    sdr2.center_freq = 99.3e6
print("Current Frequency: ", sdr2.center_freq)
sdr1.freq_correction=1
sdr2.gain=sdrgain

#Configures SDR3
sdr3 = RtlSdr(serial_number='00000003')
sdr3.sample_rate =1.024e6
sdr3.bandwidth = 512e3
if len(sys.argv)==2:
    sdr3.center_freq = sys.argv[1]
else:
    sdr3.center_freq = 99.3e6
print("Current Frequency: ", sdr3.center_freq)
sdr3.freq_correction=1
sdr3.gain=sdrgain

#Configures SDR4
sdr4 = RtlSdr(serial_number='00000004')
sdr4.sample_rate =1.024e6
sdr4.bandwidth = 512e3
if len(sys.argv)==2:
    sdr4.center_freq = sys.argv[1]
else:
    sdr4.center_freq = 99.3e6
print("Current Frequency: ", sdr4.center_freq)
sdr4.freq_correction=1
sdr4.gain=sdrgain



    
    
while(1):
    sdr1data = threading.Thread(target=readValues, args=(sdr1)) #Returns Power of SDR1
    sdr2data = threading.Thread(target=readValues, args=(sdr2)) #Returns Power of SDR2
    sdr3data = threading.Thread(target=readValues, args=(sdr3)) #Returns Power of SDR3
    sdr4data = threading.Thread(target=readValues, args=(sdr4)) #Returns Power of SDR4

    sdr1data.start() #Starts collecting data from all 4 SDRs simultaneously
    sdr2data.start()
    sdr3data.start()
    sdr4data.start()

    sdr1data.join() #Waits for all collections to finish before proceeding
    sdr2data.join()
    sdr3data.join()
    sdr4data.join()

    snr1 = getSNR(sdr1data) #Returns SNR of SDR1
    snr2 = getSNR(sdr2data) #Returns SNR of SDR2
    snr3 = getSNR(sdr3data) #Returns SNR of SDR3
    snr4 = getSNR(sdr4data) #Returns SNR of SDR4
    
    all_snr = [snr1, snr2, snr3, snr4] #Puts all SDR Data in an array

    sorted_snr = all_snr_vals.sort() #Sorts SNR Data
    highSNR = sorted_snr[-1] #Gets highest SNR
    secondSNR = sorted_snr[-2] #Gets second highest SNR


    getDist(highSNR) #Uses highest SNR to find distance
    
    findCase(highSNR, secondSNR)

    dirFind(#something)
    

    
    

    
    






def readValues(receiver):
    data = receiver.read_samples(1024000)
    SigPower = 10*np.log10(10*((data.real**2)+(data.imag**2)))
    return SigPower
    


def getSNR(power):
    mean = np.mean(data)
    st_dev = np.std(data)
    dist_mean = abs(data-mean)
    max_dev = 1
    not_outlier = dist_mean < (max_dev * st_dev)
    no_outliers = SigPower[not_outlier]
    Pmax = max(no_outliers)
    Pmin = min(no_outliers)
    SNR = Pmax-Pmin
    #snr_vals[i] = SNR
    #print("The SNR is ", SNR)

    snr_vals = np.append(snr_vals, SNR)
    return SNR
    

def getDist(SNR):

    if(SNR != 0 and SNR > 7): # and SNR > 5 and SNR < 40 ):
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

    return mike

def dirFind(data):
    #Put direction finding code here

    return direction

def findCase(SNRmax, SNRsecond)

    if(SNRmax == snr1 and SNRsecond == snr4):
        casenum = 1

    if(SNRmax == snr1 and SNRsecond == snr2):
        casenum = 2

    if(SNRmax == snr2 and SNRsecond == snr1):
        casenum = 3

    if(SNRmax == snr2 and SNRsecond == snr3):
        casenum == 4

    if(SNRmax == snr3 and SNRsecond == snr4):
        casenum = 5

    if(SNRmax == snr3 and SNRsecond == snr4):
        casenum = 6

    if(SNRmax == snr4 and SNRsecond == snr3):
        casenum = 7

    if(SNRmax == snr4 and SNRsecond == snr1):
        casenum = 8

    return casenum 

    

















































    
    
        
    


