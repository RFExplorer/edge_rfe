#!/usr/bin/env python

import serial, os, spidev, nmea, logging
from time import strftime, gmtime

#First things first - set up the program health logger
logging.basicConfig(filename='/home/pi/PythonProjects/RFEv2.0/rfelog.log', level=logging.DEBUG)
logging.info('\nSTART PROGRAM')

#Define the serial ports for the two devices
logging.info('SERIAL: Setting up the ports.')
rfe = serial.Serial('/dev/ttyUSB0', 2400, timeout=5)
gps = serial.Serial('/dev/ttyUSB1', 9600, timeout=5)
logging.info('SERIAL: Success')

#Create a unique log filename (no overwriting!)
LogFile = '/home/pi/PythonProjects/RFEv2.0/log/RfeLog_{}.log'.format(len(os.listdir('/home/pi/PythonProjects/RFEv2.0/log/')))

# Turn off the screen - an excellent indication that we're talking successfully, and an important power saver 
logging.info('RFE: Turning off the LCD')
rfe.write('#' + chr(0x04) + 'L0xxxxxxxxxxxxxxxx') #It's a hack, but the trailing characters ensure that the data actually gets written to the port; the RFE doesn't care - it expects fixed-width commands
# Request data dump
logging.info('RFE: Requesting data dump')
rfe.write('#' + chr(0x04) + 'C0xxxxxxxxxxxxxxxx')

#Initialize SPI communication to talk to the ADC on the Key Lime board
logging.info('SPIDEV: Setting up spidev')
spi = spidev.SpiDev()
spi.open(0,0)
pressureSensor = (0, 1, 2) #Ch0: Gnd, Ch1: V_pressure, Ch3: +5V

#Make the data log file that we'll be using today and write the csv header
def createLog():
	logging.info('LOG: Creating log {}'.format(LogFile))
	log = open(LogFile, 'w')
	log.write('YYYYMMDD,HHMMSS,latitude,lat_dir,longitude,lon_dir,altitude,num_sats,PressureGnd,PressureSense,Pressure3v3,-*-,data_dump\n')

#Write the data collected to the logfile in csv format
def updateLog(gps, rfe, pressure):
	logging.info('LOG: Updating log')
	log = open(LogFile, 'a')
	date = strftime("%Y%m%d", gmtime())
	time = strftime("%H%M%S", gmtime())

	log.write('{},{},'.format(date, time))
	log.write('{latitude},{lat_dir},{longitude},{lon_dir},{altitude},{num_sats},'.format(**gps))
	log.write('{0},{1},{2},-*-,'.format(*pressure))
	for r in range(len(rfe)):
		if (r < len(rfe) - 1):
			log.write(str(rfe[r]) + ',')
		else:
			log.write(str(rfe[r]) + '\n')
			
	log.close()

#Find the sentence that we care about (GGA), get it parsed, and get the relevant stuff  back to the caller
def readGps():
	logging.info('GPS: Trying to find GPGGA string')
	line = gps.readline()
	while ('GPGGA' not in line):
		line = gps.readline()

	if (line[0] == '$'):
		logging.info('GPS: Found GPGGA string, attempting to parse')
		gpgga = nmea.GPGGA()
		gpgga.feed(line)
		logging.info('GPS: The parse succeeded.')
	
		return {
			'latitude' : gpgga.lat,
			'lat_dir' : gpgga.lat_dir,
			'longitude' : gpgga.lon,
			'lon_dir' : gpgga.lon_dir,
			'altitude' : gpgga.altitude,
			'num_sats' : gpgga.num_sats
		}
	else:
		return readGps()

#The raw SPI binary commands to talk to the ADC
def readADC(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    r = spi.xfer2([1,(8+adcnum)<<4,0])
    adcout = ((r[1]&3) << 8) + r[2]
    return adcout

#Wrapper function to get just the three ADC channels we care about
def readPressure():
	logging.info('PRESSURE: Reading the pressure sensor')
	return (readADC(pressureSensor[0]), readADC(pressureSensor[1]), readADC(pressureSensor[2]))

def main():
	createLog()

	try:
		while (1):
			try:
				#The RFE returns data more slowly than any of the other sources, so we'll wait for data to come in, then get the rest of what we need for each line
				line = rfe.readline()
				dbm = []
				if (line[0] == '#'):
					logging.info('RFE: Found info header.')
					log = open(LogFile, 'a')
					log.write(line.replace(':',',') + '\n')
					log.close()
				elif (line[0] == '$'):
					logging.info('RFE: Found data line.')
					for i in line[3:]:
						d = ord(i) / -2
						dbm.append(d)
					updateLog(readGps(), dbm, readPressure())
					del dbm
				del line
			#Exception handling
			except KeyboardInterrupt:
				logging.info('Received KeyboardInterrupt, terminating')
				rfe.close()
				gps.close()
				break
			except Exception as e:
				logging.warning('Received exception: {}\n\tMoving to recover.'.format(e))
				pass

	except Exception as e:
		logging.warning('Received exception: {}\n\tCannot recover.'.format(e))
		rfe.close()
		gps.close()


if __name__ == '__main__':
	main()
