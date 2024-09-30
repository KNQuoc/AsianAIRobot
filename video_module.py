import cv2
import numpy as np

# Load the MobileNet SSD model
net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'mobilenet_iter_73000.caffemodel')

def detect_people(frame):
    height, width = frame.shape[:2]

    # Preprocess the input image
    blob = cv2.dnn.imageBlob(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    
    # Perform detection
    detections = net.forward()

    people_boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.5:  # Confidence threshold
            idx = int(detections[0, 0, i, 1])

            # Only consider class 15 (person class in COCO)
            if idx == 15:
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (x, y, w, h) = box.astype("int")
                people_boxes.append([x, y, w - x, h - y])

    return people_boxes

def display_frame_with_count(frame, people_boxes):
    for (x, y, w, h) in people_boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, "People Count: " + str(len(people_boxes)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow('frame', frame)

def run_webcam_detection():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Detect people using SSD
        people_boxes = detect_people(frame)

        # Display frame with people count and bounding boxes
        display_frame_with_count(frame, people_boxes)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_detection()
