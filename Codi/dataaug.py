from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import array_to_img, img_to_array, load_img

input_img = 1   # Nom de la primera imatge a importar
count = 3       # Nombre d'imatges derivades que es volen generar
group = 130     # Nom de l'última imatge a importar

datagen = ImageDataGenerator(
	zoom_range = 0.2,       # Es fa un zoom aleatori dins d'un marge de 0.2
	rotation_range = 40,    # Es fa una rotació aleatoria dins d'un marge de 40º
	fill_mode = 'nearest',  # Les parts que queden buides al rotar la imatge s'omplen amb el color del bit més proper
	horizontal_flip = True) # Es fa un volteig horitzontal de manera aleatoria

while input_img <= group:	
    input_path = 'data augmentation/%s.jpg' %input_img  # Directori on estan les imatges
    image = img_to_array(load_img(input_path))          # Es llegeix la imatge i es converteix en un array de valors
    image = image.reshape((1,) + image.shape)           # S'incrementa la dimensió de l'array en 1

# S'apliquen les transformacions amb la funció flow i es guarden les imatges resultants
    i=0
    for batch in datagen.flow(image, batch_size=group, save_to_dir='preview', save_prefix='pard{}'.format(input_img),save_format='jpg'):
        i += 1
        if i >= count:
            break
    input_img += 1  # Es passa a llegir i transformar la següent imatge del directori