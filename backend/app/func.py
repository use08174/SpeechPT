import numpy as np
import cv2
import tempfile
import os 
import uuid

from fastapi import File, UploadFile
from fastapi.responses import JSONResponse,FileResponse
from fastapi import HTTPException

from models.video.emotion_recognition import onnx_inference
from models.text.extraction import extract_text_from_file
from models.text.summarization import summarize_text
from models.video.eye_tracking.example import analyze_gaze
from models.speech.speech_analysis import *
from audio_util import extract_audio

async def analyze_pt_file(file: UploadFile):
    # Read the file's contents once
    contents = await file.read()
    
    # Use a temporary file for processing the video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(contents)
        temp_video_path = temp_video.name
        
    try:
        if file.filename.endswith((".mp4")):
            print("pt analysis started..")
            # 1. emotion analysis
            cap = cv2.VideoCapture(temp_video_path)
            if not cap.isOpened():
                raise Exception("Could not open video file for emotion recognition")
            
            emotion_list = onnx_inference.emotions_detector(cap)
            emotion_result = onnx_inference.emotion_detection_result(emotion_list)
            cap.release()
            print("emotion analysis finished..")
            
            # 2. gaze tracking
            try:
                gaze_result = analyze_gaze(temp_video_path)
                print("눈동자 추적 분석 결과:", gaze_result)
            except Exception as e:
                print(f"오류 발생: {e}")
                gaze_result = {}  # 오류 발생 시 빈 결과 반환
                
            print("gaze tracking finished..")

            # 3. speech analysis
            speech_analysis_results = perform_speech_analysis(temp_video_path)
                
            result = {
                    "emotion": emotion_result,
                    "gaze": gaze_result,
                    "speech": speech_analysis_results
            }
            print(result)

        else:
            raise HTTPException(status_code=415, detail="Unsupported file format")

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error processing file: {e}")
        result = {"error": str(e)}

    return result


async def analyze_sum_file(file: UploadFile):
    # Read the file's contents once
    contents = await file.read()
    
    try:
        # Assuming `file` is an object with attributes/methods to access its filename and contents
        file_extension = file.filename.rsplit('.', 1)[1].lower()  # Extract the file extension
        if file_extension in ("pdf", "docx"):
            contents = await file.read()  # This is just an example; the actual method may vary.
            extracted_text = await extract_text_from_file(file_extension, contents)
            print(extracted_text)
            summarized_text = summarize_text(extracted_text)
            
            result = {"summarized_text": summarized_text}
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error processing file: {e}")
        result = {"error": str(e)}
    return result


def perform_speech_analysis(temp_video_path):
    try:
        audio_file_path = extract_audio(temp_video_path)
        stt_result = perform_stt(audio_file_path)
        print(stt_result)
        
        if isinstance(stt_result, tuple):
            stt_text = stt_result[1]  # Extract the text from the result
        else:
            stt_text = stt_result  # Directly use the result if it's not a tuple

        speech_speed = analyze_speed(audio_file_path, stt_text)
        num_pauses = detect_pause(audio_file_path)

        filler_words= detect_korean_filler_words(stt_text)

        os.remove(audio_file_path)


    except Exception as e:
        # Handle any potential errors gracefully
        return {"error": str(e)}
    
    print("analyzing audio_file finished")
    # Return the analyzed speech data
    print("filler", filler_words)
    return {
        "speed": speech_speed,
        "num_pauses": num_pauses,
        "filler_words": filler_words
    }