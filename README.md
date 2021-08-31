# COERbuoy1 benchmark
A realistic benchmark for Wave Enegery Converter controllers

The commands how to run python might differ between systems, and the ones presented here might not work on every machine. Please refer to https://www.python.org/downloads/ to find the correct commands for your system.

# Installation
Download python3: https://www.python.org/downloads/

Install COERbuoy using pip:

Windows: py -m pip install https://github.com/SiHeTh/COERbuoy/raw/main/dist/COERbuoy-0.1.2-py3-none-any.whl 

Linux/MacOS: pip install https://github.com/SiHeTh/COERbuoy/raw/main/dist/COERbuoy-0.1.2-py3-none-any.whl

# Run COERbuoy1 (terminal)
## Bretschneider sea state:

With significant wave height 1.5 m and wave energy period of 6 s and a linear generator damping:

Windows: py -m COERbuoy --bretschneider_wave 1.5 6 results.csv linear

Linux/MacOS: python3 -m COERbuoy --bretschneider_wave 1.5 6 results.csv linear


## Regular wave:

With wave height 1.5 m and wave period of 6 s and a linear generator damping:

Windows: py -m COERbuoy --regular_wave 1.5 6 results.csv linear

Linux/MacOS: python3 -m COERbuoy --regular_wave 1.5 6 results.csv linear

# Run COERbuoy1 GUI

Windows: py -m COERbuoy.GUIServer

Linux/MacOS: python3 -m COERbuoy.GUIServer

.. then open http://localhost:8080 in a web browser.


#Funding
This research was part-funded byScience Foundation Ireland (SFI) through MaREI, the SFI Research Centre for Energy, Climate, and Marine [Grant No: 12/RC/2302 P2], with supporting funding obtained from CorPower Ocean AB.
