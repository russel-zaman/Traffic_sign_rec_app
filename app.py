# web-app for API image manipulation

from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    jsonify,
    make_response,
    send_file,
    Response,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
import os
from PIL import Image


from time import time
import json
from utils.utils import decodeImage
from cnn_predict import traffic
from lenet import sign_predict
import io

# yolov5
import cv2
import numpy as np
from yolov5.yolo_predict import entry
import pandas as pd
import csv

app = Flask(__name__)
# SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = "secret"
app.config["TEMP_UPLOAD_FOLDER"] = "static/yolo_predetection_temp"
app.config["YOLO_DETECTED_FOLDER"] = "static/yolo_detect"
app.config["LENET_DETECTED_FOLDER"] = "static/lenet_detect"
app.config["CNN_DETECTED_FOLDER"] = "static/cnn_detect"
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = "internet_uploads"
STATIC_FOLDER = "static"


class StatsForm(FlaskForm):
    start_button = SubmitField()
    upload_button = SubmitField()


# default access page
@app.route("/")
def main():
    return render_template("home.html")


##cnn training data report
@app.route("/get_cnn_report")
def get_cnn_report():
    df = pd.read_csv("static/table/cnn/cnn_classification_report.csv")
    # Rename the 'Unnamed: 0' column to an empty string
    df = df.rename(columns={"Unnamed: 0": ""})
    cnn_table = df.to_html(index=False)
    # assign id to the generated table
    cnn_table = cnn_table.replace("<table", '<table id="cnn_class_report"')
    return jsonify({"cnn_table": cnn_table})


@app.route("/get_lenet_report")
def get_lenet_report():
    df = pd.read_csv("static/table/lenet/lenet_classification_report.csv")
    # Rename the 'Unnamed: 0' column to an empty string
    df = df.rename(columns={"Unnamed: 0": ""})
    lenet_table = df.to_html(index=False)
    # assign id to the generated table
    lenet_table = lenet_table.replace("<table", '<table id="lenet_class_report"')
    return jsonify({"lenet_table": lenet_table})


##recall
@app.route("/get_recall_report")
def get_recall_report():
    cnn = pd.read_csv("static/table/cnn/cnn_classification_report.csv")
    cnn = cnn.rename(columns={"Unnamed: 0": ""})
    cnn = cnn.reset_index(drop=True)

    lenet = pd.read_csv("static/table/lenet/lenet_classification_report.csv")
    lenet = lenet.rename(columns={"Unnamed: 0": ""})
    lenet = lenet.reset_index(drop=True)

    yolo = pd.read_csv("static/table/yolov5/yolov5_classification_report.csv")
    yolo = yolo.rename(columns={"Unnamed: 0": ""})
    yolo = yolo.reset_index(drop=True)

    recall = pd.concat([cnn.iloc[:, 2], lenet.iloc[:, 2], yolo.iloc[:, 2]], axis=1)
    recall.columns = ["VGG Net Model", "Lenet5 Model", "Yolov5 Model"]

    recall_table = pd.DataFrame(recall).to_html(index=True)

    recall_table = recall_table.replace("<table", '<table id="recall_table"')
    return jsonify({"recall_table": recall_table})


##precision table
@app.route("/get_precision_report")
def get_precision_report():
    cnn = pd.read_csv("static/table/cnn/cnn_classification_report.csv")
    cnn = cnn.rename(columns={"Unnamed: 0": ""})
    cnn = cnn.reset_index(drop=True)

    lenet = pd.read_csv("static/table/lenet/lenet_classification_report.csv")
    lenet = lenet.rename(columns={"Unnamed: 0": ""})
    lenet = lenet.reset_index(drop=True)

    yolo = pd.read_csv("static/table/yolov5/yolov5_classification_report.csv")
    yolo = yolo.rename(columns={"Unnamed: 0": ""})
    yolo = yolo.reset_index(drop=True)

    precision = pd.concat([cnn.iloc[:, 1], lenet.iloc[:, 1], yolo.iloc[:, 1]], axis=1)
    precision.columns = ["VGG Net Model", "Lenet5 Model", "Yolov5 Model"]

    precision_table = pd.DataFrame(precision).to_html(index=True)
    precision_table = precision_table.replace("<table", '<table id="precision_table"')
    return jsonify({"precision_table": precision_table})


@app.route("/recognition", methods=["POST", "GET"])  #
def recognition():
    imageData = request.form
    # imageFile=imageData.get("i_file")
    imageFile = request.files["i_file"]
    imageFileName = imageData["i_filename"]
    selected_algorithm = request.form["dropdown"]
    print(imageFileName)
    print(selected_algorithm)
    imageFile.save(os.path.join(app.config["TEMP_UPLOAD_FOLDER"], imageFileName))

    # with open(imageName, "wb") as f:
    #     f.write(imageFile)
    # print(imageData["i_filename"])
    if selected_algorithm == "yolo":
        yolo = yolo_detection_result(imageFileName)
        print("in recognition function")
        print(yolo)

        new_filename = (
            os.path.splitext(
                os.path.join(app.config["YOLO_DETECTED_FOLDER"], imageFileName)
            )[0]
            + ".jpg"
        )
        processed_image_file = new_filename
        # return send_file(processed_image_file, mimetype='image/jpeg')
        # Return a JSON response with the detection result and the image URL
        return jsonify({"result": yolo, "image_url": new_filename})
    elif selected_algorithm == "cnn":
        print("cnn was selected")
        cnn = detection_result(imageFileName)

        new_filename = (
            os.path.splitext(
                os.path.join(app.config["CNN_DETECTED_FOLDER"], imageFileName)
            )[0]
            + ".jpg"
        )
        processed_image_file = new_filename
        # return send_file(processed_image_file, mimetype='image/jpeg')
        # Return a JSON response with the detection result and the image URL
        return jsonify({"result": cnn, "image_url": new_filename})
    elif selected_algorithm == "lenet":
        print("lenet was selected")
        lenet = lenet_detection_result(imageFileName)
        new_filename = (
            os.path.splitext(
                os.path.join(app.config["LENET_DETECTED_FOLDER"], imageFileName)
            )[0]
            + ".jpg"
        )

        # Return a JSON response with the detection result and the image URL
        return jsonify({"result": lenet, "image_url": new_filename})


@app.route("/image/<path:path>", methods=["GET"])
def get_image(path):
    # This endpoint serves the image based on the URL returned from the previous endpoint
    return send_file(path)


def load_model_performance(model):
    with open("scores.json", "r") as d:
        scores = json.load(d)
    plot = "/images/plot.png"
    return scores, plot


def lenet_detection_result(imageFileName):
    filepath = os.path.join(app.config["TEMP_UPLOAD_FOLDER"], imageFileName)
    result, confidence = sign_predict(filepath)
    print(result)
    print(type(result))
    return result


def detection_result(imageFileName):
    # imageFile=imageFileName
    filepath = os.path.join(app.config["TEMP_UPLOAD_FOLDER"], imageFileName)
    print("printing cnn image path")
    print(filepath)
    image_object = traffic(filepath)
    result, confidence = image_object.trafficsign()
    print(result)
    return result


def yolo_detection_result(imageFileName):

    imageFileName = imageFileName
    filepath = os.path.join(app.config["TEMP_UPLOAD_FOLDER"], imageFileName)

    # img = Image.open(io.BytesIO(imageFile))
    obj_entry = entry()
    weights = "yolov5_model/best.pt"
    imgsz = (416, 416)
    conf = 0.4
    # source="test.jpg"
    source = filepath
    # source = "/home/ngsharna/vai_code/apps/yolov5/test/stop_sign.jpg"
    project = "static/yolo_detect"
    save_txt = True
    result = obj_entry.entry_point(weights, source, imgsz, project, save_txt)
    print(result)
    return result


if __name__ == "__main__":
    app.run()
