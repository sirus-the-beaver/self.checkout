from pathlib import Path
import face_recognition
import pickle

DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")

def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
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

# RUN ONLY ONCE
# encode_known_faces()

def recognize_faces(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    
    # Load the face encodings
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)
