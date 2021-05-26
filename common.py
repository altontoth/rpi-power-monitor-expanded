# This module contains functions that are used in both the main power-monitor code and the calibration code.

from datetime import datetime
from config import ct_phase_correction, ct0_channel, ct1_channel, ct2_channel, ct3_channel, ct4_channel, board_voltage_channel, v_sensor_channel, ct5_channel, logger
import spidev
import subprocess
import docker
import sys
from time import sleep
from textwrap import dedent

#Create SPI on Chip 1
spi_ce0 = spidev.SpiDev()
spi_ce0.open(0, 0)
spi_ce0.max_speed_hz = 1750000          # Changing this value will require you to adjust the phasecal values above.

#Create SPI on Chip 2
spi_ce1 = spidev.SpiDev()
spi_ce1.open(0, 1)
spi_ce1.max_speed_hz = 1750000          # Changing this value will require you to adjust the phasecal values above.

def readadc_ce0(adcnum):
    # read SPI data from the first MCP3008, 8 channels in total
    r = spi_ce0.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def readadc_ce1(adcnum):
    # read SPI data from the second MCP3008, 8 channels in total
    r = spi_ce1.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def collect_data(numSamples):
    # Get time of reading
    now = datetime.utcnow()
    
    samples = []
    ct0_data = []
    ct1_data = []
    ct2_data = []
    ct3_data = []
    ct4_data = []
    ct5_data = []
    v_data = []
    
    ct8_data = []
    ct9_data = []
    ct10_data = []
    ct11_data = []
    ct12_data = []
    ct13_data = []
    ct14_data = []
    ct15_data = []

    for _ in range(numSamples):
        ct0 = readadc_ce0(ct0_channel)
        ct4 = readadc_ce0(ct4_channel)
        ct1 = readadc_ce0(ct1_channel)
        v = readadc_ce0(v_sensor_channel)
        ct2 = readadc_ce0(ct2_channel)
        ct3 = readadc_ce0(ct3_channel)
        ct5 = readadc_ce0(ct5_channel)
        
        ct8 = readadc_ce1(ct8_channel)
        ct9 = readadc_ce1(ct9_channel)
        ct10 = readadc_ce1(ct10_channel)
        ct11 = readadc_ce1(ct11_channel)
        ct12 = readadc_ce1(ct12_channel)
        ct13 = readadc_ce1(ct13_channel)
        ct14 = readadc_ce1(ct14_channel)
        ct15 = readadc_ce1(ct15_channel)
        
        ct0_data.append(ct0)
        ct1_data.append(ct1)
        ct2_data.append(ct2)
        ct3_data.append(ct3)
        ct4_data.append(ct4)
        ct5_data.append(ct5)
        
        ct8_data.append(ct8)
        ct9_data.append(ct9)
        ct10_data.append(ct10)
        ct11_data.append(ct11)
        ct12_data.append(ct12)
        ct13_data.append(ct13)
        ct14_data.append(ct14)
        ct15_data.append(ct15)
        
        v_data.append(v)    
    
    samples = {
        'ct0' : ct0_data,
        'ct1' : ct1_data,
        'ct2' : ct2_data,
        'ct3' : ct3_data,
        'ct4' : ct4_data,
        'ct5' : ct5_data,
        'ct8' : ct8_data,
        'ct9' : ct9_data,
        'ct10' : ct10_data,
        'ct11' : ct11_data,
        'ct12' : ct12_data,
        'ct13' : ct13_data,
        'ct14' : ct14_data,
        'ct15' : ct15_data,
        'voltage' : v_data,
        'time' : now,
    }
    return samples

def recover_influx_container():
    docker_client = docker.from_env()

    # Check to see if the influxdb container exists:
    containers = docker_client.containers.list(all=True)
    for container in containers:
        image = container.attrs['Config']['Image']

        if 'influx' in image.lower():
            name = container.attrs['Name'].replace('/','')
            status = container.attrs['State']['Status']

            if status.lower() != 'running':
                # Ask the user to restart the container
                answers = ['yes', 'no', 'y', 'n']
                logger.info(f"... It appears that your {name} container is not running. ")

                logger.info(f"... restarting your {name} container. Please wait... ")
                container.restart()

                sleep(5)
                logger.info("... checking to see if the container is running now...")
                sleep(0.5)
                for _ in range(0,2):
                    # Make two attempts to see if the container is running now.
                    try:
                        influx_container = docker_client.containers.list( filters={'name' : name} )[0]
                        container_found = True
                    except IndexError:
                        sleep(0.5)
                        continue
                if not container_found:
                    logger.info("Couldn't find the container by name! Please open a Github issue as this is an unexpected result from this experimental implementation.")
                    sys.exit()

                if influx_container.attrs['State']['Status'] != 'running':
                    # Something must be wrong with the container - check for the exit code and grab the last few lines of logs to present to the user for further troubleshooting.
                    exit_code = influx_container.attrs['State']['ExitCode']
                    logs = influx_container.logs(tail=20)

                    logger.info(dedent(f"""Sorry, I couldn't fix your InfluxDB container. Here's some information that may help you: 
                    Container Exit Code: {exit_code}
                    Logs:"""
                    ))
                    for line in logs.splitlines():
                        logger.info(f"   {line}")
                    
                    sys.exit()

                else:
                    logger.info("... container successfully started!")
                    return True
