from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError
from datetime import datetime
import random
from time import sleep
from config import logger, db_settings
from requests.exceptions import ConnectionError

# For development only
import sys, traceback

# Changes to these settings should be made in config.py!
client = InfluxDBClient(
    host=db_settings['host'],
    port=db_settings['port'],
    username=db_settings['username'],
    password=db_settings['password'],
    database=db_settings['database']
    )



class Point():
    def __init__(self, p_type, *args, **kwargs):
        if p_type == 'home_load':
            self.power   = kwargs['power']
            self.current = kwargs['current']
            self.p_type  = p_type
            self.time    = kwargs['time']
        
        elif p_type == 'solar':
            self.power   = kwargs['power']
            self.current = kwargs['current']
            self.pf      = kwargs['pf']
            self.p_type  = p_type    
            self.time    = kwargs['time']        
            
        elif p_type == 'net': 
            '''
            This type represents the current net power situation at the time of sampling. 
            self.power   : the real net power
            self.current : the rms current as measured
            self.p_type  : the type of point [home_load, solar, net, ct, voltage]
            self.time    : timestamp from when the data was sampled
            '''
            self.power   = kwargs['power']
            self.current = kwargs['current']
            self.p_type  = p_type            
            self.time    = kwargs['time']
        
        elif p_type == 'ct':
            '''
            This type represents a CT reading.
            self.power   : the real power as calculated in the calculate_power() function
            self.current : the rms current as measured
            self.p_type  : the type of point [home_load, solar, net, ct, voltage]
            self.ct_num  : the CT number [0-6]
            self.time    : timestamp from when the data was sampled
            '''
            self.power   = kwargs['power']
            self.current = kwargs['current']
            self.p_type  = p_type            
            self.pf      = kwargs['pf']
            self.ct_num  = kwargs['num']
            self.time    = kwargs['time']

        elif p_type == 'voltage':
            '''
            This type represents a voltage reading. 
            The self.voltage is self explanatory.
            The v_input represents the identifier of the voltage input. This is setting up for multiple voltage inputs in the future.
            '''
            self.voltage = kwargs['voltage']
            self.v_input = kwargs['v_input']
            self.time    = kwargs['time']
            self.p_type  = p_type
 

    def to_dict(self):
        if self.p_type == 'home_load':
            data = {
                "measurement": 'home_load',
                "fields" : {
                    "current" : self.current,
                    "power": self.power
                },
                "time" : self.time
            }
        elif self.p_type == 'solar': 
            data = {
                "measurement" : "solar",
                "fields" : {
                    "current" : self.current,
                    "power": self.power,
                    "pf": self.pf
                },
                "time" : self.time
            }
        elif self.p_type == 'net':
            if self.power < 0:
                status = 'Producing'
            elif self.power > 0:
                status = 'Consuming'
            else:
                status = "No data"
            data = {
                "measurement" : "net",
                "fields" : {
                    "current" : self.current,
                    "power" : self.power,
                },
                "tags" : {
                    "status" : status,
                },
                "time" : self.time
            }

        elif self.p_type == 'ct':
            data = {
                "measurement" : "raw_cts",
                "fields" : {
                    "current" : self.current,
                    "power" : self.power,
                    "pf" : self.pf,
                },
                "tags" : {
                    'ct' : self.ct_num
                },
                "time" : self.time
            }

        elif self.p_type == 'voltage':
            data = {
                "measurement" : "voltages",
                "fields" : {
                    "voltage" : self.voltage,
                },
                "tags" : {
                    'v_input' : self.v_input
                },
                "time" : self.time
            }
        return data



def init_db():
    try:
        client.create_database(db_settings['database'])
        logger.info("... DB initalized.")
        return True
    except ConnectionRefusedError:
        logger.debug("Could not connect to InfluxDB")
        return False
    
    except Exception:
        logger.debug(f"Could not connect to {db_settings['host']}:{db_settings['port']}")
        return False
        
        
    
    


def close_db():
    client.close()

def write_to_influx(solar_power_values, home_load_values, net_power_values, ct0_dict, ct1_dict, ct2_dict, ct3_dict, ct4_dict, ct5_dict, ct6_dict, ct7_dict, ct8_dict, ct9_dict, ct10_dict, ct11_dict, ct12_dict, ct13_dict, poll_time, length, voltages):
    
    # Calculate Averages
    avg_solar_power = sum(solar_power_values['power']) / length
    avg_solar_current = sum(solar_power_values['current']) / length
    avg_solar_pf = sum(solar_power_values['pf']) / length
    avg_home_power = sum(home_load_values['power']) / length
    avg_home_current = sum(home_load_values['current']) / length
    avg_net_power = sum(net_power_values['power']) / length
    avg_net_current = sum(net_power_values['current']) / length
    ct0_avg_power = sum(ct0_dict['power']) / length
    ct0_avg_current = sum(ct0_dict['current']) / length
    ct0_avg_pf = sum(ct0_dict['pf']) / length
    ct1_avg_power = sum(ct1_dict['power']) / length
    ct1_avg_current = sum(ct1_dict['current']) / length
    ct1_avg_pf = sum(ct1_dict['pf']) / length
    ct2_avg_power = sum(ct2_dict['power']) / length
    ct2_avg_current = sum(ct2_dict['current']) / length
    ct2_avg_pf = sum(ct2_dict['pf']) / length
    ct3_avg_power = sum(ct3_dict['power']) / length
    ct3_avg_current = sum(ct3_dict['current']) / length
    ct3_avg_pf = sum(ct3_dict['pf']) / length
    ct4_avg_power = sum(ct4_dict['power']) / length
    ct4_avg_current = sum(ct4_dict['current']) / length
    ct4_avg_pf = sum(ct4_dict['pf']) / length
    ct5_avg_power = sum(ct5_dict['power']) / length
    ct5_avg_current = sum(ct5_dict['current']) / length
    ct5_avg_pf = sum(ct5_dict['pf']) / length
    ct6_avg_power = sum(ct6_dict['power']) / length
    ct6_avg_current = sum(ct6_dict['current']) / length
    ct6_avg_pf = sum(ct6_dict['pf']) / length
    ct7_avg_power = sum(ct7_dict['power']) / length
    ct7_avg_current = sum(ct7_dict['current']) / length
    ct7_avg_pf = sum(ct7_dict['pf']) / length
    ct8_avg_power = sum(ct8_dict['power']) / length
    ct8_avg_current = sum(ct8_dict['current']) / length
    ct8_avg_pf = sum(ct8_dict['pf']) / length
    ct9_avg_power = sum(ct9_dict['power']) / length
    ct9_avg_current = sum(ct9_dict['current']) / length
    ct9_avg_pf = sum(ct9_dict['pf']) / length
    ct10_avg_power = sum(ct10_dict['power']) / length
    ct10_avg_current = sum(ct10_dict['current']) / length
    ct10_avg_pf = sum(ct10_dict['pf']) / length
    ct11_avg_power = sum(ct11_dict['power']) / length
    ct11_avg_current = sum(ct11_dict['current']) / length
    ct11_avg_pf = sum(ct11_dict['pf']) / length
    ct12_avg_power = sum(ct12_dict['power']) / length
    ct12_avg_current = sum(ct12_dict['current']) / length
    ct12_avg_pf = sum(ct12_dict['pf']) / length
    ct13_avg_power = sum(ct13_dict['power']) / length
    ct13_avg_current = sum(ct13_dict['current']) / length
    ct13_avg_pf = sum(ct13_dict['pf']) / length
    
    avg_voltage = sum(voltages) / length

    # Create Points
    home_load = Point('home_load', power=avg_home_power, current=avg_home_current, time=poll_time)
    solar = Point('solar', power=avg_solar_power, current=avg_solar_current, pf=avg_solar_pf, time=poll_time)
    net = Point('net', power=avg_net_power, current=avg_net_current, time=poll_time)
    ct0 = Point('ct', power=ct0_avg_power, current=ct0_avg_current, pf=ct0_avg_pf, time=poll_time, num=0)
    ct1 = Point('ct', power=ct1_avg_power, current=ct1_avg_current, pf=ct1_avg_pf, time=poll_time, num=1)
    ct2 = Point('ct', power=ct2_avg_power, current=ct2_avg_current, pf=ct2_avg_pf, time=poll_time, num=2)
    ct3 = Point('ct', power=ct3_avg_power, current=ct3_avg_current, pf=ct3_avg_pf, time=poll_time, num=3)
    ct4 = Point('ct', power=ct4_avg_power, current=ct4_avg_current, pf=ct4_avg_pf, time=poll_time, num=4)
    ct5 = Point('ct', power=ct5_avg_power, current=ct5_avg_current, pf=ct5_avg_pf, time=poll_time, num=5)
    ct6 = Point('ct', power=ct6_avg_power, current=ct6_avg_current, pf=ct6_avg_pf, time=poll_time, num=6)
    ct7 = Point('ct', power=ct7_avg_power, current=ct7_avg_current, pf=ct7_avg_pf, time=poll_time, num=7)
    ct8 = Point('ct', power=ct8_avg_power, current=ct8_avg_current, pf=ct8_avg_pf, time=poll_time, num=8)
    ct9 = Point('ct', power=ct9_avg_power, current=ct9_avg_current, pf=ct9_avg_pf, time=poll_time, num=9)
    ct10 = Point('ct', power=ct10_avg_power, current=ct10_avg_current, pf=ct10_avg_pf, time=poll_time, num=10)
    ct11 = Point('ct', power=ct11_avg_power, current=ct11_avg_current, pf=ct11_avg_pf, time=poll_time, num=11)
    ct12 = Point('ct', power=ct12_avg_power, current=ct12_avg_current, pf=ct12_avg_pf, time=poll_time, num=12)
    ct13 = Point('ct', power=ct13_avg_power, current=ct13_avg_current, pf=ct13_avg_pf, time=poll_time, num=13)

    v = Point('voltage', voltage=avg_voltage, v_input=0, time=poll_time)

    points = [
        home_load.to_dict(),
        solar.to_dict(),
        net.to_dict(),
        ct0.to_dict(),
        ct1.to_dict(),
        ct2.to_dict(),
        ct3.to_dict(),
        ct4.to_dict(),
        ct5.to_dict(),
        ct6.to_dict(),
        ct7.to_dict(),
        ct8.to_dict(),
        ct9.to_dict(),
        ct10.to_dict(),
        ct11.to_dict(),
        ct12.to_dict(),
        ct13.to_dict(),
        v.to_dict(),
    ]

    try:    
        client.write_points(points, time_precision='ms')
    except InfluxDBServerError as e:
        logger.critical(f"Failed to write data to Influx. Reason: {e}")
    except ConnectionError:
        logger.info("Connection to InfluxDB lost. Please investigate!")
        sys.exit()


if __name__ == '__main__':
    client = InfluxDBClient(host='localhost', port=8086, username='root', password='password', database='example')
    test_insert_and_retrieve(client)
