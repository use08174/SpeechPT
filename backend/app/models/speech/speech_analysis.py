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
        advice = "청중이 내용을 더 잘 이해할 수 있도록 말의 속도를 약간 높이는 것을 고려해보세요. 느린 말속도는 주의를 분산시키고 메시지의 전달력을 약화시킬 수 있습니다."
        return f"cpm이 {cpm}으로, 말의 빠르기가 너무 느립니다. {advice}"
    elif 390 <= cpm <= 419:
        advice = "약간만 속도를 높여도 청중의 관심을 더 잘 유지할 수 있습니다. 조금 더 자신감을 가지고 명확하게 발음하면 더욱 효과적일 것입니다."
        return f"cpm이 {cpm}으로, 말의 빠르기가 약간 느립니다. {advice}"
    elif 420 <= cpm <= 449:
        advice = "이 속도는 청중이 내용을 잘 이해하고 따라갈 수 있는 이상적인 범위입니다. 현재의 말속도를 유지하며 명확한 발음과 강조를 통해 메시지를 전달하세요."
        return f"cpm이 {cpm}으로, 말의 빠르기가 보통입니다. {advice}"
    elif 450 <= cpm <= 479:
        advice = "말의 속도가 약간 빠른 편입니다. 중요한 포인트에서는 속도를 조금 줄여서 청중이 핵심 내용을 놓치지 않도록 해보세요."
        return f"cpm이 {cpm}으로, 말의 빠르기가 약간 빠릅니다. {advice}"
    else:
        advice = "속도가 매우 빠르므로 청중이 내용을 따라가기 어려울 수 있습니다. 중요한 정보를 전달할 때는 속도를 늦추고, 청중과의 상호작용을 통해 이해도를 확인하는 것이 좋습니다."
        return f"cpm이 {cpm}으로, 말의 빠르기가 너무 빠릅니다. {advice}"

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
    
    return f"발표동안 총 {num_pauses}번 {sum(pause_durations)}초 동안 일시정지되었습니다. "


def detect_korean_filler_words(transcribed_text):
    korean_filler_words = ["음", "어", "그", "아", "그러니까", "이제", "저기"]
    
    filler_word_counts = {word: 0 for word in korean_filler_words}
    
    words = transcribed_text.split()
    
    for word in words:
        if word in korean_filler_words:
            filler_word_counts[word] += 1
    
    filler_word_counts = {word: count for word, count in filler_word_counts.items() if count > 0}

    
    if not filler_word_counts:
        return "인식된 보충어가 없습니다."
    
    filler_words_summary = ", ".join([f"'{word}'는 {count}회" for word, count in filler_word_counts.items()])
    return f"보충어 사용 현황: {filler_words_summary}"

