from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
# from fast_api import analysis
from fast_api.analysis.emotion_recognition import onnx_inference
# from fast_api.analysis.eye_tracking import *  # ##############
# from fast_api.analysis.speech_analysis import *  # ##############
# from fast_api.summarization.text_summarization import *
from fastapi import HTTPException

import numpy as np
import cv2
import tempfile
import os


async def analyze_file(file: UploadFile):
    if file.filename.endswith(".mp4"):
        # emotion recognition task
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_img:
            tmp_img.write(np_arr)
            tmp_img_path = tmp_img.name
        cap = cv2.VideoCapture(tmp_img_path)  # VideoCapture object
        tmp_img.close()
        os.unlink(tmp_img_path)

        emotion_list = onnx_inference.emotions_detector(cap)
        emotion_result = onnx_inference.emotion_detection_result(emotion_list)

        # eye tracking task

        # speech analysis task

        # speech_result = analyze_speech(file.file)  # ##############
        return JSONResponse(content={"emotion": emotion_result})  # ##############, "speech": speech_result}
    # elif file.filename.endswith((".txt", ".pdf", ".doc", ".docx")):
    #     summarized_text = summarize_text(file.file)
    #     return JSONResponse(content={"summarized_text": summarized_text})
    else:
        raise HTTPException(
            status_code=415, detail='Unsupported file format'
        )
