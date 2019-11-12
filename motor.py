import time
import config
import RPi.GPIO as GPIO  # pylint: disable=import-error,no-name-in-module


def setup_motors():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config.RL1, GPIO.OUT)
    GPIO.setup(config.RL2, GPIO.OUT)
    GPIO.setup(config.RL3, GPIO.OUT)
    GPIO.setup(config.RL4, GPIO.OUT)
    GPIO.setup(config.ena, GPIO.OUT)
    GPIO.setup(config.enb, GPIO.OUT)
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.LOW)
    global pa
    pa = GPIO.PWM(config.ena, 1000)
    global pb
    pb = GPIO.PWM(config.enb, 1000)
    pb.start(60)
    pa.start(50)


def start_fw():
    GPIO.output(config.RL1, GPIO.HIGH)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.HIGH)
    GPIO.output(config.RL4, GPIO.LOW)
    pa.ChangeDutyCycle(50)
    pb.ChangeDutyCycle(60)


def start_bw():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.HIGH)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.HIGH)
    pa.ChangeDutyCycle(50)
    pb.ChangeDutyCycle(60)


def start_left():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.HIGH)
    GPIO.output(config.RL3, GPIO.HIGH)
    GPIO.output(config.RL4, GPIO.LOW)
    pa.ChangeDutyCycle(90)
    pb.ChangeDutyCycle(90)


def start_right():
    GPIO.output(config.RL1, GPIO.HIGH)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.HIGH)
    pa.ChangeDutyCycle(90)
    pb.ChangeDutyCycle(90)


def stop():
    GPIO.output(config.RL1, GPIO.LOW)
    GPIO.output(config.RL2, GPIO.LOW)
    GPIO.output(config.RL3, GPIO.LOW)
    GPIO.output(config.RL4, GPIO.LOW)


def drive(direction, duration):
    setup_motors()
    if direction in ['F', 'FORWARD', 0]:
        start_fw()
    elif direction in ['B', 'BACKWARD', 1]:
        start_bw()
    elif direction in ["L", "LEFT", 2]:
        start_left()
    elif direction in ["R", "RIGHT", 3]:
        start_right()
    time.sleep(duration)
    stop()


def menu():
    try:
        main_menu = ['q to quit',
                     'f to go FW',
                     'b to go BW',
                     'l to turn left',
                     'r to turn right',
                     's to stop']
        setup_motor()
        while True:
            print("\tMOTOR TEST MENU")
            print("enter direction and duration (optional)")
            for option in main_menu:
                print(option)
            print("Example:f (start going fw), f 2 (go fw for 2 sec), l 0.5 (turn left for 0.5 sec), s (stop moving) etc. ")

            choice = input()
            try:
                direction, duration = choice.split()
                duration = float(duration)
                drive(direction, duration)
            except ValueError:
                if choice == 'q':
                    return
                elif choice == 'f':
                    start_fw()
                elif choice == 'b':
                    start_bw()
                elif choice == 'l':
                    start_left()
                elif choice == 'r':
                    start_right()
                elif choice == 's':
                    stop()
    finally:
        GPIO.cleanup()
    return


if __name__ == "__main__":
    menu()
