import sys
from random import uniform
from naoqi import *

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

    # Random angle in radians between min and max DoF
    yawAngle = uniform(-2.0857,2.0857)
    # Pitch angle limited based on yaw angle
    maxPitchAngle = 0
    minPitchAngle = 0
    if yawAngle <= -1.526988:
        minPitchAngle, maxPitchAngle = -0.449073, 0.330041
    elif yawAngle <= -1.089958:
        minPitchAngle, maxPitchAngle = -0.330041, 0.200015
    elif yawAngle <= -0.903033:
        minPitchAngle, maxPitchAngle = -0.430049, 0.300022
    elif yawAngle <= -0.756077:
        minPitchAngle, maxPitchAngle = -0.479965, 0.330041
    elif yawAngle <= -0.486074:
        minPitchAngle, maxPitchAngle = -0.548033, 0.370010
    elif yawAngle <= 0.000000:
        minPitchAngle, maxPitchAngle = -0.671951, 0.515047
    elif yawAngle <= 0.486074:
        minPitchAngle, maxPitchAngle = -0.671951, 0.422021
    elif yawAngle <= 0.756077:
        minPitchAngle, maxPitchAngle = -0.548033, 0.370010
    elif yawAngle <= 0.903033:
        minPitchAngle, maxPitchAngle = -0.479965, 0.330041
    elif yawAngle <= 1.089958:
        minPitchAngle, maxPitchAngle = -0.430049, 0.300022
    elif yawAngle <= 1.526988:
        minPitchAngle, maxPitchAngle = -0.330041, 0.200015
    elif yawAngle <= 2.086017:
        minPitchAngle, maxPitchAngle = -0.449073, 0.330041
    pitchAngle = uniform(minPitchAngle, maxPitchAngle)

    names      = ["HeadYaw", "HeadPitch"]
    angleLists = [yawAngle, pitchAngle]
    times      = [1.0, 1.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

    postureProxy.goToPosture("Stand", 0.5)

if __name__ == "__main__":
    main(sys.argv[1])