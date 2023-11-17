import pandas as pd
import pyvisa
from pymeasure.instruments.srs import SR830
from pymeasure.instruments.lakeshore import LakeShore331
import matplotlib.pyplot as plt
from datetime import datetime as dt
import time
import csv
from datetime import datetime


########################################################################################
def set_pid_parameters(instrument, p_value, i_value, d_value):
    instrument.write('PID 1,{:.1f},{:.1f},{:.1f}'.format(p_value, i_value, d_value))


def read_pid_parameters(instrument):
    instrument.write('PID?')
    response = instrument.read()
    p_value, i_value, d_value = map(float, response.strip().split(','))
    return p_value, i_value, d_value


def set_pid_parameters(instrument, p_value, i_value, d_value):
    instrument.write('PID 1,{:.1f},{:.1f},{:.1f}'.format(p_value, i_value, d_value))


def read_pid_parameters(instrument):
    instrument.write('PID?')
    response = instrument.read()
    p_value, i_value, d_value = map(float, response.strip().split(','))
    return p_value, i_value, d_value


def get_formatted_date_time():
    now = datetime.now()
    formatted_date_time = now.strftime("_%dth_%H-%M-%S")
    return formatted_date_time


########################################################################################
#in case of no tem readout
temperature_A = 0
############################
rm = pyvisa.ResourceManager()
print(rm.list_resources())
fluke8846a = rm.open_resource('GPIB0::1::INSTR')
keithley = rm.open_resource('GPIB0::16::INSTR')
ls335 = LakeShore331('GPIB::12::INSTR')
# Set the PID parameters, ramp - PID 200 100 10, stabilization - PID 125 12 2 (last on ramp 100 20 10) | 100 20 2
p_value = 125
i_value = 12
d_value = 2
set_pid_parameters(ls335, p_value, i_value, d_value)
print('PID parameters set successfully.')

# Read and display the PID parameters
p_read, i_read, d_read = read_pid_parameters(ls335)
print('PID parameters read from the instrument:')
print('P:', p_read)
print('I:', i_read)
print('D:', d_read)

# Set up the second channel, if needed


# Rest of the code...
print(ls335.ask('*IDN?'))
ls335.write('RAMP 2 1 2')
#ls335.setpoint_1 = input("Please input PID controller target temperature in Kelvin.")
ls335.setpoint_1 = 273
ls335.heater_range = 'high'

############################################


print(fluke8846a)
print(fluke8846a.query('*IDN?'))
print(fluke8846a.query(':MEAS:VOLT:DC?'))  # error niby ale jest query i dziala.

print(keithley)
print(keithley.query('*IDN?'))

print(keithley.query(':MEAS:CURR:DC?'))  # error niby ale jest query i dziala.

print(ls335)
#print(ls335.query('*IDN?'))

####get test type

test_type = input("[r]esistance discharge, resistance [c]harge or [v]oltage? \n press r/c/v")
if (test_type == "r"):
    test_type = test_type + input("what value?")
else:
    test_type = '_'

# init csv file, time and column headers

print('data to cvs save start!')

with open('output\\' + test_type + '@' + str(ls335.setpoint_1) +'K@' + get_formatted_date_time() + '.csv', 'w') as f:
    print("File at:\n"+ __file__+'output\\' + test_type + get_formatted_date_time() + '.csv')
    f_writer = csv.writer(f)
    data_line = []
    data_line.append('time [s]')
    data_line.append('voltage [V]')
    data_line.append('current [...]')
    data_line.append('temperature_A [K]')
    data_line.append('setpoint [K]')
    f_writer.writerow(data_line)
    print(data_line)
    start_time = time.time()

    ####
    while True:
        temperature_A = ls335.temperature_A
        data_line.clear()
        data_line.append(time.time() - start_time)
        data_line.append(float(fluke8846a.query(':MEAS:VOLT:DC?')))
        kdata = keithley.query(':MEAS:CURR:DC?')
        data_line.append((kdata[0:kdata.index(',')]))
        data_line.append(temperature_A)
        data_line.append(ls335.setpoint_1)
        f_writer.writerow(data_line)
        print(data_line)
        if (time.time() - start_time > 10):
            break

    f.close()
    #################
