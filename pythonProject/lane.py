import Function_Library as fl

arduino_port = 'COM8'

ser = fl.libARDUINO()

comm = ser.init(arduino_port, 9600)

EPOCH = 500000

if __name__ == "__main__":
    # Exercise Environment Setting
    env = fl.libCAMERA()

    ch0, ch1 = env.initial_setting(capnum=2)

    for i in range(EPOCH):
        _, frame0, _, frame1 = env.camera_read(ch0, ch1)

        direction = env.edge_detection(frame0, width=500, height=120,
                                       gap=40, threshold=100, print_enable=True)
        # print(direction)

        if direction == 0:  #forward
           input_value = 0
           comm.write(input_value)
        elif direction == 2:    #right
           input_value = 2
           comm.write(input_value)
        elif direction == 1:    #left
           input_value = 1
           comm.write(input_value)
        else:
            input_value = 0
            comm.write(input_value)

        if env.loop_break():
            break


# while True:
#     input_value = input('아두이노로 전송할 저항 값(0~255): ')


    # comm.write(input_value.encode())

    # if input_value == 'q':
    #     break