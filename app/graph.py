# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from comtrade import Comtrade

#C:\\data\\04APR163.cfg", "C:\\data\\04APR163.dat
def GetGraphs(way):
    rec = Comtrade()
    rec.load(way + ".cfg", way + ".dat")
    _return = {"name": rec.analog_channel_ids[0], "time" : rec.time, "data" :  rec.analog[0]}
    return _return
