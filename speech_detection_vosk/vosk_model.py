
import argparse
import queue
import sys
import sounddevice as sd
import cv2

import json

from vosk import Model, KaldiRecognizer

from speech_info_screen import create_info_screen


similar_words = {
    "silence": ["", " "],
    "ahornblatt": ["abermals glattstreichen", "waren blatt"],
    "anker": ["anke", "antje", "alkhol"],
    "apfel": ["axel", "schön", "rat für", "rapsöl", "absenden", "anzahl", "ob für", "am schön"],
    "auge": ["aug"],
    "ausrufezeichen": [""], 
    "auto": ["autor", "aut"],
    "baum": ["warm", "warum", "wow", "bau", "baum"], 
    "blitz": ["letz", "lets", "blättern", "plätzchen"], 
    "blume": ["blumen", "lupe", "global", "lumen"],
    "bombe": [""],
    "brille": ["eule", "relevanz", "rille"], 
    "clown": ["klaun", "klauen", "schauen", "schlauen", "klon", "flauen"], 
    "delfin": ["delphin", "der schien", "in vielen"],
    "dinosaurier": ["die nur", "dino"], 
    "drache": ["drach", "rache", "gerade", "nache"],
    "eiswürfel": ["eiswürfeln", "eis hörfunk"], 
    "fadenkreuz": [""], 
    "feuer": ["euer", "heuer"],
    "flasche": ["flaschen"],
    "fragezeichen": ["ragen solche", "frage"], 
    "geist": ["heißt"],
    "glühbirne": ["birne", "hey werner", "liberale"], 
    "hammer": ["hallo habe", "habe", "aber"], 
    "Hand": ["Hand", "And", "Hände", "Handfläche"],
    "Herz": ["Herz", "Herze", "Herzen"],
    "Hund": ["Hund", "Hunde"],
    "Iglu": ["Ego", "ego", "irr", "iglu", "egloff", "reglos", "wie genug", "ihr genug", "egal"],
    "Kaktus": ["Kaktus"],
    "Karotte": ["Karotte"], 
    "Katze": ["Katze"],
    "Kerze": ["Kerze"], 
     "Klecks": ["Klecks", "klicks"],
       "Kleeblatt": ["Kleeblatt", "Klee"], 
         'Käse': ["Käse"], 
         "Lippen": ["Lippen, Lippe, Mund"], 
        "Mann": ["Mann", "man", "Man", "manne"], 
         "Marienkäfer": ["Marienkäfer"],
         "Mond": ["Mond", "Mohn", "Mont", "mon"],
         "Notenschlüssel": ["Notenschlüssel", "schlüssel", "Noten", "note"], 
 "Pferd": ["Pferd"],  
 "Schere": ["Schere", "scheren", "schären", "scher", "schere im"], 
   "Schildkröte": ["Schildkröte"], 
    "Schloss": ["Schloss"], 
    "Schlüssel": ["Schlüssel", "Schüssel", "Schüssle"], 
    "Schneeflocke": ["Schneeflocke", "flocke", "Schneefrocke"], 
    "Schneemann": ["Schneemann", "Schneeman"], 
    "Sonne": ["Sonne", "sonnig", "sonner"], 
    "Spinne": ["Spinner", "Spinne", "spinnen", "Spinn"], 
    "Spinnennetz": ["Spinnennetz", "netz"], 
    "Stift": ["Stift", "Stifte", "stiften"], 
    "Stoppschild":["Stoppschild", "Schild", "Stopp"], 
    "Totenkopf": ["Totenkopf", "kopf", "tot", "toten", "wurden kopf"], 
    "Tropfen": ["tropfen", "tropf", "Tropfen"], 
    "Uhr": ["Uhr", "uhren", "Uhrig"], 
    "Vogel": ["Vogel", "Vogele", "Vlogel"], 
    "YingYang": ["YingYang", "Ying Yang", "Ying", "Yang", "genialen", "Jürgen", "jüngern"], 
    "Zebra": ["Zebra", "Zeb", "Zebras" ],
}

all_names = list(similar_words.keys())

cv2.namedWindow("mic_info", cv2.WINDOW_NORMAL)
cv2.setWindowProperty('mic_info', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL)



q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="show list of audio devices and exit")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="audio file to store recording to")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="input device (numeric ID or substring)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="sampling rate")
parser.add_argument(
    "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
args = parser.parse_args(remaining)

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info["default_samplerate"])
        
    if args.model is None:
        # model = Model(lang="en-us")
        model = Model("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/vosk-model-small-de-0.15_2")
    else:
        model = Model("C:/Users/tabby/Desktop/Informatik/Double-KI/speech_recognition/vosk-model-small-de-0.15_2")
        # model = Model(lang=args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
            dtype="int16", channels=1, callback=callback):
        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        rec = KaldiRecognizer(model, args.samplerate)

        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                print(rec.Result())
            else:
                str_res = rec.PartialResult()
                # print(str_res)
                par_res = json.loads(str_res)
                # print(type(par_res))
                print(par_res["partial"])

                info_screen = create_info_screen("*silence*")

                if len(par_res["partial"]) > 2:
                    for name in all_names:
                        if (name.lower() == par_res["partial"].lower()):
                            info_screen = create_info_screen(name)
                            print("something")
                        else:
                            for alternative in similar_words[name]:
                                if alternative.lower() ==  par_res["partial"].lower():
                                    info_screen = create_info_screen(name)
                    
                    cv2.imshow('mic_info', info_screen )
                    cv2.waitKey(1)  # 1 millisecond

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))