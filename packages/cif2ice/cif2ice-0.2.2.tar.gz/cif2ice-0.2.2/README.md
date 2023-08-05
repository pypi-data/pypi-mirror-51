# cif2ice
A small utility to prepare a new ice structure for [GenIce](https://github.com/vitroid/GenIce) from a CIF file.

The source can be

1. A `.cif` file.
2. An URL to a `.cif` file.
3. The three-letter code of Zeolites.

## Installation

    pip install cif2ice

## Usage

    usage: cif2ice.x [-h] [--rep REP REP REP] [--debug] [--quiet] [--force] name
    
    positional arguments:
      name                  CIF file, Zeolite 3-letter code, or URL
    
    optional arguments:
      -h, --help            show this help message and exit
      --rep REP REP REP, -r REP REP REP
                            Repeat the unit cell in x,y, and z directions. [1,1,1]
      --debug, -D           Output debugging info.
      --quiet, -q           Do not output progress messages.
      --force, -f           Force overwrite.


## Example

1. To obtain a Zeolite RHO structure from the Zeolite DB

        cif2ice MTN

2. To generate a python module from the `foo.cif` file:

        cif2ice ./MTN.cif
        
3. To make the python module from a remote `.cif` file:

        cif2ice http://somewhere/MTN.cif

To use the module with GenIce, make a folder named `lattices/` in the current working directory and put `MTN.py` there.

    genice MTN > MTN.gro


   
