from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from keras.models import load_model
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import itertools
import cv2
import os

# Es carrega del model ja entrenat
model = load_model('output/vggnet_cnn_da_200/vggnet_da_200.model')

# Es carregen les imatges i se separen en els conjunts test i train
# (mateix codi que per a l'entrenament de la xarxa)
data = []
labels = []

imagePaths = sorted(list(paths.list_images('ocells')))

for imagePath in imagePaths:
	image = cv2.imread(imagePath)
	image = cv2.resize(image, (200, 200))
	data.append(image)

	label = imagePath.split(os.path.sep)[-2]
	labels.append(label)

data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(data,
	labels, test_size=0.25, random_state=42)

lb = LabelBinarizer()
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

# Avaluació de la xarxa
predictions = model.predict(testX, batch_size=32)
print(classification_report(testY.argmax(axis=1),
	predictions.argmax(axis=1), target_names=lb.classes_))

# Plot de la matriu de confusió
cm = confusion_matrix(testY.argmax(axis=1), predictions.argmax(axis=1))

plt.figure()
plt.figure(figsize=(10,10))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion matrix')
plt.colorbar()
tick_marks = np.arange(len(lb.classes_))
plt.xticks(tick_marks, lb.classes_, rotation=45)
plt.yticks(tick_marks, lb.classes_)
fmt = '.0f'
thresh = cm.max() / 2.
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.savefig('output/vggnet_cnn_da_200/cm_test.png')