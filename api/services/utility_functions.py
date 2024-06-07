import json
import cv2

def open_json_file(file_path):
    f = open(file_path)
    data = json.load(f)
    
    return data

def preprocess_image(image,target_size):
    return cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2RGB),target_size) / .255