# -*- coding: utf-8 -*-
"""
Created on Mon Jun 11 10:59:03 2018

@author: Hesiris
"""
from __future__ import print_function
import time
#there are some other imports inside the try block in the music section,
#but if those fail, they should be silently ignored

class ProgressBar:
    ''' Initializes the progress bar. Should be called directly before the loop
    It only requires one line of output, because it rewrites the last line, 
    therefore please use a newline at the end of your final output.
    
    totalIterationCount -- the total number of expected iterations
    
    displayInterval -- the minumum amount of time between two print
            statements. Expressed in seconds
    sound -- Play a sound when 100% is reached. Should work on 
                most versions of Windows, Linux and Mac. Should work on most 
                versions of Windows, Linux and Mac. If you do not have 
                powershell (e.g. Win XP),you may experience choppy sound.
                If the sound driver is not loaded properly,
                the sound section is ignored
            'off'   - no sound played
            'bip'   - a short beep
            'bup'   - a short beep, two octaves lower than bip
            'beep'  - a longer beep
            'micro' - microwave style beep-beep-beep
            'tune'  - a melody ([HU]'Kicsi kutya tarka')
            'tune2' - Hungarian Dance
            'auto'  - Selects sound based on estimated task duration at 1%:
                        <30s       => bip
                        [30s,2min) => beep
                        [2mins,5min)=> micro
                        >=5min     => tune
            anyting else => silent
            You can use play_tune() to check out what tune sounds like
    emoji -- The type of emoji that will be displayed
            'ascii' - to be sure it works on older consoles
            'kao'   - full faces using UTF-8 characters
            'off'   - less emotional, more professional
            1   -> display every percentage
            10  -> display 10%,20%...
    
    '''
    #%% 'Constants'
    valid_sounds = ['bip','bup','beep','micro','tune','tune2','auto']
    emojis={'ascii':[':(',':|',':)',':D','\m/(^.^)\m/'],
            'kao':['(╯_╰)',	'(￣.￣)','(─‿‿─)','＼(￣▽￣)／','☆*:.｡o(≧▽≦)o｡.:*☆']}
    #if you want to modify the sound module, enabling this is probably a good 
    #idea: exceptions will now print the stacktrace instead of remaining silent
    debug=False            
    #%% 'Public' functions
    def __init__(self,totalIterationCount, displayInterval=2,
                      sound='auto', emoji='kao'):

        if totalIterationCount<1:
            raise ValueError('The number of iterations can not be <=0')
        self.n = totalIterationCount  
        self.currentIter = 0
                    
        self.displayInterval = displayInterval
                
        self.sound = sound
        self.emoji = emoji

    def check_progress(self):
        '''Call this function on each iteration. It only prints when necessary
        
        The internal iterator is incremented automatically.
        '''
        #Use the same time across the function to avoid potential discrepancies
        t_now = time.perf_counter()
        
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
            time_remaining_string = self._generate_time_string(ahead)
            print('Estimated time remaining: %s ' % time_remaining_string,end='')
            self._print_emoji(currentPercent)                
                
        if self.currentIter == self.n-1:
            time_it_took = self._generate_time_string(t_now-self.t_start,'%.2f')
            self._erase_prev_output()
            print('\r100% -- Finished!',end='')
            self._print_emoji(100)
            print(' The process took %s '% time_it_took)
            
            if self.sound=='auto':
                self._set_best_sound(t_now-self.t_start)
            self.play_tune()
            
    def play_tune(self):
        ''' If you want to check the tune currently set'''
    
        #If sound is not supported or not requested
        if not self.isSound or self.sound not in self.valid_sounds:
            return
        
        if self.sound=='bip':
            self._play([(9,1)],6,160) #A_6
        if self.sound=='bup':   
            self._play([(9,1)],4,160) #A_4
        if self.sound=='beep':
            self._play([(9,1)],6,tempo=65)
        if self.sound=='micro':
            self._play([(9,2),(0,1),(9,2),(0,1),(9,2)],6,80)
        if self.sound=='tune':
            self._play([('c',1),('e',1),('c',1),('e',1),('g',2),('g',2),
                        ('c',1),('e',1),('c',1),('e',1),('g',2),('g',2),
                        (13, 1),('b',1),('a',1),('g',1),('f',2),('a',2),
                        ('g',1),('f',1),('e',1),('d',1),('c',2),('c',2)]
                ,tempo=160)
        if self.sound=='tune2':
            self._play([\
                        ('c#',3),('f#',1),('a',3),('f#',1),
                        ('f',3),('f#',0.5),('g#',0.5),('f#',4),
                        ('d',3),('e',0.5),('f#',0.5),('c#',4),
                        ('b3',0.5),('a3',0.5),('a3',0.5),('g#3',0.5),('g#3',1.5),
                        ('c#',0.5),('f#3',4),                       

                        ('c#',1.5),('f#',0.5),('a',0.5),('c#5',.5),
                        ('f#5',.5),('a5',.5),('c#6',3),('a5',1),
                        ('g#5',3),('a5',0.5),('b5',0.5),('a5',5),
            
                        ('d5',.5),('e5',.5),('f#5',.5),('d5',.5),
                        ('c#5',.5),('d5',.5),('e5',.5),('c#5',.5),
                        ('b4',.5),('c#5',.5),('d5',.5),('b4',.5),
                        ('a4',.5),('b4',.5),('c#5',.5),('a4',.5),
                        ('b4',.5),('a4',.5),('a4',.5),('g#4',.5),('g#4',1.5),
                        ('c#5',.5),('f#4',2),('a',0.125),('c#5',0.125),('f#5',0.5),
                        (0,1.5),

                        ('c#5',.5),(0,1.5),('c#5',.5),(0,1.5),('d5',3),('c#5',1),
                        (0,1),('b',2),('bb',.5),('b',.5),('c#5',.5),('b',.5),
                        ('bb',.5),('c#5',.5),('b',1),(0,1.5),

                        ('b',.5),(0,1.5),('b',.5),(0,1.5),('c#5',3),('b',1),
                        (0,1),('a',2),('g#',.5),('a',.5),('b',.5),('a',.5),
                        ('g#',.5),('b',.5),('a',1),(0,1),

                        ('g#',1.9),(0,0.1),('g#',2),('b',0.5),(0,1),('a',2.5) ,
                        ('g#',3),('f#',3.5),('f',1),('f#',1),('g#',1),('f#',1),
                        ('f',1),('g#',1),('f#',2),(0,2),

                        ('f5',0.25),('g#5',0.125),('c#6',0.125),(0,2),
                        ('c#',0.5),(0,0.25),('d#',0.5),(0,1.5),('f',0.5),(0,1.5),
                        ('g#',0.5),('f#',0.5),(0,0.5),('f#',2),                  
                        ('f',0.5),('f#',0.5),('g#',0.5),('f#',0.5),('f',0.5),
                        ('f#',0.5),('g#',0.5),('f#',0.5),(0,1),

                        ('b',0.25),('d5',0.125),('f#5',0.125),('g#5',0.125),(0,1.5),
                        ('b',0.25),('c#5',0.125),('f5',0.125),('g#5',0.125),(0,1.5),
                        ('a',0.25),('c#5',0.25),('f#5',2)
                        ],octave=4,tempo=150)
        return


    #%% 'Private' Functions: print related
    def _generate_time_string(self,time,seconds_format='%d'):
        '''format it into a h:m:s format'''
        
        time_string = (seconds_format+' second')%(time%60)
        if int(time)!=1:
            time_string = time_string + 's'
            
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
        '''Erases previous output from the same line using \\b special character
        '''
        #If the hour is displayed as well, it can get up to 75 chars. 
        #An other 25 for good measure. Also, I don't know why it doesn't work,
        #if I only use '\b', it only prints if there is at least one, I presume,
        #non-escaped character
        for i in range(1,100):
            print('\b \b',end='')
            
    def _print_emoji(self,currentPercent):
        '''Prints the appropriate emoji for the percentage

        Takes the first four based on int(currentPercent/25) plus the last one 
        on completion        
        '''
        if self.emoji in self.emojis:
            if int(currentPercent)!=100:
                print(self.emojis[self.emoji][int(currentPercent/25)],end='')
            else:
                print(self.emojis[self.emoji][-1],end='')

    #%% 'Private' Functions: sound related
    def _set_best_sound(self,ahead):
        '''Selects appropriate sound profile based on remaining time
        
        Current time-table (puns FTW):
        0-30sec - bip
        30-120sec - beep
        2-8min - micro
        8-38min - tune
        Planning to add a tune2 for >38mins'''
        if ahead<30: #bip
            self.sound = self.valid_sounds[0]
        elif ahead<120: #beep
            self.sound = self.valid_sounds[2]
        elif ahead<640: #micro
            self.sound = self.valid_sounds[3]
        elif ahead<2280:           #tune
            self.sound = self.valid_sounds[4]
        else:
            self.sound = self.valid_sounds[5]

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
                try:
                    modifier = note_lit[1]
                    note_lit = note_lit[0].upper()
                except:
                    modifier = ''
                    note_lit = note_lit.upper()                        
                note = (notes[note_lit+modifier],note[1])
            duration = int(note[1]*1000*60/tempo/4)
            if note[0]==0:
                self._play_freq(0,duration)
            else:
                self._play_freq(int(2**((octave*12+note[0]-58)/12.0)*440),
                              duration)    
        #this allows for system independent approach: If the system requires all
        #all notes to be queued first, than start playing, this should be called
        #at the end. Otherwise it is filled with a return and is a dummy
        self._play_stop()
        
    #%% Sound engine definition. Needs to be done before OS detection, as
    # Forward class definitions are not allowed  
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
            
    class _with_file_creation:
        import math
        from array import array
        import sys
        import wave
        def __init__(self,os,player):
            self.player = player
            self.os=os
            self.samplerate = 44100
            self.samplewidth = 2 #16 bits, therefore 2 bytes
            self.channels = 1 #mono is fine for now
            self.amplitude = int((2**15)*0.708)
            self.samples_offset = 0
            self.raw_audio = None
        def create(self,frequency,duration):
            ''' Creates a 16-bit wav file containing the melody specified.
            _play_stop_with_file_creation needs to be called to play the file and
            delete it after playing has finished        
            '''        

            duration *= self.samplewidth/1000.0
            
            samples = int(self.samplerate*duration)
            #Removes popping sounds by removing the last unfinished period from
            #the sine wave            
            if frequency > 1:
                samples = samples-int(samples%(float(self.samplerate)/frequency))
                        
            if self.raw_audio is None:
                # 'h' = singed short (2B)
                self.raw_audio = self.array('h',[0])*samples
            else:
                self.raw_audio += self.array('h',[0])*samples
                
            for i in range(samples):
                self.raw_audio[self.samples_offset+i]= int(self.amplitude*\
                    self.math.sin(self.math.pi*2*frequency*i/self.samplerate))
                
            #reduce popping even further and add a small pause between notes
            lim = int(min(0.02*self.samplerate,samples/3))
            #The linear approach seems to be better with pop reduction
            for i in range(lim):
                #exponential approach: e^(-t/(lim/4))
#                self.raw_audio[-lim+i] = int(self.raw_audio[-lim+i]*\
#                        (self.math.exp(-1.0*i/(lim/4))))
#                self.raw_audio[self.samples_offset+lim-i-1] = \
#                        int(self.raw_audio[self.samples_offset+lim-i-1]*\
#                        (self.math.exp(-1.0*i/(lim/4))))
                #linear appraoch:
                self.raw_audio[-i-1] = int(self.raw_audio[-i-1]*1.0*i/lim)
                self.raw_audio[self.samples_offset+i] = int(self.raw_audio[self.samples_offset+i]*1.0*i/lim)
                
            self.samples_offset += samples
    
        def play(self, remove_raw_audio=True,remove_created_file=True):
            '''plays the file created and deletes it after playback has finished
            '''
            filename = '__temp_success_tune.wav'
            g = self.wave.open(filename,'wb')
            
            g.setnchannels(self.channels)
            g.setsampwidth(self.samplewidth)
            g.setframerate(self.samplerate)
            g.setnframes(self.samples_offset)
            if self.sys.version_info<(3,0):
                #In python2 there is a bug in the wave library where the length 
                #of data written is divided by the sample_width, that was fixed in
                #python3
                g.writeframes(self.raw_audio*2)                    
            else:
                g.writeframes(self.raw_audio)
            g.close()

            self.os.system(self.player%filename)
    
            if remove_raw_audio == True:
                self.samples_offset = 0
                self.raw_audio = None
    
            if remove_created_file == True:
                self.os.remove(filename)

    #%% Choose best sound setting based on OS availability. E.g. The base player
    # is 'aplay' for Linux, 'asplay' for MacOS (Darwin kernel)
    try:
        import os
        import platform
        if debug:
            import traceback
        if platform.system() == 'Windows':
            #Checks if powershell and Media.SoundPLayer are available
            if os.system('powershell -c (New-Object Media.SoundPlayer)') == 0:
                _player = 'powershell -c (New-Object Media.SoundPlayer \'%s\').PlaySync();'
            else:
                try:
                    import winsound
                    _player = 'winsound'
                    isSound = True
                except:
                    raise SystemError('Windows OS detected, but no player or winsound')
        elif platform.system() == 'Darwin':
            _player = 'afplay %s'
        elif platform.system() == 'Linux':
            _player = 'aplay %s'
        else:
            raise SystemError('Operating system not recognized')
        
        #it is much better to not have sound than to crash the rest of the code,
        #thus the try-chatches within the definitions
        if _player == 'winsound':
            def _play_freq(self,freq,duration): 
                try: 
                    self._play_with_winsound(freq,duration) 
                except: 
                    if self.debug: 
                        self.traceback.print_exc()
            def _play_stop(self): return   
        else: 
            _player_with_file_creation = _with_file_creation(os,_player)
            def _play_freq(self,freq,duration): 
                try: 
                    self._player_with_file_creation.create(freq,duration) 
                except: 
                    if self.debug: 
                        self.traceback.print_exc()
            def _play_stop(self): 
                try: 
                    self._player_with_file_creation.play() 
                except: 
                    if self.debug: 
                        self.traceback.print_exc()
    
        del os
        del platform            
        isSound = True
    except:            
        isSound= False
        if debug:
            print('Exception during init :isSound set to False.')
            traceback.print_exc()
    
#%% A simple test/demo
if __name__ == "__main__":
    
    #number of iterations    
    n = 3300
    #tune the length of the fake work -- stand-in for 'sleep'
    m = 40000
    
    #pb = ProgressBar(n,sound='tune2')
    pb = ProgressBar(n)    
    for i in range(1,n):
        pb.check_progress()
        
        k=0
        for j in range(1,m):
            k=k+1
        
