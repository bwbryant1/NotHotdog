import pyudev
import os

##device specifics to look for
serial = "1108170000001068"
devPaths = ['/dev/sdb1','/dev/sdc1','/dev/sdd1','/dev/sde1','/dev/sda1']
MOUNTPATH = '/mnt/keycard'
##

def waitForPlug():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')

    for device in iter(monitor.poll, None):
        if device.action == 'add':
            #print('{} connected'.format(device))
            if device['ID_SERIAL_SHORT'] == serial and device['DEVNAME'] in devPaths:
                usb = USB(device,serial,device['DEVNAME'])
                return usb
    return None

class USB(object):
    def __init__(self,device,serial,devPath):
        self.device = device
        self.ID_SERIAL_SHORT = serial
        self.DEVNAME = devPath
        self.mounted = False

    def mount(self):
        try:
            os.system("mount {devname} {mountpath}".format(devname=self.DEVNAME,mountpath=MOUNTPATH))
            self.mounted = True
        except:
            pass
    def unmount(self):
        try:
            os.system("umount {devname}".format(devname=self.DEVNAME))
            self.mounted = False
        except:
            pass
    def open(self):
        pass
    def close(self):
        pass
    def listFiles(self):
        if self.mounted:
            return os.listdir(MOUNTPATH)
        else:
            return []
