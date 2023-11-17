import time
from pymeasure.instruments.lakeshore import LakeShore331
from datetime import datetime as dt

def set_pid_parameters(instrument, p_value, i_value, d_value):
    instrument.write('PID 1,{:.1f},{:.1f},{:.1f}'.format(p_value, i_value, d_value))

def read_pid_parameters(instrument):
    instrument.write('PID?')
    response = instrument.read()
    p_value, i_value, d_value = map(float, response.strip().split(','))
    return p_value, i_value, d_value

# Create an instance of the instrument
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
# ls335.channel = 2

# Rest of the code...
print(ls335.ask('*IDN?'))
# ls335.write('RAMP 2 1 2')
ls335.setpoint_1 = 294
# ls335.heater_range = 'off'

while True:
    time.sleep(1)
    temperature_A = ls335.temperature_A
    temperature_B = ls335.temperature_B
    print('Temperature A:', temperature_A)
    print('Temperature B:', temperature_B)
    print(str(dt.now()))
