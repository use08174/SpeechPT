import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

def perform_stt(audio_file_path):
    # Create a speech recognition object
    recognizer = sr.Recognizer()
    
    # Use the audio file
    with sr.AudioFile(audio_file_path) as source:
        audio_data = recognizer.record(source)  # Read the audio data
    
    # Try to recognize the speech using Google's STT
    print("start stt")
    try:
        text = recognizer.recognize_google(audio_data, language='ko-KR')  # Korean language
        return "Recognized text:", text
    except sr.UnknownValueError:
        return "Audio could not be understood"
    except sr.RequestError as e:
        return f"Service error: {e}" 

def analyze_speed(audio_file, stt_transcript):
    audio = AudioSegment.from_file(audio_file)
    duration_minutes = len(audio) / 60000.0
    
    # Use the transcription text directly
    num_characters = len(stt_transcript.replace(" ", ""))
    cpm = int(num_characters / duration_minutes)
    
    if cpm < 390:
        return "매우 느림"
    elif 390 <= cpm <= 419:
        return "조금 느림"
    elif 420 <= cpm <= 449:
        return "보통"
    elif 450 <= cpm <= 479:
        return "조금 빠름"
    else:
        return "매우 빠름"

def detect_pause(audio_file, min_silence_len=1000, silence_thresh=-40):
    audio = AudioSegment.from_file(audio_file)
    chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh, keep_silence=True)
    
    pause_durations = []
    last_position = 0
    for chunk in chunks:
        current_position = last_position + len(chunk)
        pause_duration = current_position - last_position - len(chunk)
        if pause_duration > 0:
            pause_durations.append(pause_duration)
        last_position = current_position

    num_pauses = len(pause_durations)
    return num_pauses, pause_durations


def detect_korean_filler_words(transcribed_text):
    korean_filler_words = ["음", "어", "그", "아", "그러니까", "이제", "저기"]
    
    filler_word_counts = {word: 0 for word in korean_filler_words}
    
    words = transcribed_text.split()
    
    for word in words:
        if word in korean_filler_words:
            filler_word_counts[word] += 1
    
    filler_word_counts = {word: count for word, count in filler_word_counts.items() if count > 0}
    
    return filler_word_counts

