#!/usr/bin/env python

class GPGGA():
    def __init__(self):
        self.timestamp = None
        self.lat = None
        self.lat_dir = None
        self.lon = None
        self.lon_dir = None
        self.fix_quality = None
        self.num_sats = None
        self.dilution = None
        self.altitude = None
        self.geo_sep = None

    def feed(self, nmeaString):
        nmeaString = nmeaString.split('*')[0].split(',')
        self.timestamp = nmeaString[1]
        self.lat = nmeaString[2]
        self.lat_dir = nmeaString[3]
        self.lon = nmeaString[4]
        self.lon_dir = nmeaString[5]
        self.fix_quality = nmeaString[6]
        self.num_sats = nmeaString[7]
        self.dilution = nmeaString[8]
        self.altitude = nmeaString[9]
        self.geo_sep = nmeaString[11]

class GPRMC():
    def __init__(self):
        self.timestamp = None
        self.data_validity = None
        self.lat = None
        self.lat_dir = None
        self.lon = None
        self.lon_dir = None
        self.spd_over_gnd = None
        self.true_course = None
        self.datestamp = None
        self.mag_variation = None
        self.mag_var_dir = None

    def feed(self, nmeaString):
        nmeaString = nmeaString.split('*')[0].split(',')
        self.timestamp = nmeaString[1]
        self.data_validity = nmeaString[2]
        self.lat = nmeaString[3]
        self.lat_dir = nmeaString[4]
        self.lon = nmeaString[5]
        self.lon_dir = nmeaString[6]
        self.speed = nmeaString[7] # knots
        self.true_course = nmeaString[8]
        self.datestamp = nmeaString[9]
        self.mag_variation = nmeaString[10]
        self.mag_var_dir = nmeaString[11]
