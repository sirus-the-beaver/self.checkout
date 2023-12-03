from keras.preprocessing.image import ImageDataGenerator
from skimage import io

def augment_image(input_image):
    # Create an ImageDataGenerator and do Image Augmentation
    datagen = ImageDataGenerator(
        rotation_range=40,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.2,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.2,  # randomly shift images vertically (fraction of total height)
        shear_range=0.2,  # set range for random shear
        zoom_range=0.2,  # set range for random zoom
        horizontal_flip=True,  # randomly flip images
        fill_mode='nearest')  # set mode for filling points outside the input boundaries

    # Load image and reshape
    input_image = io.imread(input_image)
    input_image = input_image.reshape((1,) + input_image.shape)

    # Generate 20 augmented images and save to the directory
    i = 0
    for batch in datagen.flow(input_image, batch_size=16,
                                save_to_dir='training/sirus_salari', save_prefix='sirus_salari', save_format='jpeg'):
            i += 1
            if i > 20:
                break