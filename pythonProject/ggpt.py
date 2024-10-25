import os
import sys
import cv2
import numpy as np
from Function_Library as fl  # Import the libCAMERA class


# Function to calibrate the camera using the selected points
def calibrate_camera(points, output_size):
    height, width = output_size[1], output_size[0]
    src_points = np.float32([points[0], points[1], points[3], points[2]])
    dst_points = np.float32([[0, height], [width, height], [0, 0], [width, 0]])

    matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    return matrix


# Function to get bird's eye view of the image
def get_bird_eye_view(image, matrix, output_size):
    bird_eye_view = cv2.warpPerspective(image, matrix, output_size)
    return bird_eye_view


# Function to collect points from the user
def get_points(image):
    points = []
    mask = None
    is_masking = False

    def mouse_callback(event, x, y, flags, param):
        nonlocal is_masking
        if event == cv2.EVENT_LBUTTONDOWN:
            if not is_masking:
                points.append((x, y))
                print((x, y))

    def update_mask(frame):
        mask.fill(0)
        polygon = np.array([points], np.int32)
        cv2.fillPoly(mask, polygon, (255, 255, 255))
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)
        external_mask = cv2.bitwise_not(mask)
        masked_frame[external_mask == 255] = [0, 0, 0]
        return masked_frame

    def resize_image(img, scale_percent):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    scale_percent = 50
    resized_image = resize_image(image, scale_percent)
    cv2.namedWindow("Webcam")
    cv2.setMouseCallback("Webcam", mouse_callback)

    while True:
        key = cv2.waitKey(1)

        if key & 0xFF == ord('c'):
            points = []
            is_masking = False
            if mask is not None:
                mask.fill(0)
            print("\n")

        if key == 13 and not is_masking:
            if len(points) == 4:
                is_masking = True
                mask = np.zeros(resized_image.shape[:2], dtype=np.uint8)
                update_mask(resized_image)
                print(f"points: {points}")

                output_size = (resized_image.shape[1], resized_image.shape[0])
                matrix = calibrate_camera(points, output_size)
                bev = get_bird_eye_view(resized_image, matrix, output_size)
                cv2.imshow("Bird's Eye View", bev)

                # Use edge_detection for lane detection and direction
                camera = libCAMERA()
                direction = camera.edge_detection(bev, width=50, height=100, gap=10, threshold=100, print_enable=True)
                if direction is not None:
                    print("Vehicle Direction:", direction)
            else:
                print("Please select exactly 4 points.")

        if len(points) > 0 and not is_masking:
            polygon = np.array([points], np.int32)
            cv2.polylines(resized_image, polygon, True, (0, 255, 0), 2)
            for point in points:
                cv2.circle(resized_image, point, 5, (0, 255, 0), -1)

        if is_masking:
            masked_frame = update_mask(resized_image)
            cv2.imshow("Webcam", masked_frame)
        else:
            cv2.imshow("Webcam", resized_image)

        if key & 0xFF == ord('q'):
            print("\nNext Image")
            break

        if key == 27:
            print("\nProgram Exit")
            sys.exit()

    cv2.destroyAllWindows()


# Main function to capture video from webcam and get points from the user
def bev_main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        sys.exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        get_points(frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            print("Quitting...")
            break

    cap.release()
    cv2.destroyAllWindows()

EPOCH = 500000
if __name__ == "__main__":
    env = fl.libCAMERA()

    # Camera Initial Setting
    ch0, ch1 = env.initial_setting(capnum=2)

    # Camera Reading..q
    for i in range(EPOCH):
        _, frame0, _, frame1 = env.camera_read(ch0, ch1)

        point = st.get_points(frame0)

        st.get_bird_eye_view(frame0, (600, 800), point)

        """ Exercise 3: Object Detection (Traffic Light Circle) """
        #################### YOU MUST EDIT ONLY HERE ####################
        # color = env.object_detection(frame0, sample=16, print_enable=True)
        #################################################################

        """ Exercise 4: Specific Edge Detection (Traffic Line) """
        #################### YOU MUST EDIT ONLY HERE ####################
        # direction = env.edge_detection(frame0, width=500, height=120,
        #                                gap=40, threshold=150, print_enable=True)
        # print(direction)
        #################################################################

        # Process Termination (If you input the 'q', camera scanning is ended.)
        if env.loop_break():
            break
    # bev_main()
