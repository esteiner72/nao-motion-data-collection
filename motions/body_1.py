import sys
import os
import time
import numpy as np
from naoqi import ALProxy
from save_data import save_trial

TASK_NAME = "body_1"
JOINTS = ["HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll",
          "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand", "LHipRoll",
          "LHipPitch", "LKneePitch",
          "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
          "RWristYaw", "RHand", "RHipRoll", "RHipPitch", "RKneePitch"]
POLL = 0.01

def StiffnessOn(proxy):
    proxy.stiffnessInterpolation("Body", 1.0, 1.0)

def main(robotIP):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception as e:
        print e
        return

    StiffnessOn(motionProxy)
    postureProxy.goToPosture("Stand", 0.5)
    motion = postureProxy.post.goToPosture("StandZero", 0.35)

    timestamps = []
    sensor_data = []
    command_data = []

    start_time = time.time()

    while True:
        t = time.time() - start_time
        if len(timestamps) > 0 and t == 0:
            continue
        timestamps.append(t)
        sensor_angles = motionProxy.getAngles(JOINTS, True)
        command_angles = motionProxy.getAngles(JOINTS, False)
        sensor_data.append(sensor_angles)
        command_data.append(command_angles)
        time.sleep(POLL)
        if not postureProxy.isRunning(motion):
            break

    postureProxy.goToPosture("Stand", 0.5)

    sensor_np = np.array(sensor_data, dtype=np.float32)
    command_np = np.array(command_data, dtype=np.float32)
    timestamps_np = np.array(timestamps, dtype=np.float64)

    sensor_np = np.array(sensor_data, dtype=np.float32)
    command_np = np.array(command_data, dtype=np.float32)
    timestamps_np = np.array(timestamps, dtype=np.float64)

    save_trial(sensor_np, command_np, timestamps_np, TASK_NAME)

if __name__ == "__main__":
    main(sys.argv[1])
