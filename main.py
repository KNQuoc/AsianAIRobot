import video_module
from audio_module import record_audio

def main():

    print("Recording video...")
    video_module.run_webcam_detection()

    print("Recording audio...")
    record_audio()

if __name__ == "__main__":
    main()
