import random
import xml.etree.cElementTree as ET
import cv2
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from matplotlib import pyplot as plt

# In diesem Pfad werden die XML und PNG Dateien gespeichert; nutzen sie die C:\x5c Notation 
# Beispiel: C:\x5cUsers\x5cleo\OneDrive\Desktop 
path_to_save = ""

background_game_card = Image.open(
    '512_card_background.png')  

# Bilder werden geladen
icons = {
    "heart_icon": Image.open('icons/350_heart.png'),
    "sun_glass_icon": Image.open('icons/350_sunglass.png'),
    "raindrop_icon": Image.open('icons/350_raindrop.png'),
    "hand_icon": Image.open('icons/350_hand.png'),
    "hammer_icon": Image.open('icons/350_hammer.png'),
    "bird_icon": Image.open('icons/350_bird.png'),
    "stop_icon": Image.open('icons/350_stopp.png'),
    "clock_icon": Image.open('icons/350_clock.png'),
    "net_icon": Image.open('icons/350_net.png'),
    "moon_icon": Image.open('icons/350_moon.png'),
    "men_icon": Image.open('icons/350_men.png'),
    "eye_icon": Image.open('icons/350_eye.png'),
    "yingyang_icon": Image.open('icons/350_yingyang.png'),
    "fire_icon": Image.open('icons/350_fire.png'),
    "exclamation_icon": Image.open(
        'icons/350_exclamation.png'),
    "anker_icon": Image.open('icons/350_anker.png'),
    "apple_icon": Image.open('icons/350_apple.png'),
    "bomb_icon": Image.open('icons/350_bomb.png'),
    "bulb_icon": Image.open('icons/350_bulb.png'),
    "cactus_icon": Image.open('icons/350_cactus.png'),
    "candle_icon": Image.open('icons/350_candle.png'),
    "car_icon": Image.open('icons/350_car.png'),
    "carrot_icon": Image.open('icons/350_carrot.png'),
    "cat_icon": Image.open('icons/350_cat.png'),
    "cheese_icon": Image.open('icons/350_cheese.png'),
    "clef_icon": Image.open('icons/350_clef.png'),
    "cloverleaf_icon": Image.open('icons/350_cloverleaf.png'),
    "cube_icon": Image.open('icons/350_cube.png'),
    "dino_icon": Image.open('icons/350_dino.png'),
    "dog_icon": Image.open('icons/350_dog.png'),
    "dolphin_icon": Image.open('icons/350_dolphin.png'),
    "dragon_icon": Image.open('icons/350_dragon.png'),
    "horse_icon": Image.open('icons/350_horse.png'),
    "igloo_icon": Image.open('icons/350_igloo.png'),
    "key_icon": Image.open('icons/350_key.png'),
    "ladybug_icon": Image.open('icons/350_ladybug.png'),
    "lightning_icon": Image.open('icons/350_lightning.png'),
    "lips_icon": Image.open('icons/350_lips.png'),
    "lock_icon": Image.open('icons/350_lock.png'),
    "maple_icon": Image.open('icons/350_maple.png'),
    "pen_icon": Image.open('icons/350_pen.png'),
    "question_icon": Image.open('icons/350_question.png'),
    "scissors_icon": Image.open('icons/350_scissors.png'),
    "skull_icon": Image.open('icons/350_skull.png'),
    "snowman_icon": Image.open('icons/350_snowman.png'),
    "spider_icon": Image.open('icons/350_spider.png'),
    "splotch_icon": Image.open('icons/350_splotch.png'),
    "sun_icon": Image.open('icons/350_sun.png'),
    "target_icon": Image.open('icons/350_target.png'),
    "tree_icon": Image.open('icons/350_tree.png'),
    "zebra_icon": Image.open('icons/350_zebra.png'),
    "clown_icon": Image.open('icons/350_clown.png'),
    "snow_flake_icon": Image.open('icons/350_snow_flake.png'),
    "turtle_icon": Image.open('icons/350_turtle.png'),
    "flower_icon": Image.open('icons/350_flower.png'),
    "bottle_icon": Image.open('icons/350_bottle.png'),
    "ghost_icon": Image.open('icons/350_ghost.png'),
}

backgrounds = {
    "grass_background_1": Image.open('backgrounds/grass_background_1.png'),
    "grass_background_2": Image.open('backgrounds/grass_background_2.png'),
    "grass_background_3": Image.open('backgrounds/grass_background_3.png'),
    "grass_background_4": Image.open('backgrounds/grass_background_4.png'),
    "special_background_1": Image.open('backgrounds/special_background_1.png'),
    "special_background_2": Image.open('backgrounds/special_background_2.png'),
    "special_background_3": Image.open('backgrounds/special_background_3.png'),
    "special_background_4": Image.open('backgrounds/special_background_4.png'),
    "special_background_5": Image.open('backgrounds/special_background_5.png'),
    "special_background_6": Image.open('backgrounds/special_background_6.png'),
    "special_background_7": Image.open('backgrounds/special_background_7.png'),
    "special_background_8": Image.open('backgrounds/special_background_8.png'),
    "stone_background_1": Image.open('backgrounds/stone_background_1.png'),
    "stone_background_2": Image.open('backgrounds/stone_background_2.png'),
    "stone_background_3": Image.open('backgrounds/stone_background_3.png'),
    "wood_background_1": Image.open('backgrounds/wood_background_1.png'),
    "wood_background_2": Image.open('backgrounds/wood_background_2.png'),
    "wood_background_3": Image.open('backgrounds/wood_background_3.png'),
    "wood_background_4": Image.open('backgrounds/wood_background_4.png'),
}

effects = {
    "lense_flare_1": Image.open('effects/lense_flare_1.png'),
    "lense_flare_2": Image.open('effects/lense_flare_2.png'),
    "lense_flare_3": Image.open('effects/lense_flare_3.png'),
    "lense_flare_4": Image.open('effects/lense_flare_4.png'),
    "lense_flare_5": Image.open('effects/lense_flare_5.png'),
    "lense_flare_6": Image.open('effects/lense_flare_6.png'),
    "lense_flare_7": Image.open('effects/lense_flare_7.png'),
    "lense_flare_8": Image.open('effects/lense_flare_8.png'),
    "lense_flare_9": Image.open('effects/lense_flare_9.png'),
    "lense_flare_10": Image.open('effects/lense_flare_10.png'),

}



def check_intersection(image1, image2, offset_x, offset_y, invert_image1=False):
    # Überprüfen jedes einzelnen Pixels auf den Alpha-Wert (a), wenn dieser frei ist kann ein Bild platziert werden (return False)
    for x in range(image2.width):
        for y in range(image2.height):
            image_2_rgba = image2.getpixel((x, y))
            image_1_rgba = image1.getpixel((x + offset_x, y + offset_y))
            if image_2_rgba[3] != 0 and ((image_1_rgba[3] != 0) ^ invert_image1):
                return True
    return False

# gibt eine zufällige Auswahl der value und keys aus einem dictionary zurück
def sample_dict(d, n):
    names = random.sample(sorted(d.keys()), n)
    obj = {}
    for name in names:
        obj[name] = d[name]
    print(names)
    return obj

# generiert eine XML-Datei (PASCAL-VOX-Format), welche Informationen über die Symbole auf der Karte enthält 
def generate_xml(icons_arr_name, icon_size_array):
    filename_png = filename = "card" + str(i) + ".png"  # 1 = i
    file_path = path_to_save + "/card" + str(
        i) + ".png"  

    annotation = ET.Element("annotation")
    folder = ET.SubElement(annotation, "folder").text = "training_dataset"
    filename = ET.SubElement(annotation, "filename").text = filename_png
    path = ET.SubElement(annotation, "path").text = file_path
    source = ET.SubElement(annotation, "source")

    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotation, "size")

    ET.SubElement(size, "width").text = "512"
    ET.SubElement(size, "height").text = "512"
    ET.SubElement(size, "depth").text = "3"

    segmented = ET.SubElement(annotation, "segmented").text = "0"

    for j in range(len(icons_arr_name)):
        object = ET.SubElement(annotation, "object")
        ET.SubElement(object, "name").text = icons_arr_name[j]

        # for k in range(len(icon_size_array)):
        ET.SubElement(object, "pose").text = "Unspecified"  # default
        ET.SubElement(object, "truncated").text = "0"  # default
        ET.SubElement(object, "difficult").text = "0"  # default

        bndbox = ET.SubElement(object, "bndbox")

        ET.SubElement(bndbox, "xmin").text = str(icon_size_array[j][0])
        ET.SubElement(bndbox, "ymin").text = str(icon_size_array[j][1])
        ET.SubElement(bndbox, "xmax").text = str(icon_size_array[j][2])
        ET.SubElement(bndbox, "ymax").text = str(icon_size_array[j][3])

    tree = ET.ElementTree(annotation)
    # filename = "card" + str(1) + ".xml"  # 1 = i
    tree.write(
        path_to_save + "/card" + str(
            i) + ".xml")


def generate_card():
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    icon_size_array = []
    sd = sample_dict(icons, 8)
    k = 0

    for name, image in sd.items():
        k += 1

        while True:
            rotation = random.randint(1, 360)
            image = image.rotate(rotation)
            size = random.randint((50 + 30 * (9 - k)) * 0.6, ((30 * (9 - k)) + 150) * 0.6)
            image = image.resize((size, size))
            xmin = random.randint(0, canvas.width - size)
            ymin = random.randint(0, canvas.height - size)
            xmax = xmin + size
            ymax = ymin + size

            if check_intersection(canvas, image, xmin, ymin) == False:
                if check_intersection(background_game_card, image, xmin, ymin, True) == False:
                    print("no intersection")
                    break

        _new_size = round(image.width * 0.9)
        image = image.resize((_new_size, _new_size))
        canvas.paste(image, (xmin, ymin), image)
        icon_size_array.append([xmin, ymin, xmax, ymax])

    card = background_game_card.copy()
    generate_xml(list(sd.keys()), icon_size_array)
    card.paste(canvas, (0, 0), canvas)
    return card


for i in range(700):
    print("Start creating card", i)
    card = generate_card()
    rdm_num = 4
    if rdm_num == 4:
        na = np.array(card).astype(float)
        # na[..., 0] *= random.uniform(0.4,0.9)
        na[..., 1] *= random.uniform(0.6,0.9)
        na[..., 2] *= random.uniform(0.5,1)


        card = Image.fromarray(na.astype(np.uint8))

        enhancer = ImageEnhance.Brightness(card)
        card = enhancer.enhance(random.uniform(1.01, 1.3))

    if (i % 2) == 0:
        # add noise
        for  j in range(round(card.size[0] * card.size[1] / random.randint(5, 20))):
            card.putpixel(
                (random.randint(0, card.size[0] - 1), random.randint(0, card.size[1] - 1)),
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            )

    # Add background
    _rdm__bck_key = random.choice(list(backgrounds.keys()))
    bck = backgrounds[_rdm__bck_key].copy()

    bck.paste(card,(0,0), card)

    # Add lense flare effect 
    if (random.randint(0,4) == 4):
        _rdm__effect_key = random.choice(list(effects.keys()))
        effect = effects[_rdm__effect_key]

        rotation = random.randint(1, 360)
        effect = effect.rotate(rotation)

        bck.paste(effect,(0,0), effect)

    bck.save(
        path_to_save + "/card" + str(
            i) + ".png")
    
    bck = Image.new("RGBA", (512, 512), (0, 0, 0, 0))