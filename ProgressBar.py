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
    
    displayInterval -- the minumum amount of time between two print
            statements. Expressed in seconds
    sound -- Play a sound when 100% is reached. REQUIRES NUMPY. Should work on most versions 
                of Windows, Linux and Mac. Earlier versions than Windows 7 may 
                experience choppy sound. If the sound driver is not loaded properly,
                the sound section is ignored
            'off'   - no sound played
            'bip'   - a short beep
            'bup'   - a short beep, two octaves lower than bip
            'beep'  - a longer beep
            'micro' - microwave style beep-beep-beep
            'tune'  - a melody ([HU]'Kicsi kutya tarka')
            'auto'  - Selects sound based on estimated task duration at 1%:
                        <30s       => bip
                        [30s,2min) => beep
                        [2mins,5min)=> micro
                        >=5min     => tune
            anyting else => silent
            You can use playTune() to check out what tune sounds like
    emoji -- The type of emoji that will be displayed
            'ascii' - to be sure it works on older consoles
            'kao'   - full faces using UTF-8 characters
            'off'   - less emotional, more professional
            1   -> display every percentage
            10  -> display 10%,20%...
            '''
            
    class _with_file_creation:
        def __init__(self,np,wave,os,player):
            self.player = player
            self.np = np
            self.wave=wave
            self.os=os
            self.samplerate = 44100
            self.samplewidth = 2 #16 bits, therefore 2 bytes
            self.channels = 1 #mono is fine for now
            self.amplitude = (2**15)*0.79432
            self.samples_offset = 0
            self.raw_audio = None
        def create(self,frequency,duration):
            ''' Creates a 16-bit wav file containing the melody specified.
            _play_stop_with_file_creation needs to be called to play the file and
            delete it after playing has finished        
            '''        
    
            #TODO: considering the usage, this should be converted into a class of its own
            duration *= self.samplewidth/1000.0
            
            samples = int(self.samplerate*duration)
            samples = samples-int(samples%(float(self.samplerate)/frequency))
                        
            
            if self.raw_audio is None:
                self.raw_audio = self.np.empty(samples,dtype=self.np.int16)
            else:
                self.raw_audio = self.np.resize(self.raw_audio,(self.samples_offset+samples,1))
                
            for i in range(samples):
                self.raw_audio[self.samples_offset+i]= self.amplitude*self.np.sin(self.np.pi*2*frequency*i/self.samplerate)
                
            self.samples_offset += samples
    
        def play(self, remove_raw_audio=True,remove_created_file=True):
            '''plays the file created and deletes it after playback has finished
            '''
            filename = '__temp_success_tune.wav';
            g = self.wave.open(filename,'wb')
            
#            g.setnchannels(self.channels)
#            g.setsampwidth(self.samplewidth)
#            g.setframerate(self.samplerate)
#            g.setnframes(self.samples_offset)
            g.setparams((self.channels,self.samplewidth,self.samplerate,\
                        self.samples_offset,'NONE','NONE'))
            #TODO: there appears to be a bug in the wave library where the length 
            #of data written is divided by the sample_width
            g.writeframes(self.np.resize(self.raw_audio,(self.samples_offset*2,1)))
            g.close()
#            import matplotlib.pyplot as plt
#            plt.figure(figsize=(50,1),dpi=200)
#            plt.plot(self.raw_audio)
#            plt.show()
            self.os.system(self.player%filename)
    
            if remove_raw_audio == True:
                self.samples_offset = 0
                self.raw_audio = None
    
            if remove_created_file == True:
                self.os.remove(filename)


            
    try:
        #TODO: remove numpy dependency
        import numpy as np
        import wave
        import os
        import platform
        if platform.system() == 'Windows':
            #TODO: do a filecheck instead
            if int(platform.release())>=7:
                _player = 'powershell -c (New-Object Media.SoundPlayer \'%s\').PlaySync();'
            else:
                try:
                    import winsound
                    _player = 'winsound'
                    isSound = True;
                except:
                    raise SystemError('Windows OS detected, but no player or winsound')
        elif platform.system() == 'Darwin':
            _player = 'afplay %s'
        elif platform.system() == 'Linux':
            _player = 'aplay %s'
        else:
            raise SystemError('Operating system not recognized')
        
        #it is much better to not have sound, than to crash the rest of the code,
        #thus the try-chatches within the definitions
        if _player == 'winsound':
            def _play_freq(self,freq,duration): 
                try: 
                    self._play_with_winsound(freq,duration) 
                except: 
                    pass
            def _play_stop(self): return   
        else: 
            _player_with_file_creation = _with_file_creation(np,wave,os,_player)
            def _play_freq(self,freq,duration): 
                try: 
                    self._player_with_file_creation.create(freq,duration) 
                except: 
                    pass
            def _play_stop(self): 
                try: 
                    self._player_with_file_creation.play() 
                except: 
                    pass

        del np
        del wave
        del os
        del platform            
        isSound = True
    except:            
        isSound= False
        
    valid_sounds = ['bip','bup','beep','micro','tune','auto']
    emojis={'ascii':[':(',':|',':)',':D','\m/(^.^)\m/'],
            'kao':['(╯_╰)',	'(￣.￣)','(─‿‿─)','＼(￣▽￣)／','☆*:.｡o(≧▽≦)o｡.:*☆']}
    
    
    def __init__(self,totalIterationCount, displayInterval=2,
                      sound='auto', emoji='kao'):

        if totalIterationCount<1:
            raise ValueError('The number of iterations can not be <=0')
        self.n = totalIterationCount  
        self.currentIter = 0
                    
        self.displayInterval = displayInterval
                
        self.sound = sound
        self.emoji = emoji

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
            self.lastDisplayed = -self.displayInterval
            #this way the next if only has to check one condition, not two.
            #Marginal or irrelevant gains, I know
            self.currentIter = 1
            return
            
        #increment iterator    
        self.currentIter += 1
                
        #check if enough time has passed since last precentage print
        if t_now - self.lastDisplayed > self.displayInterval:
            #print precentage
            currentPercent = 100.0*self.currentIter / self.n
            self._erase_prev_output()
            print('\r%.2f%% complete. '%(currentPercent),end='')
            #update time
            self.lastDisplayed = t_now

            #Calculate and display remaining time
            ahead = (self.n-self.currentIter)*(t_now - self.t_start) / \
                        self.currentIter
            time_remaining_string = self._generate_time_string(ahead);
            print('Estimated time remaining: %s ' % time_remaining_string,end='')
            self._print_emoji(currentPercent)                
                
        if self.currentIter == self.n-1:
            time_it_took = self._generate_time_string(t_now-self.t_start,'%.2f')
            self._erase_prev_output()
            print('\r100% -- Finished!',end='')
            self._print_emoji(100)
            print(' The process took %s '% time_it_took)
            
            if self.sound=='auto':
                self._set_best_sound(t_now-self.t_start);
            self.playTune()
            
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
            self._play([(9,2),(0,1),(9,2),(0,1),(9,2)],6,100)
        if self.sound=='tune':
            self._play([('c',1),('e',1),('c',1),('e',1),('g',2),('g',2),
                        ('c',1),('e',1),('c',1),('e',1),('g',2),('g',2),
                        (13, 1),('b',1),('a',1),('g',1),('f',2),('a',2),
                        ('g',1),('f',1),('e',1),('d',1),('c',2),('c',2)]
                ,tempo=180)
        if self.sound=='tune2':
            self._play([('c#',2),('f#',1),('a',2),('f#',1),('f',2),
                        ('f#',1),('g#',1/4.0),('f#',2),
                        ('d',2),('e',1/4.0),('f#',1/4.0),('c#',2),
                        ('b3',0.25),('a3',0.25),('a3',0.25),('g#3',0.25),('g#3',0.75),
                        ('c#',0.5),('f#3',2)                        
                        ],tempo=120)
        return


    '''Private:'''
    #Printing:
    def _generate_time_string(self,time,seconds_format='%d'):
        '''format it into a h:m:s format'''
        
        time_string = (seconds_format+' second')%(time%60)
        if int(time)!=1:
            time_string = time_string + 's';
            
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
                time_string = '%d hours '%(time/3600)  \
                                    + time_string
        return time_string
        
    def _erase_prev_output(self):
        for i in range(1,50):
            print('\b \b',end='')
            
    def _print_emoji(self,currentPercent):
        '''Prints the appropriate emoji for the percentage'''
        if self.emoji in self.emojis:
            if int(currentPercent)!=100:
                print(self.emojis[self.emoji][int(currentPercent/25)],end='')
            else:
                print(self.emojis[self.emoji][-1],end='')

    def _set_best_sound(self,ahead):
        '''Selects appropriate sound profile based on remaining time'''
        if ahead<30: #bip
            self.sound = self.valid_sounds[0]
        elif ahead<120: #beep
            self.sound = self.valid_sounds[2]
        elif ahead<480: #micro
            self.sound = self.valid_sounds[3]
        else:           #tune
            self.sound = self.valid_sounds[4]

    #Sounds
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
            duration = int(note[1]*1000*60/tempo/4);
            if note[0]==0:
                self._play_freq(0,duration)
            else:
                self._play_freq(int(2**((octave*12+note[0]-58)/12.0)*440),
                              duration)    
        #this allows for system independent approach: If the system requires all
        #all notes to be queued first, than start playing, this should be called
        #at the end. Otherwise it is filled with a return and is a dummy
        self._play_stop()
        
        
    def _play_with_winsound(self,frequency,duration):
        '''Uses the windound module to play the frequencies specified
        If the playback sound choppy try _play_with_file_creation
        
        frequencies below 37 are not supported. These are considered rest a.k.a.
        silence
        '''
        if frequency >37:
            self.winsound.Beep(frequency,duration)
        else:
            time.sleep(duration/1000.0)

if __name__ == "__main__":
    
    #number of iterations    
    n = 3300;
    
    #tune the length of the fake work -- stand-in for 'sleep'
    m = 30000;
    #using default parameters
    #pb = ProgressBar(n,sound='tune');
    pb = ProgressBar(n)    
    for i in range(1,n):
        pb.checkProgress();
        
        k=0;
        for j in range(1,m):
            k=k+1;
        
