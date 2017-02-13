# unifi4homematic
Simple script for presence detection for the Homematic CCU2 using an Ubiquiti UniFi controller.

Supports multiple presence variables for different persons.

## Requirements
Python 3.x, a Homematic CCU2 and Ubiquiti UniFi Controller, Version 5.x.

## Installation and configuration
To install just download or clone the unifi-presence.py file.

Open the file in your preferred editor and change the settings between ```START CONFIG``` and ```END CONFIG``` to your needs.

## Usage

Run the file using cron, e.g.:

```*/5 * * * *  user  /path/to/unifi-presence.py```
