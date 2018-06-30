# A simple Progress Bar for Python
## Motivation behind it
If you need a two-liner to track the progress of any application where the number of total iterations is known  

I got tired of people not including progress tracking metrics  

## Usage example
```
import ProgressBar as PB

[...]  

pb = PB.ProgressBar(n)
for i in range(1,n):
    pb.CheckProgress()
    [do complicated stuff]
 ```
*You can also run the file itself to see a short demo*  
 It will look something like this (and it will make a sound at the end. It can be disabled):  
![alt Text](https://i.imgur.com/x8VRPvv.gif)
 
**Please note that updating the output relies on deleting the contents of the current output line. This means that if you also have other information printed out, the LAST LINE will be overwritten (so please put a newline at the end)**

  
 ## The default configuration:  
 print the percentage at most every two seconds (if an iteration is longer than two seconds, it is not possible to print every 2 seconds, obviously)

 ## Summary of parameters on class instantiation
  ### Required  
  - **totalIterationCount** The total number of expected iterations
  ### Optional
  - **displayInterval** The minumum amount of time between refreshing the output. Expressed in seconds. Default = **2**.
  - **sound** Play a sound when 100% is reached. Should work on most versions of Windows, Linux and Mac. If you do not have powershell (e.g. Win XP),you may experience choppy sound. If the sound driver is not loaded properly, the sound section is ignored
     - 'off'  - no sound played
     - 'bip'   - a short beep
     - 'bup'   - a short beep, two octaves lower than bip
     - 'beep'  - a longer beep
     - 'micro' - microwave style beep-beep-beep
     - 'tune'  - a melody ([HU]'Kicsi kutya tarka')
     - **'auto'**    - Selects sound based on estimated task duration at 1%:
         - \<30s       =\> bip  
         - \[30s,2min)  =\> beep  
         - \[2min,8min) =\> micro  
         - \>=8min     =\> tune  
      - anyting else => silent
	  - *You can use pb.playTune() to check out what tune sounds like*
  - **emoji** -- The type of emoji that will be displayed  
       - 'ascii' - to be sure it works on older consoles
       - **'kao'**   - full faces using UTF-8 characters
       - 'off'   - less emotional, more professional
 
## Documentation  
Standard python documentation has been included for the class and functions  
To check the details about the parameters use  
```
#Check class parameters
print(ProgressBar.__doc__)

#Check the parameters of a function
print(ProgressBar.checkProgress.__doc__)
```
 
