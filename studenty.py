import pandas as pd
import pyvisa
from pymeasure.instruments.srs import SR830
from pymeasure.instruments.lakeshore import LakeShore331
import matplotlib.pyplot as plt
from datetime import datetime as dt
from time import sleep
#################
rm = pyvisa.ResourceManager()
print(rm.list_resources())
#################
# Create a function to write the header to the file
def write_header(filename):
    header = 'T_A[K] T_B[K] Setpoint[K] sr830x[V] sr830y[V] sr830f[Hz] sr830sin[V] CNT yyyy-mm-dd hh:mm:ss.ccccc\n'
    with open(filename, "a") as file:
        file.write(header)

# Create a function to append a line of data to the file
def append_data(filename, data, cnt):
    line_to_save = ' '.join(f'{value:.3f}' for value in data[:3])  # Save the first 3 values with 3 significant digits
    line_to_save += f' {data[3]:.9f}'  # Save sr860.x with 8 significant digits
    line_to_save += f' {data[4]:.9f}'  # Save sr860.y with 8 significant digits
    line_to_save += f' {data[5]:.4f}'  # Save sr860.frequency with 4 significant digits
    line_to_save += f' {data[6]:.8f}'  # Save sr860.sine_voltage with 8 significant digits
    line_to_save += f' {cnt}'  # Save the count as an integer
    line_to_save += f' {dt.now()}\n'
    with open(filename, "a") as file:
        file.write(line_to_save)
    print(line_to_save)  # Print the data line


# Write the header to the file
filename = './diameter_0.05mm_n_50_loops/run_509.70Hz_59.23deg_00.dat'
write_header(filename)

# Create instances of the instruments
sr830 = SR830('GPIB::8::INSTR')
ls335 = LakeShore331('GPIB::12::INSTR')

# Print instrument identification
print(sr830.id)
print(ls335.id)

# Input settings
sr830.phase = 59.23
sr830.frequency = 509.70
sr830.sine_voltage = 5.0

# select a sensitivity, from a list below
# 0 - 2 nV/fA   | 13 - 50 µV/pA
# 1 - 5 nV/fA   | 14 - 100 µV/pA
# 2 - 10 nV/fA  | 15 - 200 µV/pA
# 3 - 20 nV/fA  | 16 - 500 µV/pA
# 4 - 50 nV/fA  | 17 - 1 mV/nA
# 5 - 100 nV/fA | 18 - 2 mV/nA
# 6 - 200 nV/fA | 19 - 5 mV/nA
# 7 - 500 nV/fA | 20 - 10 mV/nA
# 8 - 1 µV/pA   | 21 - 20 mV/nA
# 9 - 2 µV/pA   | 22 - 50 mV/nA
# 10 - 5 µV/pA  | 23 - 100 mV/nA
# 11 - 10 µV/pA | 24 - 200 mV/nA
# 12 - 20 µV/pA | 25 - 500 mV/nA
#               | 26 - 1 V/µA
# sr830.write("SENS 23")

# Auto Offset 1 - X, 2 - Y, 3 - R
sr830.write("AOFF 1")
sr830.write("AOFF 2")

# Set up plotting
plt.ion()
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('AC susceptibility (V) vs. LakeShore 335 Temperature')

ax1.set_ylabel('chiprim (V)')

ax2.set_xlabel('Temperature (K)')
ax2.set_ylabel('chibis (V)')

# Initialize plot data
x_data, y_data, yy_data = [], [], []

while True:
    try:
        data = []
        for _ in range(6):
            data.append([
                ls335.temperature_A, ls335.temperature_B, ls335.setpoint_1,
                sr830.x, sr830.y, sr830.frequency, sr830.sine_voltage
            ])
            sleep(0.1)

        # Calculate the mean values of the data
        data = pd.DataFrame(data).mean().tolist()

        # Append the data to the file and print it
        append_data(filename, data, len(x_data) + 1)

        # Add the data to the plot
        x_data.append(data[0])
        y_data.append(data[3])
        yy_data.append(data[4])
        ax1.plot(x_data, y_data, 'b-')
        ax2.plot(x_data, yy_data, 'r-')
        plt.show()
        plt.pause(1)

        sleep(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sleep(1)
