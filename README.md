# vagrant-py
Python daemon to programatically control vagrant. 

### How to start
Start with `python main.py start` - this will start the daemon. Similarly you can close the daemon using `python main.py stop` or restart using `python main.py restart`

The daemon listens to a named pipe at: `<current dir>/tmp/pipe` by default and accepts certain command. Command looks like:

 - <random str> create <xml file path>
 - <random str> delete <box id>
 - <random str> start <box id>
 - <random str> destroy <challenge id>
 - <random str> info boxes
 - <random str> info box <box id>

The daemon responds back via named pipe situated at `<current dir>/tmp/<random str>` in `json` format.

### How to contribute
Just fork and pull!
