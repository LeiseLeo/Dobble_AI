from audiomentations import Compose, AddGaussianNoise, TimeStretch, PitchShift, Shift, AddBackgroundNoise, PolarityInversion, LowPassFilter, Gain, BandPassFilter
import numpy as np
import wave 
from scipy.io.wavfile import write
import os 
import random 
import shutil


def convert_wav_to_numpy(audio):
    '''
    Takes .wav file as input and converts it to an numpy array  
    '''
    # Convert buffer to float32 using NumPy                                                                                 
    audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
    audio_as_np_float32 = audio_as_np_int16.astype(np.float32)

    # Normalise float32 array so that values are between -1.0 and +1.0                                                      
    max_int16 = 2**15
    audio_normalised = audio_as_np_float32 / max_int16
    return audio_normalised

def compose_random_augment(filename):
    '''
    Adds randomly different noise or effects to audio files and return them 
    '''
    message = ""
    def apply_stuff(_rdm, _filename):
        global message
        if _rdm == 1:
            message = "Gaussian Noise and Background Noise has been added to" + _filename
            background_noise_path = "C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/examples/background" # from https://zenodo.org/record/3713328#.XyAMoy-w2L4
            # background_noise_path = "C:/Users/tabby/Downloads/ESC-50-master/ESC-50-master/audio"
            augment = Compose([
                AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.02, p=1),
                AddBackgroundNoise(sounds_path=background_noise_path, min_snr_in_db=3.0, max_snr_in_db=30.0, noise_transform=PolarityInversion(), p=1.0)
            ])
            return augment
    
        if _rdm == 2:
            message = "Applys Time Shifts and strechtes the audio"
            augment = Compose([
                TimeStretch(min_rate=0.8, max_rate=1.25, p=1),
                Shift(min_fraction=-0.1, max_fraction=0.1, p=1),
            ])
            return augment

        if _rdm == 3:
            message = "Applys a random selection 1"
            augment = Compose([
                AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.02, p=0.5),
                TimeStretch(min_rate=0.8, max_rate=1.25, p=0.5),
                PitchShift(min_semitones= 3, max_semitones=3, p=0.5),
                Shift(min_fraction=-0.1, max_fraction=0.1, p=0.5),
            ])
            return augment
            
        if _rdm == 4:
            message = "Applys a random selection 2"
            augment = Compose([
                LowPassFilter(),
                Gain(),
                BandPassFilter(),
            ])
            return augment


    rdm = random.randint(0,4)
    augment = apply_stuff(rdm, file_name)

    while augment == None:
        rdm = random.randint(0,4)
        augment = apply_stuff(rdm, file_name)
        print("message:", message)
    
    return augment

save_dir = "C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/examples/augmented_dataset/"
dataset_path = "C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/examples/dataset_new 2/" 

os.chdir("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/examples/dataset_new 2")

for folder_name in os.listdir(os.getcwd()):
    count = 0 
    print(folder_name)
    class_path = dataset_path + folder_name
    for file_name in os.listdir(class_path):
        count = count + 1

        # load audio file 
        input_file = wave.open(class_path + "/" + file_name)
        samples = input_file.getnframes()
        audio = input_file.readframes(samples)

        # Get and print sample rate from audio + len
        sample_rate = input_file.getframerate()     
        print("sample rate:", sample_rate)
        print("sample lenght", len(audio))

        audio_normalised = convert_wav_to_numpy(audio)

        print("audio_normalised", audio_normalised)
        augment = compose_random_augment(file_name)

        augmented_file = augment(samples=audio_normalised, sample_rate=16000)
        
        aug_new_file_path = save_dir + folder_name + "/" + file_name[:-4] + "_aug.wav"     
        source_new_file_path = save_dir + folder_name + "/" + file_name

        os.chdir(save_dir)
                                                  
        max_int16 = 2**15
        float32 = augmented_file * max_int16
        audio_as_np_float16 = float32.astype(np.int16)


        if os.path.exists(save_dir + folder_name):
            # write(aug_new_file_path, 16000, augmented_file)
            # write(source_new_file_path,16000, audio_normalised)

            outwav = wave.open(aug_new_file_path, 'w')
            outwav.setparams(input_file.getparams())
            outwav.setnchannels(1)
            outwav.writeframes(audio_as_np_float16.tostring())
            outwav.close()
            shutil.copyfile(class_path + "/" + file_name, source_new_file_path)

        else:
            os.makedirs(folder_name)
            
            outwav = wave.open(aug_new_file_path, 'w')
            outwav.setparams(input_file.getparams())
            outwav.setnchannels(1)
            outwav.writeframes(audio_as_np_float16.tostring())
            outwav.close()

            shutil.copyfile(class_path + "/" + file_name, source_new_file_path)

            # write(aug_new_file_path, 16000, augmented_file)
            # write(source_new_file_path,16000, audio_normalised)
