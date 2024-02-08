import subprocess
import tempfile

def extract_audio(video_file):
    # Create a temporary file for the extracted audio
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    
    # Define the ffmpeg command
    cmd = ['ffmpeg', '-i', video_file, '-f', 'mp3', '-acodec', 'mp3', temp_audio_file.name]
    
    # Execute the command
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Return the path of the temporary audio file
    return temp_audio_file.name


