import cv2
import numpy as np
import serial
import Function_Library as fl
# Serial communication setup
# ser = serial.Serial('/dev/ttyACM0', 9600)
arduino_port = 'COM3'

ser = fl.libARDUINO()

comm = ser.init(arduino_port, 9600)

def process_frame(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # Detect edges using Canny
    edges = cv2.Canny(blur, 50, 150)

    # Define a region of interest (ROI)
    height, width = edges.shape
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (0, height * 1 / 2),
        (width, height * 1 / 2),
        (width, height),
        (0, height),
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    cropped_edges = cv2.bitwise_and(edges, mask)

    # Detect lines using Hough transform
    lines = cv2.HoughLinesP(cropped_edges, 1, np.pi / 180, 50, maxLineGap=20)

    return lines


def display_lines(frame, lines):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    combined_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return combined_image


def send_command(command):
    comm.write(command.encode())


cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    lines = process_frame(frame)
    line_image = display_lines(frame, lines)

    cv2.imshow('Line Tracking', line_image)

    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                # Calculate the slope of the line
                slope = (y2 - y1) / (x2 - x1)
                print(slope)
                if slope < -0.5:
                    send_command('R')  # Turn left
                elif slope > 0.5:
                    send_command('L')  # Turn right
                else:
                    send_command('F')  # Move forward

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

send_command('S')  # Ensure the car stops if the program ends
cap.release()
cv2.destroyAllWindows()
