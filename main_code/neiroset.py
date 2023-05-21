from ultralytics import YOLO
from PIL import Image
from numpy import asarray
import cv2
import numpy as np
from transformers import ViTFeatureExtractor, ViTForImageClassification
from hugsvision.inference.VisionClassifierInference import VisionClassifierInference

hugs_path = "trainer/"
hugs_model = VisionClassifierInference(
    feature_extractor = ViTFeatureExtractor.from_pretrained(hugs_path),
    model = ViTForImageClassification.from_pretrained(hugs_path),
)

classes = {
    'mal': 0,
    'skikun': 1,
    'ship': 2
}

num = 0

yolo_model = YOLO('best.pt')
k = {1: "кликун", 0: "малый", 2: "шипун"}

def gen(path):
    ####################
    # YOLO PREDICTION DOWN
    ###################
    image = Image.open(path)
    image = image.convert('RGB')
    image = asarray(image)

    res = yolo_model.predict(image)

    class_c = {
        0: 0.,
        1: 0.,
        2: 0.
    }

    for i, clas in enumerate(res[0].boxes.cls):
        clas = int(clas)

        class_c[clas] += float(res[0].boxes.conf[i].item())

    yolo_class = max(class_c, key=class_c.get)
    # average conf
    yolo_conf = class_c[yolo_class] / len(res[0].boxes.cls)
    ###################
    # YOLO PRED UP
    ###################

    ###################
    # HUGS PRED DOWN
    ###################
    hugs_class = hugs_model.predict(img_path=path)
    hugs_class = classes[hugs_class]
    ###################
    # HUGS PRED UP
    ###################

    final_pred = 0
    if yolo_class != hugs_class:
        if yolo_conf >= 0.5:
            final_pred = yolo_class
        else:
            final_pred = hugs_class
    else:
        final_pred = yolo_class

    print(f'Yolo class {yolo_class}, yolo conf {yolo_conf}, Hugs class {hugs_class}')

    image = cv2.imread(path)

    boxes_list = np.array(res[0].boxes.boxes.cpu()).tolist()

    for _ in boxes_list:
        xmin, ymin, xmax, ymax, pro, cl = _[0], _[1], _[2], _[3], _[4], _[5]
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)

    global num
    new_path = 'images/'+str(num)+".png"
    num += 1

    image = Image.fromarray(image[:, :, ::-1])
    image.save(new_path)

    return [new_path, "Обнаруженно "+ str(len(res[0].boxes.cls))+" особей \nподвида " + str(k[final_pred]) + "." ]

