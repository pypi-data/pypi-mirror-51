# infinitythread
The thread that never rests.

Feature Support
---------------
With `InfinityThread` you can
- Run function **Periodically** inside a thread.
- Keep running and **Ignore** function error.
- **Stop** the thread.
- Execute **Cleanup Function** when thread is stopped.

Usage
---------------
Basic Usage
``` {.sourceCode .python}
from infinitythread import InfinityThread
my_thread = InfinityThread(target=my_func, interval=2)
my_thread.start()
# Run `my_func` every 2 seconds.
```
Advance Usage
``` {.sourceCode .python}
from infinitythread import InfinityThread
def my_func():
    print("I am running in intervals")
    raise Exception("Non affective exception")
def cleanup_function():
    print("Cleaning Up..")
my_thread = InfinityThread(target=my_func, interval=2,on_stop_func=cleanup_function,ignore_errors=True)
my_thread.start()
#  the thread keeps running like a clock even when the target function has errors.
my_thread.stop()
# When the thread stops the `cleanup_function` will be called.
```

Installation
-------

``` {.sourceCode .bash}
$ pip install infinitythread