from ctypes import *

_sum = cdll.LoadLibrary('libdpfp.so.0')
_sum.dpfp_init()
dev = _sum.dpfp_open()
_sum.dpfp_simple_await_finger_on(dev)
_sum.dpfp_set_mode(dev,10)
_sum.dpfp_capture_fprint(dev, fp)
