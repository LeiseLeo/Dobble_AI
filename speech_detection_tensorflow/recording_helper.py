import pyaudio
import numpy as np

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
p = pyaudio.PyAudio()

def record_audio():
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER,
        # input_device_index = 1
    )

    print("start recording...")

    frames = []
    seconds = 1

    recording = False 
    silence_count = 0

    while True:

        # Read audio data from the stream
        data = stream.read(1024)
        
        # Convert data to numpy array
        audio = np.frombuffer(data, dtype=np.int16)

        print("np.abs(audio).mean()", np.abs(audio).mean())
        last_noise = []
        while len(last_noise) < 5:
            last_noise.append(np.abs(audio).mean())
        print("last noise", last_noise)
        noise_sum = 0 
        for noise in last_noise:
            noise_sum = noise_sum + noise
        # Check if audio exceeds noise threshold
        print("noise sum / 5", noise_sum / 5)
        if (noise_sum / 5 ) > 10:
            print("sound detected")
            last_noise = []
            noise_sum = 0 
        
            for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
                data = stream.read(FRAMES_PER_BUFFER)
                frames.append(data)

            silence_count = 0

            print("recording stopped")

            stream.stop_stream()
            stream.close()
            
            return np.frombuffer(b''.join(frames), dtype=np.int16)


            # If noise detected, start recording
            # if not recording:
            #     print("Recording started.")
            #     recording = True
            
            # # Append audio data to recording frames
            # frames.append(data)
        
        # If no noise detected, count frames of silence
        else:
            if recording:
                silence_count += 1
                
                # If too many frames of silence, stop recording and save file
                if silence_count > (RATE/1024)*10:
                    print("Recording stopped.")
                    recording = False
                    
                    # Reset recording frames
                    frames = []
                    silence_count = 0
                    print("break while loop")
                    break
    


    # for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
    #     data = stream.read(FRAMES_PER_BUFFER)
    #     frames.append(data)

    # print("recording stopped")

    # stream.stop_stream()
    # stream.close()
    
    # return np.frombuffer(b''.join(frames), dtype=np.int16)


def terminate():
    p.terminate()
