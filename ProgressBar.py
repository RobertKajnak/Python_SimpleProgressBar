# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:59:03 2018

@author: Hesiris
"""
from __future__ import print_function
import time



class ProgressBar:
    ''' Initializes the progress bar. Should be called directly before the loop
    
    totalIterationCount -- the total number of expected iterations
    
    percentageDisplayInterval -- the minumum amount of time between two print
            statements. Expressed in seconds
    timeRemainingDisplayInterval -- the minumum number of seconds elapsed between
            display remaining time. Expressed in seconds
    sound -- Play a sound when 100% is reached. **ONLY works on MS Windows**
            'off'   - no sound played
            'bip'   - a short beep
            'bup'   - a short beep, two octaves lower than bip
            'beep'  - a longer beep
            'micro' - microwave style beep-beep-beep
            'tune'  - a melody ('Kicsi kutya tarka')
            'auto'  - Selects sound based on estimated task duration at 1%:
                        <10s       => bip
                        [10s,60s)  => beep
                        [60s,5min) => micro
                        >5min      => tune
            anyting else => silent
            You can use playTune() to check out what tune sounds like
    skipPercent -- the pecentage that are displayed. Takes priority over time 
                   estimate
            1   -> display every percentage
            10  -> display 10%,20%...
            '''
    try:
        import winsound
        def _play_freq(self,freq,duration): self.winsound.Beep(freq,duration)
        isSound = True;
    except:
        isSound= False;
        
    valid_sounds = ['bip','bup','beep','micro','tune','auto']
    
    
    def __init__(self,totalIterationCount,percentageDisplayInterval=2,
                 timeRemainingDisplayInterval=10, sound='auto', skipPercent=1):

        if totalIterationCount<1:
            raise ValueError('The number of iterations can not be <=0')
        self.n = totalIterationCount  
    
        self.currentIter = 0
        self.currentPercent = 0
        
        self.percent = self.n/100
        self.skipPercent = skipPercent if skipPercent>0 else 1
        
        self.timeDisplayInterval = timeRemainingDisplayInterval
        self.percentageDisplayInterval = percentageDisplayInterval
                
        self.sound = sound

    def checkProgress(self):
        '''Call this function on each iteration. It only prints when necessary
        
        The internal iterator is incremented automatically.
        '''
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
        
        #TODO - create subpercentages     
        
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
                    time_remaining_string = self._generate_time_string(ahead);
                    print('Estimated Time Remaining: %s' % time_remaining_string,end='')
                    
                    #update estimation timestamp
                    self.lastEstimated = t_now
                if self.sound=='auto':
                    if ahead<10: #bip
                        self.sound = self.valid_sounds[0]
                    elif ahead<60: #beep
                        self.sound = self.valid_sounds[2]
                    elif ahead<300: #micro
                        self.sound = self.valid_sounds[3]
                    else:           #tune
                        self.sound = self.valid_sounds[4]
                
                
        if self.currentIter == self.n-1:
            print('\n100% - Finished!')
            self.playTune()

    def _play(self,sheet,octave=4,tempo=80):
        ''' Plays the "sheet music" provided at a certain tempo
        
        octave is an offset addded to notes (440Hz is A in octave 4). Max=9
        sheet = an array of (note,duration) tuplets
            note: Can be specified either as a string e.g. 'C', 'c','c#' etc.
                    or as a number. If a digit is specified after the character, 
                    it overrides the octave settings, e.g. C#2 or D2 will 
                    always be in the second octave
                If this is specified as a digit:
                    0=rest; 1=C, 2=C#, 3=D; -1=B from previous octave, 13=C 
                    from next octave
                Feel free to mix the two formats e.g. notes=[(1,2),('C#',1/2)]
            duration: 1 unit is equal to 1/4 in the specified tempo
            tempo: specified in BPM
        '''
        notes = {'C':1,'C#':2,'Db':2,'D':3,'D#':4,'Eb':4,'E':5,'F':6,'F#':7,
                 'Gb':7,'G':8,'G#':9,'Ab':9,'A':10,'A#':11,'Bb':11,'Hb':11,
                 'B':12,'H':12}
        octave_base = octave
        for note in sheet:
            #convert to int if string format provided
            if type(note[0])==str:
                try:
                    octave = int(note[0][-1])
                    note_lit = note[0][:-1]                    
                except:
                    octave = octave_base
                    note_lit = note[0]
                note = (notes[note_lit.upper()],note[1])
            duration = int(note[1]*1000*60/tempo);
            if note[0]==0:
                time.sleep(duration/1000.0)
            else:
                self._play_freq(int(2**((octave*12+note[0]-58)/12.0)*440),
                              duration)    
    

    def playTune(self):
        ''' If you want to check the tune currently set'''
    
        #If sound is not supported or not requested
        if not self.isSound or self.sound not in self.valid_sounds:
            return;
        
        if self.sound=='bip':
            self._play([(9,1)],6,160) #A_6
        if self.sound=='bup':   
            self._play([(9,1)],4,160) #A_4
        if self.sound=='beep':
            self._play([(9,1)],6,tempo=65);
        if self.sound=='micro':
            self._play([(9,1),(0,1/2),(9,1),(0,1/2),(9,1)],6,63)
        if self.sound=='tune':
            self._play([('c',1),('e',1),('c',1),('e',1),('g',2),('g',2),
                        ('c',1),('e',1),('c',1),('e',1),('g',2),('g',2),
                        (13, 1),('b',1),('a',1),('g',1),('f',2),('a',2),
                        ('g',1),('f',1),('e',1),('d',1),('c',2),('c',2)]
                ,tempo=200)
            
        return


    '''Private:'''
    def _generate_time_string(self,time):
        '''format it into a h:m:s format'''
        #seconds is always a fractional value, therefore it is 
        #always plural
        time_string = '%.2f seconds'%(time%60)
        if time%3600 >= 60:
            if time%3600 < 120:
                time_string ='%d minunte '%((time/60)%60) \
                                    + time_string
            else:
                time_string ='%d minuntes '%((time/60)%60) \
                                    + time_string
                                    
        if time>=3600:
            if time<7200:
                time_string = '%d hour '%(time/3600)  \
                                    + time_string
            else:
                time_string = '%d hour '%(time/3600)  \
                                    + time_string
        return time_string

if __name__ == "__main__":
    n = 10000;
    #using default parameters
    pb = ProgressBar(n);
    for i in range(1,n):
        pb.checkProgress();
        
        k=0;
        for j in range(1,n):
            k=k+1;
        
        
