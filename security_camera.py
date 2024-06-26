# This is a short script that uses a Raspberry Pi Model 4B, Raspberry Pi Camera v2, Elegoo Big Sound Sensor, and Google Coral AI USB Accelerator
# to detect the noise level and amount of people that are currently in a room. This was designed for the UIRP hackathon.

import os.path
from aiymakerkit import vision
from aiymakerkit import utils
from pycoral.adapters.detect import BBox
from pycoral.utils.dataset import read_label_file
from time import sleep
import datetime
import RPi.GPIO as gpio
import requests
import jsonify


# BGR (not RGB) colors
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

#GPIO setup for sound sensor
digital_in = 40
gpio.setmode(gpio.BOARD)
gpio.setup(digital_in, gpio.IN)


#function to find path to this script
def path(name):
    """ Creates an absolute path to a file in the same directory as this script."""
    root = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(root, name)


# Load the TensorFlow Lite model (compiled for the Edge TPU)
OBJECT_DETECTION_MODEL = path('ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite')
detector = vision.Detector(OBJECT_DETECTION_MODEL)
labels = utils.read_labels_from_metadata(OBJECT_DETECTION_MODEL)


#count people function
def count_people():
    frame_counter = 0
    max_occupancy = 0
    # Run a loop to get images and process them in real-time
    for frame in vision.get_frames():
        frame_counter += 1
    # Detect only objects with at least 50% confidence
        objects = detector.get_objects(frame, threshold=0.5)
        if frame_counter >= 60:
            break
    # Review all detected objects and check for
    # objects that look like a person (ignore the rest)
        people_count = 0
        for obj in objects:
            label = labels.get(obj.id)
            if 'person' in label:
            # Get the number of people in the current frame
                people_count += 1
                person_area = obj.bbox.area
                vision.draw_rect(frame, obj.bbox, color=GREEN)
        # find the maximum number of people in all frames provided
        if people_count > max_occupancy:
            max_occupancy = people_count
    return max_occupancy 


#noise level detection function
def sound_check():
    count = 0
    is_loud = False
    while count <= 20:
        sleep(0.25)
        count += 1
        if gpio.input(digital_in) == 1:
            is_loud = True
    return is_loud

#send payload function
def send_payload(noise, count, url):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    data ={
    "node_id":1,
    "timestamp":timestamp,
    "noise":noise,
    "count":count
    }
    response = requests.post(url+'/add', headers={'Content-Type': 'application/json'}, json=data)
    print(response)
    return

#main
def main():
    url = "http://192.168.71.126:5050"
    is_loud = sound_check()
    current_occupancy = count_people()
    send_payload(is_loud, current_occupancy, url)
    return

if __name__ == "__main__":
    main()