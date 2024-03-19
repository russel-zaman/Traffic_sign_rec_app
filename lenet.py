import numpy as np
#import streamlit as st
import cv2 as cv
from PIL import Image
from keras.models import load_model
import os


# Label traffic signs original was "labels_dict" ,now "classes"
labels_dict = {
    0: 'Speed limit (20km/h)',
    1: 'Speed limit (30km/h)',
    2: 'Speed limit (50km/h)',
    3: 'Speed limit (60km/h)',
    4: 'Speed limit (70km/h)',
    5: 'Speed limit (80km/h)',
    6: 'End of speed limit (80km/h)',
    7: 'Speed limit (100km/h)',
    8: 'Speed limit (120km/h)',
    9: 'No passing',
    10: 'No passing vehicle over 3.5 tons',
    11: 'Right-of-way at intersection',
    12: 'Priority road',
    13: 'Yield',
    14: 'Stop',
    15: 'No vehicles',
    16: 'Vehicle > 3.5 tons prohibited',
    17: 'No entry',
    18: 'General caution',
    19: 'Dangerous curve left',
    20: 'Dangerous curve right',
    21: 'Double curve',
    22: 'Bumpy road',
    23: 'Slippery road',
    24: 'Road narrows on the right',
    25: 'Road work',
    26: 'Traffic signals',
    27: 'Pedestrians',
    28: 'Children crossing',
    29: 'Bicycles crossing',
    30: 'Beware of ice/snow',
    31: 'Wild animals crossing',
    32: 'End speed + passing limits',
    33: 'Turn right ahead',
    34: 'Turn left ahead',
    35: 'Ahead only',
    36: 'Go straight or right',
    37: 'Go straight or left',
    38: 'Keep right',
    39: 'Keep left',
    40: 'Roundabout mandatory',
    41: 'End of no passing',
    42: 'End no passing vehicle > 3.5 tons'
}

    

def sign_predict(image_usr):
    print(image_usr)
    image = Image.open(image_usr)
    image_np = np.array(image.convert('RGB'))
    image_col = cv.cvtColor(image_np, 1)
    image_gray = cv.cvtColor(image_col, cv.COLOR_BGR2GRAY)
    image_32 = cv.resize(image_gray, (32, 32))
    model = load_model('./lenet5_model/')
    #model = load_model('lenet5_kaggle/lenet5_kaggle_saved_model_and_history/lenet5_kaggle_50epoch.h5')
    
    image = np.array(image_32, dtype=np.float32)
    image = image/255
    image = np.reshape(image, (1, 32, 32))
    x = image.astype(np.float32)
    prediction = model.predict(x)
    prediction_max = np.argmax(prediction)
    #get the detection class
    prediction_label = labels_dict[prediction_max]
    #get the confidence
    confidence = np.max(prediction)

    #get the original filename from the provided path
    dirname, filename = os.path.split(image_usr)
    print("now print the file name")
    print(filename)
    #define output directory
    output_dir = 'static/lenet_detect'
    if not os.path.exists(output_dir):
     os.makedirs(output_dir)

    output_path = os.path.join(output_dir, filename)
    # Define the color and font for the bounding box
    color = (0, 255, 0)  # green
    font = cv.FONT_HERSHEY_SIMPLEX
    for_bounding_box= cv.cvtColor(image_np, 3)

    # Draw the bounding box with class name and confidence
    cv.rectangle(for_bounding_box, (6, 6), (90, 90), color, thickness=2)
    cv.putText(for_bounding_box , prediction_label, (10, 80 - 10), font, fontScale=0.5, color=color, thickness=1)
    cv.imwrite(output_path, for_bounding_box)
    return prediction_label, confidence

