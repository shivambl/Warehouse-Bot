# PINOUT VARS
RL1 = 17
RL2 = 18
RL3 = 22
RL4 = 23
ena = 25
enb = 27
TRIGGER = 24
ECHO = 8
# UID OF BOT
UID = "123"
##########################################
# MOTOR VARS
ANGLE_TOLERANCE = 10
DELAY_PER_UNIT = 5
DELAY_PER_ANGLE = 0.0105
# PING SENSOR VARS
MIN_DIST = 15  # in cm
DIST_CHECK_DELAY = 1  # in sec
TIME_TO_DIST_MULTIPLIER = 17150  # to convert time(ms) to dist(cm)
##########################################
# MQTT VARS
MQTT_SERVER = "192.168.43.142"
MQTT_CHANNEL = "rpi/"
MQTT_CHANNEL_GET = MQTT_CHANNEL + "get/"
MQTT_CHANNEL_PUT = MQTT_CHANNEL + "put/"
MQTT_CHANNEL_BARRIER = "block"
# WEBCAM
FRAME_WIDTH = 1024
FRAME_HEIGHT = 768
FPS = 30
USE_QR = False
##########################################
# CONST FOR ANGLE MEASUREMENT
ANGLES = {"FORWARD": 135, "BACKWARD": -45, "LEFT": -135, "RIGHT": 45,
          "F": 135, "B": -45, "L": -135, "R": 45,
          0: 135, 1: -45, 2: -135, 3: 45}
# F(0)=135
# B(1)=-45
# L(2)=-135
# R(3)=45
# UNKNOWN(-1)=??
###########################################
# STEPPER
out1 = 12
out2 = 6
out3 = 13
out4 = 5
up_steps = -100
down_steps = 100
