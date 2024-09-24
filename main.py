from video_module import record_video
from audio_module import record_audio

def main():

    print("Recording video...")
    video_filename = record_video()

    print("Recording audio...")
    audio_filename = record_audio()

    print("Video file:", video_filename)
    print("Audio file:", audio_filename)