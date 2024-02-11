from fastapi import UploadFile
import onnxruntime as rt
import cv2
import numpy as np
from PIL import Image
from collections import Counter

providers = ['CPUExecutionProvider']
model = rt.InferenceSession('models/video/emotion_recognition/vit_quantized.onnx', providers=providers)


def emotions_detector(video):
    emotion_list = []
    visualization_number = 1
    while True:
        #print(f"Working...Processing the frame {visualization_number}")
        ret, frame = video.read()
        if not ret:
            break

        pil_image = Image.fromarray(frame)
        pil_image = Image.fromarray(frame)
        image = np.array(pil_image)

        face_haar_cascade = cv2.CascadeClassifier('models/video/haarcascade_frontalface_default.xml')
        face_haar_cascade = cv2.CascadeClassifier('models/video/haarcascade_frontalface_default.xml')
        faces_detected = face_haar_cascade.detectMultiScale(frame, 1.1, 5, minSize=(30, 30))

        for (x, y, w, h) in faces_detected:
            # Crop and resize the face region for the model/preprocessing
            face = frame[y:y + h, x:x + w]
            face = cv2.resize(face, (256, 256))
            im = np.float32(face)
            im = np.expand_dims(im, axis=0)

            onnx_prediction = model.run(['dense'], {'input_image': im})

            class_names = ['angry', 'happy', 'neutral', 'sad', 'surprised']
            emotion = class_names[np.argmax(onnx_prediction[0][0])]
            emotion_list.append(emotion)
            visualization_number += 1
    return emotion_list


def emotion_detection_result(p_emotion_list):
    len_emotion_list = len(p_emotion_list)
    element_counts = Counter(p_emotion_list)
    result_emotions = []
    threshold = 0.6
    for e, cnt in element_counts.items():
        if e == "neutral":
            continue
        else:
            percent = cnt / len_emotion_list
            if percent >= threshold:
                result_emotions.append(e)

    if len(result_emotions) == 0:
        result_emotions.append('neutral')

    return {'emotion': result_emotions}
