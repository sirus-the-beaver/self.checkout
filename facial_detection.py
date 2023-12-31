from pathlib import Path
import face_recognition
import pickle
from collections import Counter
from PIL import Image, ImageDraw
import argparse
from moviepy.editor import *
import image_augmentation

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
    """
    This function handles the encoding of known faces. It takes in a model and encodings_location
    and then encodes the faces and saves them to the encodings_location.

    :param model: The model to use for encoding the faces. Can be either "hog" or "cnn".
    :param encodings_location: The location to save the encodings to.
    :return: None
    """
    
    # Augment ID image to get more training data
    image_augmentation.augment_image("training/sirus_salari/IMG_6089 2.jpg")

    # hog is faster but less accurate (best for CPU)
    # cnn is slower but more accurate (best for GPU)pip3 install face_recognition
    
    names = []
    encodings = []
    for filepath in Path("training").glob("*/*"):
        # Ignore .DS_Store files
        if filepath.name == '.DS_Store':
            continue

        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        # Detect faces and encode them
        # face_locations() returns a list of tuples for each face found in the image
        # Each tuple contains the coordinates of the top, right, bottom and left corner of the face
        face_locations = face_recognition.face_locations(image, model=model)

        # face_encodings() returns a list of 128-dimensional face encodings (one for each face in the image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # Add the face encoding and name for the current image to the training set
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    # Save the face encodings
    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open("wb") as f:
        pickle.dump(name_encodings, f)

#encode_known_faces()

def recognize_faces(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    This function handles the recognition of faces. It takes in an image_location, model and encodings_location
    and then encodes the faces and saves them to the encodings_location.

    :param image_location: The location of the image to recognize faces in.
    :param model: The model to use for encoding the faces. Can be either "hog" or "cnn".
    :param encodings_location: The location to save the encodings to.
    :return: None
    """
    
    # Load the face encodings
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    clip = VideoFileClip(image_location)
    
    for i in range(5):
        frame = "frame" + str(i) + ".jpg"
        clip.save_frame(frame, t = i)

        input_image = face_recognition.load_image_file(frame)

        # Find all the faces in the input image
        input_face_locations = face_recognition.face_locations(
            input_image, model=model
        )
        input_face_encodings = face_recognition.face_encodings(
            input_image, input_face_locations
        )

        # Create a PIL image to draw on
        pillow_image = Image.fromarray(input_image)

        # Create a Pillow ImageDraw Draw instance to draw with
        draw = ImageDraw.Draw(pillow_image)

        # Iterate over each face found in the input image
        for bounding_box, unknown_encoding in zip(
            input_face_locations, input_face_encodings
        ):
            # See if the face is a match for the known face(s)
            name = _recognize_face(unknown_encoding, loaded_encodings)
            if not name:
                name = "Unknown"
            print(name, bounding_box)
            _display_face(draw, bounding_box, name)

        del draw
        pillow_image.show()

def _recognize_face(unknown_encoding, loaded_encodings):
    # See if the face is a match for the known face(s)
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    """
    This private helper function handles the recognition of faces. It takes in an image_location, model and encodings_location
    and then encodes the faces and saves them to the encodings_location.

    :param unknown_encoding: The encoding of the face to recognize.
    :param loaded_encodings: The encodings of the known faces.
    :return: The name of the face if it is recognized, otherwise None.
    """

    # If a match was found in known_face_encodings, just use the first one.
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    # Get the most common name
    if votes:
        return votes.most_common(1)[0][0]
    


def _display_face(draw, bounding_box, name):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline="green")
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    """
    This private helper function handles the display of faces. It takes in a draw instance, bounding_box and name
    and then draws a bounding box and name on the image.

    :param draw: The draw instance to draw with.
    :param bounding_box: The bounding box of the face.
    :param name: The name of the face.
    :return: None
    """

    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill="green",
        outline="green",
    )
    draw.text(
        (text_left, text_top),
        name,
        fill="white",
    )


def validate():
    """
    This function handles the validation of the model.

    :return: None
    """

    for image in Path("validation").rglob("*"):
        if image.name == '.DS_Store':
            continue
        recognize_faces(str(image.absolute()))

#validate()

parser = argparse.ArgumentParser(prog='self.checkout', description='Draws bounding box outline around face(s) in image')

parser.add_argument('filename')

args = parser.parse_args()

recognize_faces(args.filename)