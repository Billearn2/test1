import Function_Library as fl
import start_lib as st
import straight_lib as straight
import cv2
EPOCH = 500000
polygon = [(312, 229), (5, 231), (53, 96), (224, 95)]
if __name__ == "__main__":
    # Exercise Environment Setting
    env = fl.libCAMERA()

    """ Exercise 1: RGB Color Value Extracting """
    ############## YOU MUST EDIT ONLY HERE ##############
    # example = env.file_read("./Example Image.jpg")  #image 경로를 설정해야 함
    # R, G, B = env.extract_rgb(example, print_enable=True)
    # quit()
    #####################################################

    # Camera Initial Setting
    ch0, ch1 = env.initial_setting(capnum=2)

    # Camera Reading..
    for i in range(EPOCH):
        _, frame0, _, frame1 = env.camera_read(ch0, ch1)

        """ Exercise 2: Webcam Real-time Reading """
        ############## YOU MUST EDIT ONLY HERE ##############
        # env.image_show(frame0, frame1)
        #####################################################

        # point = st.get_points(frame0)
        # print(point)
        result_img = straight.hough_transform(frame0, polygon)
        # print(result_img)
        cv2.imshow("frame0", result_img)
        # st.get_bird_eye_view(frame0,(600,800),point)
        # print(straight.point_in_polygon(point,polygon=[(314, 233), (9, 230), (62, 85), (205, 93)]))
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
