import json
from naoqi import ALProxy

ROBOT_IP = "127.0.0.1"
PORT = 9559
JSON_FILE_PATH = "tasks/task_1.json"

joints = [
    "HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", 
    "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", "LHipRoll", 
    "LHipPitch", "LKneePitch", "RShoulderPitch", "RShoulderRoll", 
    "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand", "RHipRoll", 
    "RHipPitch", "RKneePitch"
]

motion = ALProxy("ALMotion", ROBOT_IP, PORT)

with open(JSON_FILE_PATH, "r") as f:
    motion_data = json.load(f)

motion_data.sort(key=lambda x: x["timestamp"])

timestamps = [frame["timestamp"] for frame in motion_data]
angles_per_timestamp = [frame["angles"] for frame in motion_data]
angle_lists = [list(angles) for angles in zip(*angles_per_timestamp)]

time_lists = [timestamps] * len(joints)

motion.angleInterpolation(joints, angle_lists, time_lists, True)