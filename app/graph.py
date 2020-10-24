# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from comtrade import Comtrade, Cfg
from mpld3 import fig_to_html, plugins


# C:\\data\\04APR163.cfg", "C:\\data\\04APR163.dat
def GetGraphs(way, id, type):
    rec = Comtrade()
    rec.load(way + ".cfg", way + ".dat")
    if (type == "digital"):
        plotdata = rec.digital[id]
        plotname = rec.digital_channel_ids[id]
    else:
        plotdata = rec.analog[id]
        plotname = rec.analog_channel_ids[id]
    cmap = get_cmap(20)
    # fgr = plt.figure(figsize=(18.8, 2.7))
    fgr = plt.figure(figsize=(40, 2.7))
    margins = {
        "left": 0.000,
        "bottom": 0.090,
        "right": 0.990,
        "top": 0.990
    }

    fgr.subplots_adjust(**margins)
    plt.plot(rec.time, plotdata, color=cmap(id))
    plt.legend([plotname])
    return fig_to_html(fgr)


def GetGraphInfo(way):
    rec = Comtrade()
    rec.load(way + ".cfg", way + ".dat")
    data = {"analog" : rec.analog_channel_ids, "digital" : rec.digital_channel_ids, "time": format(rec.trigger_time), "name":rec.station_name, "time_base" : rec.time_base}
    return data


def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n % 255)

def getEventInfo(filename):
    rec = Cfg()
    rec.load(filename)
    return rec.start_timestamp, rec.analog_count, rec.digital_count