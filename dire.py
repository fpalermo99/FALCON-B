import numpy as np
from rtlsdr  import RtlSdr
import os, sys
from time import sleep
#np.set_printoptions(threshold=sys.maxsize)


def readValues(receiver,samp_rate):
    data = receiver.read_samples(1024000)
    valueDBFS = 20*np.log10(abs(data)/32768)
    SigPower = 10*np.log10(10*((data.real**2)+(data.imag**2)))
    return SigPower
    

def findZone(SNR):
	if(SNR > 42.9):
		distmin = 7
		distmax = 15
        	colorzone = 1
	elif(SNR > 40.11 and SNR < 42.9):
		distmin = 15
		distmax = 25
        	colorzone = 2
	elif(SNR < 40.11 and SNR > 37.455):
		distmin = 25
		distmax = 35
        	colorzone = 3
	elif(SNR < 37.455 and SNR > 30.5):
		distmin = 35
		distmax = 45
        	colorzone = 4
	elif(SNR < 30.5 and SNR > 25):
		distmin = 45
		distmax = 100
        	colorzone = 5
	return distmin, distmax, colorzone
    


def getSNR(power):
    mean = np.mean(power)
    st_dev = np.std(power)
    dist_mean = abs(power-mean)
    max_dev = 1
    not_outlier = dist_mean < (max_dev * st_dev)
    no_outliers = power[not_outlier]
    Pmax = max(no_outliers)
#    Pmax = max(power)
#    Pmin = min(no_outliers)
    floor = -36
    SNR = Pmax-floor
    if(SNR < 1):
        SNR = 0

    return SNR
    

def getDist(SNR):
    #print(SNR)
    x = SNR 
    radiolog = -98.72*np.log(x)+387.86
    #print("the incoming signal is ", radiolog, "ft away")
    return radiolog

def dirFind(shortDist, longDist, ceiling):
    antDist = 1
    a = longDist
    b = shortDist
    c = antDist
    boxLeg = 0.5*np.sqrt(2)
    alpha = np.arccos((b**2 + c**2 - a**2)/(2*b*c)) #Law of Cosines
    beta = np.arccos((a**2 + c**2 - b**2)/(2*a*c))
    gamma = np.arccos((b**2 + a**2 - c**2)/(2*b*a))

    alphaDeg = np.rad2deg(alpha)
    betaDeg = np.rad2deg(beta)
    gammaDeg = np.rad2deg(gamma)

    angle1 = alphaDeg + 45
    
    z=np.sqrt((boxLeg**2)+(b**2)-(2*boxLeg*b*np.cos(angle1)))
    mu = np.arcsin((np.sin(angle1)*b)/z)
    direction =ceiling-mu   

    return direction

def findCase(SNRmax, SNRsecond, snr1, snr2, snr3, snr4):


    if(SNRmax == snr1 and SNRsecond == snr4):
        casenum = 1
        ceiling = 45

    elif(SNRmax == snr1 and SNRsecond == snr2):
        casenum = 2
        ceiling = 90

    elif(SNRmax == snr2 and SNRsecond == snr1):
        casenum = 3
        ceiling = 135

    elif(SNRmax == snr2 and SNRsecond == snr3):
        casenum = 4
        ceiling = 180

    elif(SNRmax == snr3 and SNRsecond == snr2):
        casenum = 5
        ceiling = 225

    elif(SNRmax == snr3 and SNRsecond == snr4):
        casenum = 6
        ceiling = 270

    elif(SNRmax == snr4 and SNRsecond == snr3):
        casenum = 7
        ceiling = 315

    elif(SNRmax == snr4 and SNRsecond == snr1):
        casenum = 8
        ceiling = 360
    else:
        casenum = 0
        ceiling = 0
    #print("Case Number: ", casenum,"\n")
    #print("Ceiling: ", ceiling,"\n")

    return casenum, ceiling



    
def main():
    clear = lambda: os.system('clear')
    clear()    
    print("\nFALCON-B Tracking and Monitoring Software v0.0.2.")
    print("Created by Ian Carney, Michael Krzystowczyk, William Lee, and Frank Palermo.")
    print("Louisiana Tech University")
    print("This program is for technical demonstration only and is not for use\nin any commercial, industrial, or operational environments.\n")

    sdrgain = 5
    bw = 32e3
    sampRate = 1.024e6
    correction = 50



    #global snr1, snr2, snr3, snr4
    if len(sys.argv)==2:
        centerfreq = sys.argv[1]
    else:
        centerfreq = 462562500

    #Configures SDR1
    sdr1 = RtlSdr(serial_number='0000101')
    sdr1.sample_rate = sampRate
    sdr1.bandwidth = bw
    sdr1.center_freq = centerfreq
    print(sdr1.center_freq)
    sdr1.gain=5
    sdr1.freq_correction = correction

    #Configures SDR2
    sdr2 = RtlSdr(serial_number='0000102')
    sdr2.sample_rate = sampRate
    sdr2.bandwidth = bw
    sdr2.center_freq = centerfreq
    sdr2.gain=5
    sdr2.freq_correction = correction

    #Configures SDR3
    sdr3 = RtlSdr(serial_number='0000103')
    sdr3.sample_rate = sampRate
    sdr3.bandwidth = bw
    sdr3.center_freq = centerfreq
    sdr3.gain=5
    sdr3.freq_correction = correction

    #Configures SDR4
    sdr4 = RtlSdr(serial_number='0000104')
    sdr4.sample_rate = sampRate
    sdr4.bandwidth = bw
    sdr4.center_freq = centerfreq
    sdr4.gain=4
    sdr4.freq_correction = correction

    while(1):
        print("Collecting data...")
        
        sdr1data = readValues(sdr1, sampRate) #Returns Power of SDR1
        sleep(0.1)
        sdr2data = readValues(sdr2, sampRate) #Returns Power of SDR2
        sleep(0.1)
        sdr3data = readValues(sdr3, sampRate) #Returns Power of SDR3
        sleep(0.1)
        sdr4data = readValues(sdr4, sampRate) #Returns Power of SDR4

        snr1 = np.float32(getSNR(sdr1data)) #Returns SNR of SDR1
        snr2 = np.float32(getSNR(sdr2data)) #Returns SNR of SDR2
        snr3 = np.float32(getSNR(sdr3data)) #Returns SNR of SDR3
        snr4 = np.float32(getSNR(sdr4data)) #Returns SNR of SDR4
        all_snr = [snr1, snr2, snr3, snr4] #Puts all SDR Data in an array
        #print("All SNR: ")
       # print(all_snr)
        all_snr.sort()
        #print("Sorted SNR: ")
        highSNR = all_snr[-1] #Gets highest SNR
        secondSNR = all_snr[-2] #Gets second highest SNR
	if(highSNR == snr1):
		snr3 = 0
	if(highSNR == snr2):
		snr4 = 0
	if(highSNR == snr3):
		snr1 = 0
	if(highSNR == snr4):
		snr2 = 0
	all_snr2 = [snr1, snr2, snr3, snr4]
	#print(all_snr2)
	all_snr2.sort()
	highSNR2 = all_snr2[-1]
	secondSNR2 = all_snr2[-2]
	#print(all_snr2)
        #print("High SNR: ", highSNR,"\n")
        #print("Second SNR: ", secondSNR, "\n")

        if((highSNR2 or secondSNR2) != 0 and (highSNR2 or secondSNR2) > 2):
            shortDist = getDist(highSNR2) #Uses highest SNR to find distance
            #longDist = getDist(secondSNR2) #Gets distance from second highest antenna SNR
         #   print(highSNR, secondSNR)
            #print(snr1, snr2, snr3, snr4)
            try:
                case, ceiling = findCase(highSNR2, secondSNR2, snr1, snr2, snr3, snr4)
                minDist, maxDist, colorZone = findZone(highSNR)
                locationMatrix = [case, colorZone]
                #print("The signal is between ", minDist, " feet away and ", maxDist, " feet away.")
                if(case==0):
                    raise TypeError
          #      print("\n")
          #      print("Case Number: ", case)
          #      print("Ceiling: ", ceiling, " degrees")

                #angle = dirFind(shortDist, longDist, ceiling)
                print("Signal Detected!")
                print "Distance: ", minDist, " to ", maxDist, " feet away."
                #print "Distance Zone: ", colorZone
                print "Direction Zone: ", case
                print "Ceiling: ", ceiling, " degrees to ", ceiling-45, " degrees"
                
                #print("Signal Detected! There is a signal that is ", shortDist, " away at an angle of ", angle, " degrees.")
                for _ in range(2):
                    print('\n')
            except:
            #    print("Casenum Error")
                print("Error")

if(__name__ == "__main__"):
    main()
   

