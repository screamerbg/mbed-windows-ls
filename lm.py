import serial.tools.list_ports as lp
import win32api

mbed_com_ports = []
for p in lp.comports():
    name, data, more = p
    if data.lower().find("mbed serial port") != -1:
        mbed_com_ports.append(name)

# ST...
mbed_com_ports_st = []
for p in lp.comports():
    name, data, more = p
    if data.lower().find("stlink") != -1:
        mbed_com_ports_st.append(name)

mbed_drives = []
for d in xrange(ord('A'), ord('U')):
    try:
        info = win32api.GetVolumeInformation(chr(d) + ":\\")
    except:
        continue
    if info[0].lower().find("mbed") != -1:
        mbed_drives.append(chr(d) + ":")

# ST...
mbed_drives_st = []
for d in xrange(ord('A'), ord('U')):
    try:
        info = win32api.GetVolumeInformation(chr(d) + ":\\")
    except:
        continue
    if info[0].lower().find("nucleo") != -1:
        mbed_drives_st.append(chr(d) + ":")

if mbed_com_ports:
    print "Serial ports:", ", ".join(mbed_com_ports)

if mbed_drives:
    print "      Drives:", ", ".join(mbed_drives)

if mbed_com_ports_st:
    print "ST Serial ports:", ", ".join(mbed_com_ports_st)

if mbed_drives_st:
    print "      ST Drives:", ", ".join(mbed_drives_st)
