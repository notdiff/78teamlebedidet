from ultralytics import YOLO
from PIL import Image
from numpy import asarray
import cv2
import numpy as np

num = 0

model = YOLO('best.pt')
k = {0: "кликун", 1: "малый", 2: "шипун"}

def gen(path):
    image = Image.open(path)
    image = image.convert('RGB')
    image = asarray(image)

    res = model.predict(image)

    class_c = {
        0: 0.,
        1: 0.,
        2: 0.
    }
    for i, clas in enumerate(res[0].boxes.cls):
        clas = int(clas)

        class_c[clas] += res[0].boxes.conf[i]

    max_key = max(class_c, key=class_c.get)

    image = cv2.imread(path)

    boxes_list = np.array(res[0].boxes.boxes.cpu()).tolist()

    for _ in boxes_list:
        xmin, ymin, xmax, ymax, pro, cl = _[0], _[1], _[2], _[3], _[4], _[5]
        cv2.rectangle(image, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)

    # boxed_img = visualize_yolo_res(image, np.array(res[0].boxes.boxes.cpu()).tolist())
    global num
    new_path = 'images/'+str(num)+".png"
    num += 1

    image = Image.fromarray(image[:, :, ::-1])
    image.save(new_path)

    return [new_path, "Обнаруженно "+ str(len(res[0].boxes.cls))+" особей \nподвида " + str(k[max_key]) + "." ]

    # print( "Количество особей: "+str((res[0].boxes.cls)) )
    # print(res[0].boxes.boxes)
