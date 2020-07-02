from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers.core import Dense
from keras.optimizers import SGD
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import argparse
import random
import pickle
import cv2
import os

# Inicialització de les dades i les etiquetes
data = []
labels = []

# Es guarden els paths de les imatges
imagePaths = list(paths.list_images('ocells'))

# Cada una de les imatges d’entrada:
for imagePath in imagePaths:
	image = cv2.imread(imagePath)       # Es carrega la imatge
	image = cv2.resize(image, (32, 32)).flatten()   # Es redimensiona a 64x64 píxels i s'aplana en un vector
	data.append(image)                  # S'emmagatzema a la llista de dades

	label = imagePath.split(os.path.sep)[-2]    # S'extreu l'etiqueta de classe del path de la imatge
	labels.append(label)                        # S'actualitza la llista d'etiquetes

# S'escalen les intensitats de píxels en al rang [0, 1] i es guarden les dues llistes com un numpy array
data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

# Es separen les dades en les particions de train (75%) i test (25%)
(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.25, random_state=42)

# Les etiquetes es converteixen a vectors
lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# Es defineix l'arquitectura de la xarxa neuronal
model = Sequential()
model.add(Dense(1024, input_shape=(3072,), activation="tanh"))
model.add(Dense(512, activation="tanh"))
model.add(Dense(4, activation="softmax"))

# S'inicialitzen el learning rate i el # d'epochs
INIT_LR = 0.01
EPOCHS = 75

# S'inicialitzen el model i l'optimitzador
opt = SGD(lr=INIT_LR)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# Entrenament de la xarxa
H = model.fit(trainX, trainY, validation_data=(testX, testY),
	epochs=EPOCHS, batch_size=32)

# Avaluació de la xarxa
predictions = model.predict(testX, batch_size=32)
print(classification_report(testY.argmax(axis=1),
	predictions.argmax(axis=1), target_names=lb.classes_))

# Es grafiquen la pèrdua i la precissió
N = np.arange(0, EPOCHS)
plt.style.use("ggplot")
plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
plt.plot(N, H.history["accuracy"], label="train_acc")
plt.plot(N, H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy (Simple NN)")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig('output/simple_nn/simple_nn_plot.png')

# Es guarda el model ja entrenat
model.save('output/simple_nn/simple_nn.model')