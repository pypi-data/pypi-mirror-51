# Timemap

> repository under renovation

A python package to deal with location history files, such
as GMAPS takeout json.

The main motivation behind this package is to allow simple analytics
based on where you have been, for example, how long did you spend
at the office over January?


Supported providers:
* Google - takeout's json


## Settings

You can customize the runtime parameters through a configuration file
or command line parameters (requires extension).


# Configuration File
The configuration consist of a yaml file. All the items in it, will be
exposed as settings to your script.


``` yaml
filepath: ./.history.json
start: 2019-03-01
end: 2019-03-31

radius: 200 # in meters
latitude: 44.434 # in decimal format
longitude: 22.213 # in decimal format
```


# Contributing
Feel free to send me your pull requests


