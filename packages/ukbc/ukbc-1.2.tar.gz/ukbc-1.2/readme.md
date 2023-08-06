# UKBCrunch


## Requirements

It is highly recommended to install the Anaconda python distribution which contains most dependencies (see https://www.anaconda.com/download/).


### Viewing documentation 

See: https://ukbcrunch.readthedocs.io


## Installation

##### Option 1 (easy)

1. Open a command line and enter: ```pip install ukbc ```


##### For latest version:

1. Clone repository
2. Enter ukbc folder (containing setup.py) and run command ```pip install . ```


### Basic usage

```
import ukbc
my_ukbc=ukbc.UKBcrunch(html_file='path/to/html/file', csv_file='path/to/csv/file')
Epilepsy=Filtering.select_by_multiple(ukbc,on_illness='epilepsy')
```


### To launch the GUI:

```
import ukbc
ukbc.GUI.start()
```

## Contributing

Feel free to contribute via pull requests


