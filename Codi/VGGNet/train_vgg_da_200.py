from smallvggnet import SmallVGGNet
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from keras.preprocessing.image import ImageDataGenerator
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
	image = cv2.imread(imagePath)           # Es carrega la imatge
	image = cv2.resize(image, (200, 200))   # Es redimensiona a 64x64 píxels
	data.append(image)                      # S'emmagatzema a la llista de dades

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

# Es defineix el generador d'imatges per la data augmentation
aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

# S'inicialitza la CNN
model = SmallVGGNet.build(width=200, height=200, depth=3,
	classes=len(lb.classes_))

# S'inicialitzen el learning rate, # d'epochs i el batch size
INIT_LR = 0.01
EPOCHS = 75
BS = 32

# S'inicialitzen el model i l'optimitzador
opt = SGD(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# Entrenament de la xarxa amb data augmentation
H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
	validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
	epochs=EPOCHS)

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
plt.title("Training Loss and Accuracy (SmallVGGNet)")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend()
plt.savefig('output/vggnet_cnn_da_200/vggnet_da_200.png')

# Es guarda el model ja entrenat
model.save('output/vggnet_cnn_da_200/vggnet_da_200.model')