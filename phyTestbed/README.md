# Physical Testbed

This folder contains scripts to setup the hybrid testbed. 

`/configurations` contains the script for the MitM devices to activate/deactivate the attack,

`/indicators` contains a script to test LEDs connected to Raspberry PIs and a `start.py` file which require an argument 
(`<se|ev>`) and which starts a RiseV2G with a wrapper around taht controls the LEDs.

There is also an experimental `remote_control.py` script to control all the devices from the same laptop. 
It need the IPs in the `config.json` file.