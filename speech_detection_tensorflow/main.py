import numpy as np
import tensorflow as tf
from tensorflow.keras import models
from keras.models import model_from_json
import wave
from time import sleep

from recording_helper import record_audio, terminate
from tf_helper import preprocess_audiobuffer, convert_wav_to_numpy

commands = ['Auto', 'Blitz', 'Blume', 'Geist', 'Katze', 'Kerze', 'SchildkrФte', 'Zebra']

audio_from_mic = True

commands = ['Ahornblatt', 'Anker', 'Apfel', 'Auge', 'Ausrufezeichen', 'Auto', 'Baum',
 'Blitz', 'Blume', 'Bombe', 'Brille', 'Clown', 'Delfin', 'Dino', 'Drache',
 'EiswБrfel', 'Fadenkreuz', 'Feuer', 'Flasche', 'Fragezeichen', 'Geist',
 'GlБhbirne', 'Hammer', 'Hand', 'Herz', 'Hund', 'Iglu', 'Kaktus', 'Karotte',
 'Katze', 'Kerze', 'Klecks', 'Kleeblatt', 'KДse', 'Lippen', 'Mann', 'MarienkДfer',
 'Mond', 'NotenschlБssel', 'Pferd', 'Schere', 'SchildkrФte', 'Schloss',
 'SchlБssel', 'Schneeflocke', 'Schneemann', 'Sonne', 'Spinne', 'Spinnennetz',
 'Stift', 'Stoppschild', 'Totenkopf', 'Tropfen', 'Uhr', 'Vogel', 'YingYang',
 'Zebra', 'background']


# loaded_model = models.load_model("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/tensorflow_approach/saved_model", compile=False)
# loaded_model = models.load_model("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/tensorflow_approach/saved_model3", compile=False)

# loaded_model = tf.saved_model.load("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/tensorflow_approach/saved")

#test start
json_file = open('C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/tensorflow_approach/ai3/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/tensorflow_approach/ai3/model.h5")
#test end 

print("Loaded model from disk")

print("loaded model")

def predict_mic():

    if audio_from_mic:
        audio = record_audio()
    else:
        _input = wave.open("C:/Users/tabby/Documents/Sound Recordings/222.wav")
        _samples = _input.getnframes()
        audio = _input.readframes(_samples)
        audio = convert_wav_to_numpy(audio)

    print("audio", audio)

    # max_int16 = 2**15
    # float32 = audio * max_int16
    # audio_as_np_float16 = float32.astype(np.int16)
    if audio_from_mic:
        outwav = wave.open("C:/Users/tabby/Documents/Sound Recordings/222.wav", 'w')
        # outwav.setparams(input_file.getparams())
        outwav.setframerate(16000)
        outwav.setsampwidth(2)
        outwav.setnchannels(1)
        outwav.writeframes(audio.tobytes())
        outwav.close()

        print("done save")
        sleep(1)

    spec = preprocess_audiobuffer(audio)

    prediction = loaded_model(spec)
    print("prediction", prediction)

    label_pred = np.array([])

    # test_arr = np.array(["hi", "sus"])
    # test_arr = np.append(test_arr, [0,1])
    # print("test_arr", test_arr)



    label_pred = np.argmax(prediction, axis=1)
    # label_pred.append(0)
    # label_pred = np.append(label_pred, [0])

    # print("label_pred", label_pred)
    # print("label_pred[0]", label_pred[0])
    # print("commands[0]", commands[0])

    command = commands[label_pred[0]]
    print("Predicted label:", command)
    sleep(1)
    return command

if __name__ == "__main__":
    # from turtle_helper import move_turtle
    while True:
        command = predict_mic()
        # move_turtle(command)
        # if command == "stop":
        #     terminate()
        #     break