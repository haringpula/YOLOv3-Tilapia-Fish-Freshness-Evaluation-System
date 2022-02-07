from tkinter import *
from tkinter import filedialog
from datetime import date
from PIL import Image, ImageTk
from tkinter import messagebox
import argparse
import numpy as np
import os
import cv2

root = Tk()
root.title("Tilapia Freshness Evaluator")
root.geometry("1366x768")


def selected():
    global img_path, img
    img_path = filedialog.askopenfilename(initialdir=os.getcwd())

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--image", default=img_path, help="image for prediction")
    parser.add_argument("--config", default='data/yolov3_tilapia.cfg', help="YOLO config path")
    parser.add_argument("--weights", default='data/yolov3_tilapia_last.weights', help="YOLO weights path")
    parser.add_argument("--names", default='data/obj.names', help="class names path")
    args = parser.parse_args()

    lbl_freshnes.config(text="<<FRESHNESS ANALYSIS>>", font=("Helvetica", 18))
    average_rgb.config(text="<<AVERAGE COLOR RGB>>", font=("Helvetica", 18))

    CONF_THRESH, NMS_THRESH = 0.5, 0.5

    # Load the network
    net = cv2.dnn.readNetFromDarknet(args.config, args.weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # Get the output layer from YOLO
    layers = net.getLayerNames()
    output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Read and convert the image to blob and perform forward pass to get the bounding boxes with their confidence scores
    img = cv2.imread(args.image)
    height, width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_outputs = net.forward(output_layers)

    class_ids, confidences, b_boxes = [], [], []
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONF_THRESH:
                center_x, center_y, w, h = (
                        detection[0:4] * np.array([width, height, width, height])).astype('int')

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                b_boxes.append([x, y, int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    # Perform non maximum suppression for the bounding boxes to filter overlapping and low confident bounding boxes
    indices = cv2.dnn.NMSBoxes(b_boxes, confidences, CONF_THRESH, NMS_THRESH).flatten().tolist()

    # Draw the filtered bounding boxes with their class to the image
    with open(args.names, "r") as f:
        classes = [line.strip() for line in f.readlines()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    for index in indices:
        x, y, w, h = b_boxes[index]
        cv2.rectangle(img, (x, y), (x + w, y + h), colors[index], 2)
        cv2.putText(img, classes[class_ids[index]], (x + 5, y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, colors[index],
                    2)

    # Create and write the bounding box coordinates to a .txt file
    txt = open("outputs/coordinates.txt", "w")
    coordinates = " ".join(str(i) for i in b_boxes[0])
    txt.write(coordinates)

    cv2.imwrite("outputs/prediction.jpg", img)

    img = Image.open("outputs/prediction.jpg")
    img.thumbnail((600, 600))
    fish_image = ImageTk.PhotoImage(img)
    canvas2.create_image(660, 210, image=fish_image)
    canvas2.image = fish_image


def grabcut():
    global freshness
    try:
        image = cv2.imread(img_path)
        messagebox.showinfo(title="GrabCut", message="Performing Background Subtraction, it may take a moment.\nPress OK to continue")

        with open('outputs/coordinates.txt', 'r') as file:
            fp = file.read()
        coord = fp.split()
        rectangle = (int(coord[0]), int(coord[1]), int(coord[2]), int(coord[3]))
        # Image cropping
        cropped = image[rectangle[1]:rectangle[1] + rectangle[3], rectangle[0]:rectangle[0] + rectangle[2]]
        cv2.imwrite("outputs/grabcut.png", cropped)
        size=cropped.shape
        print(size[0],size[1])
        box = (1,1,(size[1]-2),(size[0]-2))

        black_mask = np.zeros(cropped.shape[:2], np.uint8)
        background = np.zeros((1, 65), np.float64)
        foreground = np.zeros((1, 65), np.float64)

        # GrabCut Extraction
        cv2.grabCut(cropped, black_mask, box, background, foreground, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((black_mask == 2) | (
                black_mask == 0), 0, 1).astype('uint8')

        
        cropped = cropped * mask2[:, :, np.newaxis]

        # Turn image into transparent
        tmp = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
        cv2.imwrite("outputs/mask.png", alpha)
        b, g, r = cv2.split(cropped)
        rgba = [b, g, r, alpha]
        dst = cv2.merge(rgba, 4)
        cv2.imwrite("outputs/segmented.png", dst)

        # Color channel average
        #avgR = round(np.mean(dst[:, :, 2]))
        #avgG = round(np.mean(dst[:, :, 1]))
        #avgB = round(np.mean(dst[:, :, 0]))

        clrd = cv2.imread("outputs\segmented.png")
        mskd = cv2.imread("outputs\mask.png")
        py= clrd.shape[0]
        px= clrd.shape[1]
        count=0
        ar=0
        ag=0
        ab=0

        for y in range(0,py):
            for x in range(0,px):
                if mskd[y,x,2] == 255 and mskd[y,x,1] == 255 and mskd[y,x,0] == 255:
                    count=count+1
                    cr = clrd[y,x,2]
                    cg = clrd[y,x,1]
                    cb = clrd[y,x,0]
                    ar=ar+cr
                    ag=ag+cg
                    ab=ab+cb

        avgR=round(ar/count)
        avgG=round(ag/count)
        avgB=round(ab/count)

        RSQ = (avgR - 32) * (avgR - 32)
        GSQ = (avgG - 19) * (avgG - 19)
        BSQ = (avgB - 17) * (avgB - 17)

        distance = np.sqrt(RSQ + GSQ + BSQ)
        print(distance)

        if distance < 84 :
            if avgB > 62 and avgG > 54:
                freshness = "Not Fresh"
            else:
                freshness = "Fresh"
        elif distance >= 84 and distance < 144:
            if avgB < 76 and avgG < 68:
                freshness = "Fresh"
            elif avgB > 121 and avgG > 118:
                freshness = "Old"
            else:
                freshness = "Not Fresh"
        elif distance >= 144:
            if avgB < 80 and avgG < 76:
                freshness = "Not Fresh"
            else:
                freshness = "Old"

        # Get image name    
        img_name = img_path.split('/')[-1]

        # Get current date
        today = date.today()

        # cv2.imwrite("test.png", dst) #Export non cropped
        grabcut_image = Image.open("outputs/segmented.png")
        img.thumbnail((600, 600))
        mask_image = ImageTk.PhotoImage(grabcut_image)
        canvas2.create_image(660, 210, image=mask_image)
        canvas2.image = mask_image

        freshness_analysis = "FRESHNESS ANALYSIS: {}".format(freshness)
        rgb_channels = "AVERAGE COLOR RGB: {} {} {}".format(avgR, avgG, avgB)
        lbl_freshnes.config(text=freshness_analysis, font=("Helvetica", 18))
        average_rgb.config(text=rgb_channels, font=("Helvetica", 18))

        success_box = "{}\n{}".format(freshness_analysis, rgb_channels)
        messagebox.showinfo(title="GrabCut", message=success_box)

        file = open("outputs/logs.txt", "a")
        log = "{}\t{}\t\t{}\n".format(today, img_name, freshness)
        file.write(log)
        file.close()


    except:
        messagebox.showwarning(
            title="GrabCut", message="Image path not defiend")


fish_image = None

# create canvas to display image
canvas2 = Canvas(root, width="1320", height="420", relief=RIDGE, bd=2)
canvas2.place(x=15, y=10)

# freshness analyis
lbl_freshnes = Label(root, text="<<FRESHNESS ANALYSIS>>", font=("Helvetica", 18))
lbl_freshnes.place(x=60, y=480)

# average rgb channels
average_rgb = Label(root, text="<<AVERAGE COLOR RGB>>", font=("Helvetica", 18))
average_rgb.place(x=60, y=520)

# create buttons
btn_yolov3 = Button(root, text="Select Image", font='ariel 15 bold', relief=GROOVE, command=selected)
btn_yolov3.place(x=60, y=570)
btn2 = Button(root, text="Start", width=12, font='ariel 15 bold', relief=GROOVE, command=grabcut)
btn2.place(x=240, y=570)

root.mainloop()
