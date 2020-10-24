import tensorflow as tf

def TrainCNN(array):
    (x_train, y_train), (x_test, y_test) = array
    y_train = tf.keras.utils.to_categorical(y_train, num_classes) y_test = tf.keras.utils.to_categorical(y_test, num_classes)
    model.compile(loss=tf.keras.losses.categorical_crossentropy, optimizer=tf.keras.optimizers.Adadelta(), metrics=['accuracy'])
    vector = model.evaluate(x_test, y_test, verbose=0) 
    SaveCNN(y_train)
    return vector

def TrainAPT2(Vector):
    from numpy import exp, array, random, dot
    training_set_inputs = Vector
    training_set_outputs = Vector[:1].T
    random.seed(1)
    synaptic_weights = 2 * random.random((3, 1)) - 1
    for iteration in xrange(10000):
        output = 1 / (1 + exp(-(dot(training_set_inputs, synaptic_weights))))
        synaptic_weights += dot(training_set_inputs.T, (training_set_outputs - output) * output * (1 - output))
    print 1 / (1 + exp(-(dot(array([1, 0, 0]), synaptic_weights))))

def SaveCNN(weights):
    #добавить сохраниение сети
    a = 1

def SaveAPT2( synaptic_weights):
    #добавить сохраниение сети
    a = 1

def EvristicAnalisis(id, way, numberOfLines):
    _return = {"Type" : 1, "TimeOf":"12ms","APV":"Успешно","distanceToKZ":"2.145км" }
    #dbFunctions.getStatuses() - получение всех статусов {id:{'name':name}}
    return _return