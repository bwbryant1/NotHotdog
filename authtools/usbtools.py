import pyudev

def monitor():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            print('{} connected'.format(device))
            # do something very interesting here.
def open():
    pass
def close():
    pass
def findUSB():
    pass

class USB(object):
    def __init__(self):
        self.vendor_id = ""
