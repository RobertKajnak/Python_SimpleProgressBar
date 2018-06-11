# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:59:03 2018

@author: Hesiris
"""
from __future__ import print_function
import time

try:
    import winsound
    isSound = True;
except:
    isSound= False;
        

class ProgressBar:
    duration = 500;
    freq_base = 1;
    
    '''
    totalIterationCount -- the total number of expected iterations
    skipPercent -- the pecentage that are displayed:
            <=0 -> calculated based on time
            1   -> display every percentage
            10  -> display 10%,20%...
    percentageDisplayInterval -- the minumum amount of time between two print
            statements. Expressed in seconds
    timeRemainingDisplayInterval -- the minumum number of seconds elapsed between
            display remaining time. Expressed in seconds
    '''
    def __init__(self,totalIterationCount,sound='none',percentageDisplayInterval=2,
                 timeRemainingDisplayInterval=10, skipPercent=1):
        self.isSound = sound
        self.n = totalIterationCount        
    
        self.currentIter = 0
        self.currentPercent = 0
        
        self.percent = self.n/100
        self.skipPercent = skipPercent
        
        self.timeDisplayInterval = timeRemainingDisplayInterval
        self.percentageDisplayInterval = percentageDisplayInterval
    '''
    Call this function on each iteration. It only prints when necessary
    
    '''
    def checkProgress(self):
        #Use the same time across the function to avoid potential discrepancies
        t_now = time.clock();
        
        #Set starting time        
        if self.currentIter==0:
            print('Initializing Variables, calculating time estimate',end='')   
            self.t_start = t_now
            #The estimation will be guaranteed on first percent
            self.lastEstimated = -self.timeDisplayInterval
            self.lastDisplayed = -self.percentageDisplayInterval
            
        #increment iterator    
        self.currentIter += 1 
        
        #if a percentage mark is hit
        if self.currentIter % self.percent == 0:
            self.currentPercent += 1;
            
            #chek if it needs to be skipped
            if self.currentPercent % self.skipPercent == 0:
                
                #check if enough time has passed since last precentage  print
                if t_now - self.lastDisplayed > self.percentageDisplayInterval:
                    #print precentage
                    print('\n%d%% '%(self.currentPercent),end='')
                    #update time
                    self.lastDisplayed = t_now

                #Check if enough time has elapsed since last estimation print.
                if t_now - self.lastEstimated > self.timeDisplayInterval:
                    #Calculate and display remaining time
                    ahead = (100-self.currentPercent)*(t_now - self.t_start) / \
                                self.currentPercent
                    print('Time Remaining: %f seconds' % ahead,end='')
                    
                    #update estimation timestamp
                    self.lastEstimated = t_now
                
                
        if self.currentIter == self.n-1:
            print('\n100% - Finished!')
            self.playTune()
    
    '''
    If you want to check the current set tune
    '''
    def playTune(self):
        #If sound is not supported or not requested
        if not isSound:
            return;
            
        duration = self.duration;
        if isSound=='beep':
            freq_beep = self.freq_base * 440
            winsound.Beep(freq_beep, duration)
            
        if isSound=='melody':
            frequency_E = 660
            frequency_C = 513
            frequency_G = 783
            winsound.Beep(frequency_C, duration)
            winsound.Beep(frequency_E, duration)
            winsound.Beep(frequency_C, duration)
            winsound.Beep(frequency_E, duration)
            winsound.Beep(frequency_G, duration*2)
            time.sleep(duration/10.0)
            winsound.Beep(frequency_G, duration*2)
        return



if __name__ == "__main__":
    n = 30000;
    pb = ProgressBar(n,skipPercent=1);
    for i in range(1,n):
        k=0;
        for j in range(1,n):
            k=k+1;
        
        pb.checkProgress();
        
        
        '''if i%100==0:
            print('\n%d%% '%(i/100),end='')
        if i%10==0 and i%100!=0:
            print('#',end='')
    if i==9999:
        print('\n100% - Finished!')
    playTune();'''