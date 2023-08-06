# Install

``` bash

pip install sal-timer

```


# Quick start

``` python
from sal_timer import timer




@timer
def func():
    pass
 

func()

'''
*******************************************************
Finished 'func' in 0.0000 secs.
*******************************************************
'''


```