from pyComtrade import pyComtrade
import pylab

comtradeObj = pyComtrade.ComtradeRecord(r'B:\COMPTRADE\04JUL205.cfg')
comtradeObj.ReadDataFile()

N = comtradeObj.getNumberOfSamples()

AnalogChannelData = comtradeObj.getAnalogChannelData(1)
DigitalChannelData = comtradeObj.getDigitalChannelData(1)

time = comtradeObj.getTime()
f, axarr = pylab.subplots(2, sharex=True)

axarr[0].plot(time, AnalogChannelData)
axarr[0].set_title('pyComtrade Demo')
axarr[0].grid()
axarr[1].plot(time, DigitalChannelData)
axarr[1].set_ylim(top=1.05)
axarr[1].grid()
axarr[1].set_xlabel('Time [s]')

pylab.show()