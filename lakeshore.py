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
while True:
    print(ls335.input_A.temperature)

