import numpy as np
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import ShortTermFeatures, MidTermFeatures
import matplotlib.pyplot as plt

# 1. Read audio file
[Fs, x] = aIO.read_audio_file(r"C:\Users\82102\Desktop\프메\test_audio.wav")  # 음성 파일 경로를 지정하세요.
'''Fs ; 44100, 
x : [[   0    0]
 [   0    0]
 [   0    0]
 ...
 [1610 1610]
 [1929 1929]
 [1996 1996]]'''

# 2. Extract mid-term features (with default parameters)
mid_window, mid_step, short_window, short_step = 1, 1, 0.2, 0.2
mid_term_features, short_term_features, mid_feature_names = MidTermFeatures.mid_feature_extraction(x, Fs, mid_window * Fs, mid_step * Fs, round(Fs * short_window), round(Fs*short_step))

# 3. Get Voice Activity Detection feature (the last feature)
vad = mid_term_features[-1, :]

# 4. Convert VAD to segments (start and end times)
segments = []
segment_start = None
for i in range(len(vad)):
    if vad[i] == 1.0 and segment_start is None:  # Voice starts
        segment_start = i * mid_step
    elif vad[i] == 0.0 and segment_start is not None:  # Voice ends
        segments.append((segment_start, i * mid_step))
        segment_start = None
# VAD를 실행한 후 반환된 음성 세그먼트에 대해 반복
for start,end in segments : 
    # 세그먼트의 시작과 종료 시간을 출력합니다.
    print(f"Voice segment: {start} to {end}")