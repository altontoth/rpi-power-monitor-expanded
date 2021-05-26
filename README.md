# Raspberry Pi Power Monitor (Expanded Version)

The Raspberry Pi Power Monitor is a combination of custom hardware and software that will allow you to monitor your unique power situation in real time (<0.5 second intervals), including accurate consumption, generation, and net-production. The data are stored to a database and displayed in a Grafana dashboard for monitoring and reporting purposes.

This project has been expanded from the original project published by David00, with the intention of adding a second MCP3008 chip to the board to read an additional 8 channels using the second SPI port on the Raspberry Pi. This would not have been possible without David's work, and advice.

This project is derived from and inspired by the resources located at https://learn.openenergymonitor.org as well as https://github.com/David00/rpi-power-monitor/

---

## What does it do?

This code accompanies DIY circuitry that supports monitoring of up to 14 current transformers and one AC voltage reading. The individual readings are then used in calculations to provide real data on consumption and generation, including the following key metrics:

* Total home consumption
* Total solar PV generation
* Net home consumption
* Net home generation
* Total current, voltage, power, and power factor values
* Individual current transformer readings
* Harmonics inspection through a built in snapshot/plotting mechanism.

The code takes tens of thousands of samples per second, corrects for phase errors in the measurements, calculates the instantaneous power for the tens of thousands of sampled points, and uses the instantaneous power calculations to determine real power, apparent power, and power factor. This means the project is able to monitor any type of load, including reactive, capacitive, and resisitve loads.

---

## Installation

Follow David00's original instructions for setup of the expanded board (for now) revised hardware will be forthcoming.

### Please see the [project Wiki](https://github.com/David00/rpi-power-monitor/wiki#quick-start--table-of-contents) for detailed setup instructions.


---

## Contributing

Would you like to help out? Shoot an email at github@dalbrecht.tech to see what items he currently has pending on the main branch. This was developed for expanded reading of a larger panel.

---

### Credits

* [David00's Power Monitor](https://github.com/David00/rpi-power-monitor/) David is the original creator of this project.
* 
* [OpenEnergyMonitor](https://openenergymonitor.org) and forum member Robert.Wall for guidance and support

* The `spidev` project on PyPi for providing the interface to read an analog to digital converter


---


### Like my project? Donations are welcome!

BTC:  

###### Last Updated:  May 25, 2021
