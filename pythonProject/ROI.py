import os
import cv2
import numpy as np


def apply_roi(image, polygon):
    mask = np.zeros_like(image)
    vertices = np.array([polygon], dtype=np.int32)
    cv2.fillPoly(mask, vertices, (255, 255, 255))  # ROI 부분을 흰색으로 채우기
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image


def color_filter(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    filtered_image = cv2.bitwise_and(image, image, mask=mask)
    return filtered_image


def hough_transform(image, polygon):
    # Apply ROI
    roi_image = apply_roi(image, polygon)

    # Color filtering
    filtered_image = color_filter(roi_image)

    # Preprocess for line detection
    resized_image = cv2.resize(filtered_image, (filtered_image.shape[1] // 2, filtered_image.shape[0] // 2))
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Hough 변환을 사용하여 직선을 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # 검출된 직선을 이미지에 그림
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return resized_image


def hough_main():
    dataset_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Downloads"))
    image_files = ["steering_4.jpg"]
    polygon = [(12, 718), (718, 705), (582, 389), (103, 414)]

    for image_file in image_files:
        image_path = os.path.join(dataset_directory, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error: Could not open or find the image {image_file}.")
            continue

        result_image = hough_transform(image, polygon)

        cv2.imshow("Detected Lines - " + image_file, result_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    hough_main()
