import subprocess
import requests
from flask import (
    Flask,
    make_response,
    jsonify,
    request,
    send_file,
    send_from_directory,
    abort,
)
from flask_cors import CORS
from io import BytesIO
import base64
import sys
import os
import time
import argparse
from PIL import Image

app = Flask(__name__)
CORS(app)


def response_body(status, data):
    status = int(status)
    if status == 0:
        status = "error"
    if status == 1:
        status = "success"

    response_body_json = {
        "status": status,
        "data": data
    }
    res = make_response(jsonify(response_body_json), 200)
    return res


def base64_to_cv(data_source):
    data_source = data_source.split(",")[-1]
    data_source = base64.b64decode(data_source)
    data_source = np.fromstring(data_source, dtype=np.uint8)
    print(data_source)
    # img = cv2.imdecode(data_source, 1)
    return img


def base64_to_file(data_input):
    data_input = data_input.split(",")[-1]
    img = Image.open(BytesIO(base64.b64decode(data_input)))
    time_now = str(time.time())
    source = "input/"+time_now+".jpg"

    img = img.save(source)
    return source


def np_to_base64(data):
    im = Image.fromarray(data)
    buff = BytesIO()
    im.save(buff, format="JPEG")
    mask_base64 = base64.b64encode(buff.getvalue()).decode("utf-8")

    return mask_base64


@app.route("/cv015", methods=['POST'])
def cv014_api():
    # get data from user
    try:
        body_req = request.get_json(force=True)
        input_source = body_req["input_source"]
    except Exception as error:
        error = str(error)
        print(error)
        return response_body(status=0, data=error)

    try:
        source = base64_to_file(input_source)
    except Exception as error:
        error = str(error)
        print(error)
        return response_body(status=0, data=error)

    try:
        string_command_line = "./darknet detector test cfg/coco.data cfg/yolov4-tiny.cfg yolov4-tiny.weights " + \
            source+" -dont_show -ext_output "
        output = subprocess.check_output(string_command_line, shell=True)
        print("start =======")
        output = output.decode().split("\n")

        result = []

        for i in output:
            data_detect = {
                "label": None,
                "score": None,
                "bounding_box": None
            }
            if i.find('%') != -1:
                # print(i.split("\t"))
                i = i.split("\t")

                data_detect.update({
                    "label": i[0].split(":")[0],
                    "score": int(i[0].split(":")[1][:-1])
                })

                aa = i[1].split(" ")
                bb = []
                for j in aa:
                    if len(j) != 0:
                        bb.append(j)
                # print(bb)

                data_detect.update({
                    "bounding_box": {
                        "left_x:": int(bb[1]),
                        "top_y": int(bb[3]),
                        "width": int(bb[5]),
                        "height": int(bb[7][:-1])
                    }})

                result.append(data_detect)

        print("end ========")
        return response_body(status=1, data=result)
    except Exception as error:
        error = str(error)
        print(error)
        return response_body(status=0, data=error)


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5019)
