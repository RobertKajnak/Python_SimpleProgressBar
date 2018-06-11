# Python_SimpleProgressBar
If you need a two-liner to track the progress of any application where the number of total iterations is known  

I got tired of people not including progress tracking metrics  

## Usage example
```
import ProgressBar as ProgressBar

[...]  

pb = ProgressBar(n)
for i in range(1,n):
    pb.CheckProgress()
    [do complicated stuff]
 ```
**You can also run the file itself to see a short demo**
  
  
  
 ## The default configuration:  
 print the percentage at most every 2 seconds  
 print the time estimation at most every 10 seconds  

 ## Summary of parameters on class instantiation
  ### Required
    - **totalIterationCount** -- the total number of expected iterations
  ### Optional
    - **percentageDisplayInterval** -- the minumum amount of time between two print statements. Expressed in seconds. Default = **2**. If 1% of the works takes 0.2 seconds to complete, then 1%,6%,11% etc. will be printed
    - **timeRemainingDisplayInterval** -- the minumum number of seconds elapsed between display remaining time. Expressed in seconds. Default = **10**
    - **sound** -- Play a sound when 100% is reached. **ONLY works on MS Windows** Support for other OSs may be coming in future versions
        - 'off'  - no sound played
        - 'bip'   - a short beep
        - 'bup'   - a short beep, two octaves lower than bip
        - 'beep'  - a longer beep
        - **'micro'** - microwave stile beep-beep-beep
        - 'tune'  - a melody ('Kicsi kutya tarka')
        - anyting else => silent
    - **skipPercent** -- the pecentage that are displayed. Takes priority over time estimate
        - **1**   -> display every percentage
        - 10  -> display 10%,20%...
 
 ## Documentation  
 Standard python documentation has been included for the class and functions  
To check the details about the parameters use  
```
#Check class parameters
print(ProgressBar.__doc__)

#Check the parameters of a function
print(ProgressBar.checkProgress.__doc__)
```
 
 
 *subpercentages coming soon*
