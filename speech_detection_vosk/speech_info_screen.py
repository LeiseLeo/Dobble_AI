import cv2
import numpy as np
# import torch
# from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
#                            increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)

font = cv2.FONT_HERSHEY_SIMPLEX

german_words = {'heart_icon': 'Herz','sun_glass_icon': 'Sonnenbrille', 'raindrop_icon': 'Regentropfen','hand_icon': "Hand", 'hammer_icon': 'Hammer',  'bird_icon': 'Vogel','stop_icon': 'Stoppschild', 'clock_icon':'Uhr','net_icon': 'Spinnennetz', 'moon_icon': 'Mond', 'men_icon': 'Mann','eye_icon': 'Auge', 'yingyang_icon': 'YingYang','fire_icon': 'Feuer', 'exclamation_icon': 'Ausrufezeichen','anker_icon': 'Anker', 'apple_icon': 'Apfel','bomb_icon': 'Bombe','bulb_icon':'Glühbirne', 'cactus_icon': 'Kaktus','candle_icon': 'Kerze', 'car_icon':'Auto', 'carrot_icon': 'Karotte','cat_icon': 'Katze', 'cheese_icon': 'Katze','clef_icon': 'Kleeblatt', 'cloverleaf_icon': 'Kleeblatt', 'cube_icon': 'Eiswürfel','dino_icon': 'Dinosaurier', 'dog_icon': 'Hund',  'dolphin_icon':'Delfin','dragon_icon': 'Drache', 'horse_icon': 'Pferd', 'igloo_icon': 'Iglu', 'key_icon': 'Schlüssel', 'ladybug_icon': 'Marienkäfer', 'lightning_icon': 'Feuerzeug','lips_icon': 'Lippen', 'lock_icon': 'Schloss', 'maple_icon': 'Ahornblatt', 'pen_icon': 'Stift','question_icon': 'Fragezeichen', 'scissors_icon': 'Scheere','skull_icon': 'Totenkopf','snowman_icon': 'Schneemann', 'spider_icon': 'Spinne', 'splotch_icon': 'Klecks', 'sun_icon': 'Sonne','target_icon': 'Fadenkreuz','tree_icon': 'Baum', 'zebra_icon': 'Zebra', 'clown_icon': 'Clown', 'snow_flake_icon': 'Schneeflocke', 'turtle_icon': 'Schildkröte','flower_icon': 'Blume', 'bottle_icon': 'Babyflasche', 'ghost_icon': 'Geist'}



def same_symbols(seq):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set(x for x in seq if x in seen or seen_add(x))
    # turn the set into a list (as requested)
    return list(seen_twice)

def create_info_screen(equal_symbol):
    canvas = np.zeros([512,512,1], dtype=np.uint8)
    canvas.fill(199)

    if equal_symbol == "*silence*":
        cv2.putText(canvas, (f"{equal_symbol}"), (25, 200), font, 0.75, (30,100,70), 1 , cv2.LINE_AA)
    else:
        cv2.putText(canvas, (f"Das gleiche Symbol ist: {equal_symbol}"), (25, 200), font, 0.75, (30,100,70), 1 , cv2.LINE_AA)

    return canvas

