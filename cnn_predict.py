import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
import os

class traffic:
    def __init__(self,filename):
        self.filename =filename 

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


    
    def trafficsign(self):
        #get the class
        labels_dict=self.labels_dict

        model_path = "CNN_kaggle_saved_model_and_history/CNN_kaggle_50epoch.h5"
        loaded_model = tf.keras.models.load_model(model_path)

        imagename = self.filename
        image = cv2.imread(imagename)
        #arr = np.asarray(bytearray("static/yolo_predetection_temp/stop_sign.jpg".encode("utf-8")), dtype=np.uint8)

        #arr = np.asarray(bytearray(imagename), dtype=np.uint8)
        #image = cv2.imdecode(arr, -1) 

        image_fromarray = Image.fromarray(image, 'RGB')
        resize_image = image_fromarray.resize((32, 32))
        expand_input = np.expand_dims(resize_image,axis=0)
        input_data = np.array(expand_input)
        input_data = input_data/255
        pred = loaded_model.predict(input_data)
        ##result = pred.argmax()
        prediction_max = np.argmax(pred)
        prediction_label = labels_dict[prediction_max]
        confidence = np.max(pred)

        #get the original filename from the provided path
        dirname, filename = os.path.split(imagename)
        print("now print the file name")
        print(filename)
        print("now print prediction")
        print(prediction_label)
        #define output directory
        output_dir = 'static/cnn_detect'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_path = os.path.join(output_dir, filename)
        # Define the color and font for the bounding box
        color = (0, 255, 0)  # green
        font = cv2.FONT_HERSHEY_SIMPLEX
        for_bounding_box= image

        # Draw the bounding box with class name and confidence
        cv2.rectangle(for_bounding_box, (6, 6), (90, 90), color, thickness=2)
        cv2.putText(for_bounding_box , prediction_label, (10, 80 - 10), font, fontScale=0.5, color=color, thickness=1)
        cv2.imwrite(output_path, for_bounding_box)
        return prediction_label, confidence
