# string-color   
   
string-color is just another python module for coloring strings in print statements.   
   
### Installation   
   
`$ pip install string-color`   
   
### CLI Usage     
   
`$ string-color`   
   
display a list of all 256 colors   
   
`$ string-color yellow`   
   
show color info for the color yellow   
   
`$ string-color "#ff0000"`   
   
show color info for the hex value #ff0000   
   
![Usage Screep Cap][screencap]  
  
[screencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/sc-screen-cap2.jpg  "Usage Screen Cap"  
  
### Python Module Usage   
   
```python   
from stringcolor import cs   
   
# a few examples without background colors.   
# for color names see CLI usage above.   
print(cs("here we go", "orchid"))   
print(cs("away to space!", "DeepPink3"))   
print(cs("final fantasy", "#ffff87"))   
   
# yellow text with a red background.   
# color names, hex values, and ansi numbers will work.   
print(cs("warning!", "yellow", "#ff0000"))   
```   
  
![Usage Screep Cap][screencap]

[screencap]: https://believe-it-or-not-im-walking-on-air.s3.amazonaws.com/sc-screen-cap.png "Usage Screen Cap"
