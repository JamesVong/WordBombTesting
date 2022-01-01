import pyautogui
import pytesseract
import numpy as np
import random
import re

from ast import literal_eval
from time import sleep
from PIL import ImageGrab
from imgTest import test_image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

MAX_LENGTH = 8
# Hard-coded to find section of what characters to contain
# Bounds within 1920 x 1080
TOP = (550, 300, 1070, 450)
BOTTOM = (550, 650, 1070, 800)

# oem (OCR Engine Mode) 3 is default
# psm (Page segmentation modes), 11. Sparse text. Find as much text as possible in no particular order.
# Legend: https://stackoverflow.com/questions/64099248/pytesseract-improve-ocr-accuracy
config = '--oem 3 --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def determine_contains(bbox):
    im = ImageGrab.grab(bbox=bbox)
    output = test_image(np.array(im))
    return pytesseract.image_to_string(output, config=config, lang='eng')


def json_search(part, max_length):
    with open('condensed_english_words.txt.', 'r') as fp:
        word_list = fp.read()

    matches = [word for word in literal_eval(word_list) if part in word and 3 <= len(word) <= max_length]
    print(f"{len(matches)} matches.")
    return random.choice(matches) if len(matches) > 0 else None


sleep(3)
print("Turning on in 3...")
while True:
    sleep(0.2)
    txt = determine_contains(TOP)
    if len(txt) == 0:
        txt = determine_contains(BOTTOM)

    if len(txt) == 0:
        continue

    txt = txt.replace(" ", "").lower()
    txt = re.findall("[a-z]+", txt)
    print(f"Word contains: {txt[0]}")
    word = json_search(txt[0], MAX_LENGTH)
    print(word)
    if word:
        pyautogui.write(word, interval=0.01)
        sleep(0.5)

