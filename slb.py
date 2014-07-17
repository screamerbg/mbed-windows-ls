import sys
import optparse
from serial import Serial

def flush_serial(serial):
    """ Flushing serial in/out. """
    serial.flushInput()
    serial.flushOutput()

def safe_sendLongBreak(self, serial, timeout=0.6):
    """ Wraps serial.sendBreak() to avoid serial::serialposix.py exception on Linux
    Traceback (most recent call last):
      File "make.py", line 189, in <module>
        serial.sendBreak()
      File "/usr/lib/python2.7/dist-packages/serial/serialposix.py", line 511, in sendBreak
        termios.tcsendbreak(self.fd, int(duration/0.25))
    error: (32, 'Broken pipe')
    """
    result = True
    try:
        serial.sendBreak(timeout)
    except:
        # In linux a termios.error is raised in sendBreak and in setBreak.
        # The following setBreak() is needed to release the reset signal on the target mcu.
        try:
            serial.setBreak(False)
        except:
            result = False
    return result

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-f', '--flush',
                      dest='serial_flush',
                      metavar=True,
                      action="store_false",
                      help='Do not flush serial before reset')

    parser.add_option("-s", "--serial", dest="port",
                      default=None, help="The mbed serial port")

    (opts, args) = parser.parse_args()

    print "Sending break to " + opts.port + "..."

    try:
        serial = Serial(opts.port, timeout=1)
        baud = 9600
        serial.setBaudrate(baud)

        if opts.serial_flush:
            print "Flushing..."
            flush_serial(serial)

        safe_sendLongBreak(serial, 0.6)

        try:
            while True:
                test_output = serial.read(512)
                if test_output:
                    sys.stdout.write('%s' % test_output)
                flush_serial(serial)
                if "{{end}}" in test_output:
                    break
        except KeyboardInterrupt, _:
            print "CTRL+C break"
        serial.close()

    except Exception as e:
        print "Error: %s" % (e)

    print "Done"
