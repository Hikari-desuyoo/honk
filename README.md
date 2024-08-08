# Honk

**H**eartrate **ON** noteboo**K**

Application to store Haylou Smart Watch 2's heartrate on a database. Will probably have some tools to analyze it later (mainly for sleep monitoring). This only exists thanks to [this reverse engineered docs](https://github.com/XorTroll/Haywatch).

### Setup

On the current directory, run:

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`$ pip install -r requirements.txt`

### Running the program

For **recording** the BPM to the database, run `$ python3 record.py` while on venv (`$ source venv/bin/activate`). To get the readings, you need to initiate any of the sports routines on the smartwatch, and leave it running.

### Requirements

Depends on [Bleak](https://github.com/hbldh/bleak) being able to run.
