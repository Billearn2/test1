
import Function_Library as fl
import BridEyeView as bev
import cv2
EPOCH = 500000

if __name__ == "__main__":

    _init = True
    _scale_percent = 50

    # Exercise Environment Setting
    env = fl.libCAMERA()
    bev_converter = bev.libBirdEyeView(_init, _scale_percent)


    """ Exercise 1: RGB Color Value Extracting """
    ############## YOU MUST EDIT ONLY HERE ##############
    # example = env.file_read("./Example Image.jpg")
    # R, G, B = env.extract_rgb(example, print_enable=True)
    # quit()
    #####################################################

    # Camera Initial Setting
    ch0, ch1 = env.initial_setting(capnum=2)

    # Camera Reading..
    for i in range(EPOCH):
        _, frame0, _, frame1 = env.camera_read(ch0, ch1)
        cv2.imshow(frame0)

        if _init:

            _points0 = bev_converter.get_points(frame0)
            _points1 = bev_converter.get_points(frame1)
            _init = False

        resized_img0 = bev_converter.resize_image(frame0)
        resized_img1 = bev_converter.resize_image(frame1)
        # cv2.imshow(frame0)
        # cv2.imshow(frame1)
        
        img0 = get_bird_eye_view(resized_img0, (resized_img0.shape[1], resized_img0.shape[0]), _points0)
        img1 = get_bird_eye_view(resized_img1, (resized_img1.shape[1], resized_img1.shape[0]), _points1)

        """ Exercise 2: Webcam Real-time Reading """
        ############## YOU MUST EDIT ONLY HERE ##############
        env.image_show(frame0, frame1)
        env.image_show(img0, img1)
        #####################################################

        """ Exercise 3: Object Detection (Traffic Light Circle) """
        #################### YOU MUST EDIT ONLY HERE ####################
        # color = env.object_detection(frame0, sample=16, print_enable=True)
        #################################################################

        """ Exercise 4: Specific Edge Detection (Traffic Line) """
        #################### YOU MUST EDIT ONLY HERE ####################
        # direction = env.edge_detection(frame0, width=500, height=120,
        #                                gap=40, threshold=150, print_enable=True)
        #################################################################

        # Process Termination (If you input the 'q', camera scanning is ended.)
        if env.loop_break():
            break