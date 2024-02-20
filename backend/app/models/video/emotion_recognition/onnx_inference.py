from fastapi import UploadFile
import onnxruntime as rt
import cv2
import numpy as np
from PIL import Image
from collections import Counter
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "vit_quantized.onnx")
providers = ['CPUExecutionProvider']
model = rt.InferenceSession(model_path, providers=providers)

emo_feedback_dict = {
    'angry': "화나보이는 표정을 짓는 순간이 필요 이상으로 많아 보입니다. 발표 시 중요한 요소 중 하나는 안정감있는 표정입니다. 따라서 화내는 표정이 꼭 필요한 경우를 제외하고는, 보다 평온하고 중립적인 표정을 지을 수 있도록 연습하는 것이 좋을 것 같습니다.",
    'happy': "행복한 표정은 상대에게 호감을 느낄 수 있게하는 좋은 표정이기는 하나, 공식적인 발표 자리에서는 조금 더 중립적이고 안정감있는 표정을 유지하는 것이 좋을 것 같습니다. 기본 표정은 조금 더 중립적으로 유지하되, 필요한 경우에 따라 약간의 웃음을 섞어주면 도움이 될 것입니다.",
    'neutral': "발표에 가장 적절한 중립적이고 안정감있는 표정을 잘 유지하고 있습니다. 현재 표정을 기억하고 유지하되, 추가적인 말씀을 드리자면, 필요한 경우에 따라 약간 화나거나 슬픈 표정등을 적절히 사용하여 발표의 질을 더욱 높일 수도 있을 것입니다.",
    'sad': "슬퍼보이는 표정을 짓는 순간이 필요 이상으로 많아 보입니다. 발표 시 중요한 요소 중 하나는 안정감있는 표정입니다. 따라서 슬퍼하 표정이 꼭 필요한 경우를 제외하고는는, 보다 평온하고 중립적인 표정을 지을 수 있도록 연습하는 것이 좋을 것 같습니다.",
    'surprised': "놀란 표정을 짓는 순간이 필요 이상으로 많아 보입니다. 발표 시 중요한 요소 중 하나는 안정감있는 표정입니다. 따라서 놀란 표정이 꼭 필요한 경우를 제외하고는 보다 평온하고 중립적인 표정을 지을 수 있도록 연습하는 것이 좋을 것 같습니다."
}


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

    feedback_rst = []
    emo_feedback_dict_keys = emotions_feedback_dict.keys()
    for emo in result_emotions:
        if emo in emo_feedback_dict_keys:
            feedback_rst.append(emotions_feedback_dict[emo])

    return {'emotion': feedback_rst}
