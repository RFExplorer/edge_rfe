Proof of Concept for EDGE Research Lab, it is not 100% repeatably deployable as this stands.

## Intro

The EDGE Spectral Awareness Payload (SAP) is a small, lightweight, RF power spectrum recorder specifically designed for high-altitude balloon deployment.  Focusing on COTS hardware, this effort is intended to demonstrate the feasibility of the sensing portion of the payload-able whitespace radio concept (a dynamic radio determining useable bandwidth).

## Scope

The SAP is a record-only, analyze-on-recovery, high-power requirement (>5W) payload.

## BOM

* 1xRaspberryPi (originally the model B)
* 1xRFExplorer WSUB3G/3G
* 1xNwazet Key Lime Pi interface module, incl. MCP3008 ADC
* 2xFTDI TTL232R Cable
* 1xSFE Venus GPS Module
* 1xSFE Embedded GPS Antenna
* 1xHoneywell ASDX 0-15psi absolute pressure guage
* 2xDimension Engineering 5V / 1A (5W) switching regulator
* 1xPower-injected USB A – MiniUSB cable
* 1xUSB A – MiniUSB cable
* 1xWideband dipole antenna
* 1x36WH (minimum) LiPo battery

## Power Connections

Battery

* 5v Reg 1
    * USB Hub Port 0: RasPi, GPS FTDI, Key Line Intf., GPS Module
* 5v Reg2
    * Power Injected USB: RF Explorer

## Data Connections

RasPi

* USB Hub Mux Port
    * Port1: RF Explorer (`/dev/ttyUSB0`)
    * Port2: GPS FTDI (`/dev/ttyUSB1`) -> GPS Module
* GPIO Header
    * Key Line Iintf: FTDI Terminal, ADC -> Pressure Sensor

## Software

Requirements:

* pyserial
* spidev

* RFE.py
    * Main executable
* nmea.py
    * GPS Sentence definitions
* StartRFE.sh
    * Auto-Restart script, set up as a cron job `@reboot` and repeated every `30` seconds.

## Common Issues

* The RFE is not consistent with responding to the API, some commands require additional tries (such as shutdown, if it works at all - this is an issue with the RFE).
    * You will not see the screen shut off on initialization (a simple sign)
* The ports enumerated incorrectly, you may need to adjust RFE.py to look for different `/dev/tty*` devices.
