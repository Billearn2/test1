import cv2

def check_camera_indices():
    index = 0
    arr = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            arr.append(index)
        cap.release()
        index += 1
    return arr

camera_indices = check_camera_indices()
print("Available camera indices:", camera_indices)