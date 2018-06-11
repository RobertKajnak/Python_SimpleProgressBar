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
 
 ## If you want to customize the output
 The default configuration:  
 print the percentage at most every 2 seconds  
 print the time estimation at most every 10 seconds  

The description of the parameters can be found in the file, before the \_\_init\_\_ function  
 
 
 **subpercentages coming soon  **
