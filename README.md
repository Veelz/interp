## interpolation
Using:  
Import the modules  
```
from interp import *  
```
Create interpolator instance and call ``` fit ``` method  
```
spline = Spline().fit(knots, values, d0, dn)
```  
```knots``` - interpolation knots, ```list``` (or ```numpy.ndarray```)   
```values``` - known values, ```list``` (or ```numpy.ndarray```)   
```d0``` - derivative in ```knots[0]```  
```dn``` - derivative in ```knots[-1]```  
To obtain interpolation value call ```value```  
```
f = spline.value(x)
```  
```x``` is number between ```knots[0]``` and ```knots[-1]```  
## dependencies  
- > python3.5  
- > numpy1.15  
## GUI  
GUI.py requires:  
- matplotlib3.0.0  
- tkinter  
