from PyPDF2 import PdfFileWriter, PdfFileReader
from pytesseract import pytesseract
from difflib import SequenceMatcher
from PIL import Image
from pdf2image import convert_from_path
from pdf2image.exceptions import *
import cv2
import cv2 
import os
import io
pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract'


def get_mark(path):
    img_cv = cv2.imread(path)
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    new = pytesseract.image_to_string(img_rgb)
    true_answers = open('media/RightAnswers.txt').read()
    mark = SequenceMatcher(None, new, true_answers).ratio() * 1388 
    return mark

def exam_evaluate_map(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    pages = convert_from_path(path, 200)
    count = 1
    data = dict()
    for page in pages:
        image_name = 'media/diploma/{}_page_{}.png'.format(fname, count)
        page.save(image_name,'PNG')
        img = Image.open(image_name)
        img = cv2.imread(image_name)
        cropped_image = img[160:250, 400:850]
        student_full_name = pytesseract.image_to_string(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        data[student_full_name] = image_name 
        count += 1
    return data