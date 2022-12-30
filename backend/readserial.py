
# Grabs raw data from the Pico's UART and plots it as received

# Install dependencies:
# python3 -m pip install pyserial matplotlib

# Usage: python3 plotter <port>
# eg. python3 plotter /dev/ttyACM0

# see matplotlib animation API for more: https://matplotlib.org/stable/api/animation_api.html

import serial
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

PORT = '/dev/tty.usbserial-021FEFB2'
BAUD_RATE = 9600

# disable toolbar
plt.rcParams['toolbar'] = 'None'

class Plotter:
    def __init__(self, ax):
        self.ax = ax
        self.maxt = 250
        self.tdata = range(self.maxt)
        self.ydata = [0]*self.maxt
        self.alldata = []
        self.line = Line2D(self.tdata, self.ydata)

        self.ax.add_line(self.line)
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        # lastt = self.tdata[-1]
        # if lastt - self.tdata[0] >= self.maxt:  # drop old frames
        #     self.tdata = self.tdata[1:]
        #     self.ydata = self.ydata[1:]
        #     self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
        
        self.ydata[:-1] = self.ydata[1:]
        self.ydata[-1] = y
        self.alldata.append(y)

        
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def serial_getter():
    # grab fresh ADC values
    # note sometimes UART drops chars so we try a max of 5 times
    # to get proper data
    # while True:
        # for i in range(1):
        line = ser.readline()
        # try:
        splits = line.decode('utf-8').replace('\r\n','').split(',')
        
        s = float(splits[0]) if len(splits) >=1 else 0
        line = s
            # print(line)
        # except ValueError:
        #     '34'
        print(line)
        yield line


ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

fig, ax = plt.subplots()
plotter = Plotter(ax)

ani = animation.FuncAnimation(fig, plotter.update, serial_getter, interval=1,
                              blit=True, cache_frame_data=False)

ax.set_xlabel("Samples")
ax.set_ylabel("Voltage (V)")
fig.canvas.manager.set_window_title('Microphone ADC example')
fig.tight_layout()
plt.show()