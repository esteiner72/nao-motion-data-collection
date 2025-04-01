from naoqi import ALProxy
import time
import json

# Connect to NAO
robot_ip = "127.0.0.1"  # Change this to your NAO's IP
port = 9559
motion_proxy = ALProxy("ALMotion", robot_ip, port)

# List of joints to track
joints = ["HeadYaw", "HeadPitch", "LShoulderPitch", "LShoulderRoll", 
          "LElbowYaw", "LElbowRoll", "LWristYaw", "LHand",
          "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", 
          "RWristYaw", "RHand", "HipRoll", "HipPitch", "KneePitch"]

# Start collecting joint data
data_log = []
start_time = time.time()

while True:
    try:
        timestamp = time.time() - start_time  # Synchronize timestamps
        angles = motion_proxy.getAngles(joints, True)
        data_log.append({"timestamp": timestamp, "angles": angles})
        time.sleep(0.05)  # Collect data at ~20 Hz
    except KeyboardInterrupt:
        break

# Save joint data
with open("joint_data.json", "w") as f:
    json.dump(data_log, f)