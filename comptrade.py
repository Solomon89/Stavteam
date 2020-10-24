import matplotlib.pyplot as plt
from comtrade import Comtrade
rec = Comtrade()

rec.load("C:\\data\\04APR163.cfg", "C:\\data\\04APR163.dat")
print("Trigger time = {}s".format(rec.trigger_time))
print(type(rec.analog[0]))
plt.figure()
plt.plot(rec.time, rec.analog[0])
plt.plot(rec.time, rec.analog[9])
plt.legend([rec.analog_channel_ids[0], rec.analog_channel_ids[2]])
plt.show()