# Tree Guardian

Track the changes into the filesystem and trigger callback on changes 
 detecting.


## Getting Started

### Installation

```bash
pip install tree-guardian
```

### Usage

Observe the changes into your project.

```python
from tree_guardian import observe

# Target function to trigger
def cb():
    from time import time

    print('[{}] Changes detected...'.format(time()))

observe(cb)  # Run observer
```

Run in background.

```python
from time import sleep
from threading import Event
from tree_guardian import observe


# Target function to trigger
def cb():
    from time import time

    print('[{}] Changes detected...'.format(time()))


event = Event()
observe(cb, run_async=True, event=event)  # Run observer

# Type your code below...

try:
    sleep(10)  # Run for 10 seconds or until interrupted
except KeyboardInterrupt:
    event.set()
```
