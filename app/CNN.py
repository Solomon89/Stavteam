#import tensorflow as tf
from comtrade import Comtrade

#def TrainCNN(array):
    #(x_train, y_train), (x_test, y_test) = array
    #y_train = tf.keras.utils.to_categorical(y_train, num_classes) y_test = tf.keras.utils.to_categorical(y_test, num_classes)
   # model.compile(loss=tf.keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.Adadelta(), metrics=['accuracy'])
    #vector = model.evaluate(x_test, y_test, verbose=0) 
    #SaveCNN(y_train)
    #return vector

#def TrainAPT2(Vector):
    #from numpy import exp, array, random, dot
    #training_set_inputs = Vector
    #training_set_outputs = Vector[:1].T
    #random.seed(1)
    #synaptic_weights = 2 * random.random((3, 1)) - 1
    #for iteration in xrange(10000):
    #    output = 1 / (1 + exp(-(dot(training_set_inputs, synaptic_weights))))
   #     synaptic_weights += dot(training_set_inputs.T, (training_set_outputs - output) * output * (1 - output))
   # print 1 / (1 + exp(-(dot(array([1, 0, 0]), synaptic_weights))))

def SaveCNN(weights):
    #добавить сохраниение сети
    a = 1

def SaveAPT2( synaptic_weights):
    #добавить сохраниение сети
    a = 1

def EvristicAnalisis(id, way, analogLineCount):
    _return = {"Type" : 1, "TimeOf":"12ms","APV":"Успешно","distanceToKZ":"2.145км" }
    way += ".cfg"
    for i in range(1, analogLineCount + 1):
        (kz1, t1) = findShorCircuit(way, i * 4)
        (kz2, t2) = findShorCircuit(way, i * 4 + 1)
        (kz3, t3) = findShorCircuit(way, i * 4 + 2)
        (kz4, t4) = findShorCircuit(way, i * 4 + 3)
        if kz1 + kz2 + kz3 != 0:
            return {"Type" : kz1 + kz2 + kz3, "TimeOf": str(max([t1, t2, t3, t4])*100) + 'ms',
                    "APV":"Успешно","distanceToKZ":"2.145км" }
    return _return


def findShorCircuit(file_path, phases):
    rec = Comtrade()
    rec.load(file_path)
    # normal_i = np.mean(np.array(rec.analog[phases]))
    normal_i = rec.analog[phases][0]
    normal_delta_i = 0.0015
    time1 = 0
    time2 = 0
    short_circuit = False
    for i in range(0, len(rec.analog[phases]) - 2):
        roll = rec.analog[phases][i: i + 3]
        roll_type = extremum(roll)
        if roll_type == 0 or roll_type == 1:
            if abs(roll[1]) - normal_i > normal_delta_i:
                if not short_circuit:
                    short_circuit = True
                    time1 = i
            else:
                if short_circuit:
                    time2 = i
                    break
    return short_circuit, rec.time[time2] - rec.time[time1]


def extremum(roll):
    if roll[0] < roll[1] > roll[2]:
         return 0  # local max
    if roll[0] > roll[1] < roll[2]:
        return 1  # local_min
    if roll[0] > roll[1] > roll[2]:
        return 2  # decreases
    if roll[0] < roll[1] < roll[2]:
        return 3  # increases
    return -1