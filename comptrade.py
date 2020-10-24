import matplotlib.pyplot as plt
from comtrade import Comtrade

rec = Comtrade()
rec.load(r'B:\COMPTRADE\04JUL205.cfg')
print("Trigger time = {}s".format(rec.trigger_time))

plt.figure()
plt.plot(rec.time, rec.digital[4])
print(type(rec.digital[4]))
plt.legend([rec.digital_channel_ids[0]])
plt.show()