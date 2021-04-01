import numpy as np
from rtlsdr  import RtlSdr
import os, sys
from time import sleep
#import matplotlib
#import matplotlib.pyplot as plt
#np.set_printoptions(threshold=sys.maxsize)


def readValues(receiver,samp_rate):
    print(samp_rate)
    data = receiver.read_samples(1024000)
    valueDBFS = 20*np.log10(abs(data)/32768)
    SigPower = 10*np.log10(10*((data.real**2)+(data.imag**2)))
    return SigPower
    


def getSNR(power):
    mean = np.mean(power)
    st_dev = np.std(power)
    dist_mean = abs(power-mean)
    max_dev = 1
    not_outlier = dist_mean < (max_dev * st_dev)
    no_outliers = power[not_outlier]
    Pmax = max(no_outliers)
    Pmin = min(no_outliers)
    floor = -35.1205
    print("Maximum SNR: ", Pmax)
    print("Minimum SNR: ", Pmin)
    SNR = Pmax-floor
    #snr_vals[i] = SNR
    #print("The SNR is ", SNR)

   # snr_vals = np.append(snr_vals, SNR)
    return SNR
    

def getDist(SNR):


    print(SNR)
    x = SNR 
    ColdDist = 0.1245*(x**2)-10.659*x+212.36
    WarmDist = -0.0857*(x**3)+6.2553*(x**2)-155.33*(x)+1342.8
    frank = .0177*(x**3)-.9015*(x**2)+10.86*(x)+27.934
    ian = .0195*(x**3)-1.0075*(x**2)+12.906*(x)+14.742
    will = (frank + ian)/2
    mike = .0174*(x**3)-.8964*(x**2)+10.857*(x)+29.338
    #print("eq1", frank)
    #print("eq2", ian)
    #print("eq3 ", will)
    #print('mike', mike)
    print("The distance is between", mike-2, "and", mike+2,"ft. away")
    #print("Cold Distance: ", ColdDist)
    #print("Warm Distance: ", WarmDist)
    #print('\n')
    

    return mike

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

    elif(SNRmax == snr3 and SNRsecond == snr4):
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
  

    return casenum, ceiling



    
def main():
    clear = lambda: os.system('clear')
    clear()    
    print("\nFALCON-B Tracking and Monitoring Software v0.0.2.")
    print("Created by Ian Carney, Michael Krzystowczyk, William Lee, and Frank Palermo.")
    print("Louisiana Tech University")
    print("This program is for technical demonstration only and is not for use\nin any commercial, industrial, or operational environments.\n")

    print("Version Notes: Adds ability to coordinate direction with multiple antennas.\n")

    sdrgain = 0
    bw = 32e3
    sampRate = 1.024e6
    correction = 50

    #global snr1, snr2, snr3, snr4
    if len(sys.argv)==2:
        centerfreq = sys.argv[1]
    else:
        centerfreq = 462662500 - (correction/2)

    #print(len(sys.argv))
    #print(sys.argv[0])

    sdr1gain = 25
    sdr2gain = 25
    sdr3gain = 25
    sdr4gain = 25

    #Configures SDR1
    sdr1 = RtlSdr(serial_number='0000101')
    sdr1.sample_rate = sampRate
    sdr1.bandwidth = bw
    sdr1.center_freq = centerfreq
    sdr1.gain=sdrgain
    sdr1.freq_correction = correction

    #Configures SDR2
    sdr2 = RtlSdr(serial_number='0000102')
    sdr2.sample_rate = sampRate
    sdr2.bandwidth = bw
    sdr2.center_freq = centerfreq
    sdr2.gain=sdrgain
    sdr2.freq_correction = correction

    #Configures SDR3
    sdr3 = RtlSdr(serial_number='0000103')
    sdr3.sample_rate = sampRate
    sdr3.bandwidth = bw
    sdr3.center_freq = centerfreq
    sdr3.gain=sdrgain
    sdr3.freq_correction = correction

    #Configures SDR4
    sdr4 = RtlSdr(serial_number='0000104')
    sdr4.sample_rate = sampRate
    sdr4.bandwidth = bw
    sdr4.center_freq = centerfreq
    sdr4.gain=sdrgain
    sdr4.freq_correction = correction

    print("Center Frequency: ", centerfreq)
    while(1):
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
        print("All SNR: ")
        print(all_snr)
        all_snr.sort()
        print("Sorted SNR: ")
        print(all_snr)
	#reg_list = np.tolist(sorted_snr)
        highSNR = all_snr[-1] #Gets highest SNR
        secondSNR = all_snr[-2] #Gets second highest SNR
        print("High SNR: ", highSNR,"\n")
        print("Second SNR: ", secondSNR, "\n")

        if((highSNR or secondSNR) != 0 and (highSNR or secondSNR) > 2):
            shortDist = getDist(highSNR) #Uses highest SNR to find distance
            longDist = getDist(secondSNR) #Gets distance from second highest antenna SNR
            print("Printing vals that go into findcase\n")
            print(highSNR, secondSNR)
            print(snr1, snr2, snr3, snr4)
            try:
                case, ceiling = findCase(highSNR, secondSNR, snr1, snr2, snr3, snr4)
                if(case==0):
                    raise TypeError
                print("\n")
                print("Case Number: ", case)
                print("Ceiling: ", ceiling, " degrees")

                angle = dirFind(shortDist, longDist, ceiling)

                print("Signal Detected! There is a signal that is ", shortDist, " away at an angle of ", angle, " degrees.")
            except TypeError:
                print("Casenum Error")
                pass

if(__name__ == "__main__"):
    main()
   

