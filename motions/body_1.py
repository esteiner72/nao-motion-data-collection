import sys
from naoqi import *
import time
import json
import os

TASK_NAME = "body_1"
JOINTS = ["HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", 
          "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", "LHipRoll", 
          "LHipPitch", "LKneePitch",
          "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", 
          "RWristYaw", "RHand", "RHipRoll", "RHipPitch", "RKneePitch"]
POLL = 0.01

current_dir = os.path.dirname(os.path.abspath(__file__))
temp_data_dir = os.path.normpath(os.path.join(current_dir, "..", 'temp_data'))
sensor_file_path = os.path.join(temp_data_dir, "{}_sensor.json".format(TASK_NAME))
command_file_path = os.path.join(temp_data_dir, "{}_command.json".format(TASK_NAME))

def StiffnessOn(proxy):
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def main(robotIP):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception as e:
        print("Could not create proxy to ALMotion")
        print ("Error was: ", e)

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception as e:
        print("Could not create proxy to ALRobotPosture")
        print ("Error was: ", e)

    StiffnessOn(motionProxy)

    postureProxy.goToPosture("Stand", 0.5)

    motion = postureProxy.post.goToPosture("StandZero", 0.35)

    start_time = time.time()
    sensor_data = []
    command_data = []
    while True:
        timestamp = time.time() - start_time
        # getting sensor angles using True for 'useSensors' param
        # a False 'useSensors' param will record command angles
        sensor_angles = motionProxy.getAngles(JOINTS, True)
        sensor_data.append({"timestamp": timestamp, "angles": sensor_angles})
        command_angles = motionProxy.getAngles(JOINTS, False)
        command_data.append({"timestamp": timestamp, "command": command_angles})
        time.sleep(POLL)
        if not postureProxy.isRunning(motion):
            break

    with open(sensor_file_path, "w") as f:
        # avoid 0 timestamp
        del sensor_data[0]
        json.dump(sensor_data, f)

    with open(command_file_path, "w") as f:
        # avoid 0 timestamp
        del command_data[0]
        json.dump(command_data, f)

    postureProxy.goToPosture("Stand", 0.5)

if __name__ == "__main__":
    main(sys.argv[1])