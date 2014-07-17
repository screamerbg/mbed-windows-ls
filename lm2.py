import serial.tools.list_ports as lp
import win32api
from prettytable import PrettyTable

cols = ["Name", "Data", "More"]
pt = PrettyTable(cols)
for c in cols:
    pt.align[c] = 'l'

mbed_com_ports = []
for p in lp.comports():
    name, data, more = p
    pt.add_row([name, data, more])
print pt

cols = ["Volume Name", "Volume Serial Number", "Max Length of a file name", "Sys Flags", "FS Name"]
pt = PrettyTable(cols)
for c in cols:
    pt.align[c] = 'l'

for d in xrange(ord('A'), ord('Z')):
    try:
        info = win32api.GetVolumeInformation(chr(d) + ":\\")
    except:
        continue
    pt.add_row(info)

print pt