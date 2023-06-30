# input-with-timeout
The same as standard Python input() but with a timeout!
Optimised (I think), written in pure Python though...
The inaccuracy of time elapsed before timeout increases with the decrease in the polling rate, I might try to minimise this later.

Example:
```python
from input_with_timeout import input_with_timout

#4.2 seconds timeout
number = input_with_timout(4.2, "Enter a number: ")

#None is returned if timeout
if number == None:
    print("You didn't enter a number in time!")
else:
    print("You entered: " + number) 
```
