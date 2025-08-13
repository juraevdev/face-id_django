import face_recognition
import numpy as np
from PIL import Image
from typing import Optional

def encode_face(image_file) -> Optional[np.ndarray]:
    try:
        image = Image.open(image_file).convert("RGB")
        image = np.array(image, dtype=np.uint8).copy()
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            return face_encodings[0]
        return None
    
    except Exception as e:
        print(f"Encoding error: {str(e)}")
        return None


def verify_face(image_file, user_encoding: list) -> bool:
    new_face_encoding = encode_face(image_file)
    if new_face_encoding is None:
        return False
    return face_recognition.compare_faces([np.array(user_encoding)], new_face_encoding)[0]
