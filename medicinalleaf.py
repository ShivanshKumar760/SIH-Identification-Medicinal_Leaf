# -*- coding: utf-8 -*-
"""MedicinalLeaf.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17x5hDNU49Yqy0Mv2-cgizR9641fzkqZS
"""

import tensorflow as tf
import matplotlib.pyplot as plt

img_height , img_width=32,32
batch_size=20
train_ds=tf.keras.utils.image_dataset_from_directory(
    "/content/drive/MyDrive/MedicinalLeafs/train",
    image_size=(img_height,img_width),
    batch_size=batch_size
)

val_ds=tf.keras.utils.image_dataset_from_directory(
    "/content/drive/MyDrive/MedicinalLeafs/validation",
    image_size=(img_height,img_width),
    batch_size=batch_size
)

test_ds=tf.keras.utils.image_dataset_from_directory(
    "/content/drive/MyDrive/MedicinalLeafs/test",
    image_size=(img_height,img_width),
    batch_size=batch_size
)

class_name=['Alpinia Galanga','Amaranthus Viridis','Artocarpus Hetrophyllus']
plt.figure(figsize=(10,10))
for images,labels in train_ds.take(1):
  for i  in range(9):
    ax=plt.subplot(3,3,i+1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_name[labels[i]])
    plt.axis("off")

model=tf.keras.Sequential(

    [
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(32,3,activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32,3,activation="relu"),
        tf.keras.layers.MaxPooling2D(),
        tf.keras.layers.Conv2D(32,3,activation="relu"),
        tf.keras.layers.MaxPooling2D(),


        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128,activation="relu"),
        tf.keras.layers.Dense(3)
    ]
)

model.compile(
    optimizer="adam",
    loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=20
)

model.evaluate(test_ds)

import numpy

plt.figure(figsize=(10,10))
for images,labels in test_ds.take(1):
  classifications=model(images)
  print(classifications)

import numpy

plt.figure(figsize=(10,10))
for images,labels in test_ds.take(1):
  classifications=model(images)
  # print(classifications)

  for i in range(9):
    ax=plt.subplot(3,3,i+1)
    plt.imshow(images[i].numpy().astype("uint8"))
    index=numpy.argmax(classifications[i])
    plt.title("pre:"+class_name[index]+"\n| Rel:      "+class_name[labels[i]])

converter=tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model=converter.convert()
with open("model.tflite",'wb') as f:
  f.write(tflite_model)