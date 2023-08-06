# clogger

Python logger configuration, my way.

clogger is a library that helps you to configure
python logging library in the way I like. It
helps configuration tasks such:

- multiple handlers
- log level setting


clogger contains two classes -
CustomLogger and CustomFormatter -
based on default logging library.

CustomFormatter inherit and modify
logging.Formatter class in order to split
handler names at the last '.', to improve readability
of the log.

CustomoLogger class can be used to initialize
and configure logging
library in a smart and easily replicable way.
It also enable a (small) set of preconfigured
actions.

## Installation

Install clogger is as easy as run ```pip install clogger```.

## Usage

You can configure log inside your script with
few code rows. 

```python
from clogger import CustomLogger
from datetime import datetime

now = datetime.now().strftime('%Y%m%d')
thisrunlog = 'thisrunlog_{}.log'.format(now)

logger = CustomLogger(
    handler_name="mylog",
    stream_handler=True,
    file_handler=True,
    filenames=["default.log", thisrunlog],
    level="INFO",
)
```

In the above example three handlers
are defined: one stream handler and two file
handlers. After definition, the same logger
can be modified, to hack log level of all
handlers (of course, the handler must exists
in the namespace to be varied):

```python
# changing log level for all the handlers
logger.change_level('DEBUG')

# changine level for some handlers
logger.change_level('DEBUG', ["mylog", "requests"])
```

Two methods are definied to be immediately call
at the start and at the end of a script:

```python
logger.starting_message()

#... a lot of code...

logger.exiting_message()
```