import os
import sys
import cv2
import numpy as np
           
def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def hough_transform(image, polygon):
    resized_image = cv2.resize(image, (image.shape[1] // 2, image.shape[0] // 2))
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    # Hough 변환을 사용하여 직선을 검출
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # 다각형 내부에 있는 세로선들만 그리기
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # 직선의 기울기 계산
            if x2 - x1 != 0:
                slope = abs((y2 - y1) / (x2 - x1))
            else:
                slope = float('inf')  # 기울기가 무한대인 경우 (수직선)

            # 기울기를 이용하여 세로선 여부 판별 (수평선 제외)
            if slope > 0.5:  # 기울기가 수평에 가까운 경우 (세로선)
                mid_point = ((x1 + x2) // 2, (y1 + y2) // 2)

                # 중점이 다각형 내부에 있는지 확인
                if point_in_polygon(mid_point, polygon):
                    cv2.line(resized_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return resized_image


def hough_main():
    dataset_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../Downloads"))
    image_files = ["steering_4.jpg"]
    polygon = [(12, 718), (718, 705), (582, 389), (103, 414)]
    # point = point_in_polygon((12,718), polygon)
    # print(point)
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

