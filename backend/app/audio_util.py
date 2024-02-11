import tempfile
import subprocess
import os
import ffmpeg

def extract_audio(video_file_path: str) -> str:
    # Create a temporary file for the audio output
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        output_file = temp_audio_file.name

    try:
        print("Start extracting audio")
        # Execute the command, suppressing the stderr output
        input_file = ffmpeg.input(video_file_path)
        # Add overwrite_output() to overwrite the output file if it exists
        (input_file.output(output_file, acodec='pcm_s16le', ar='44100')
                   .overwrite_output()
                   .run(capture_stdout=True, capture_stderr=True))  # Added capture_stdout and capture_stderr to suppress output
        
        print(f"Audio extracted and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred during the audio extraction process: {e}")
        # Ensure the temporary file is deleted in case of error
        if os.path.exists(output_file):
            os.remove(output_file)
        return ""
    return output_file
