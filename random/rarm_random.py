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
    # Left arm
    RShoulderPitch = uniform(-2.0857,2.0857)
    RShoulderRoll = uniform(-0.3142,1.3265)
    RElbowYaw = uniform(-2.0857,2.0857)
    RElbowRoll = uniform(-1.5446,-0.0349)
    RWristYaw = uniform(-1.8238,1.8238)
    names      = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
    angleLists = [RShoulderPitch, RShoulderRoll, RElbowYaw, RElbowRoll, RWristYaw]
    times      = [1.0, 1.0, 1.0, 1.0, 1.0]
    isAbsolute = True
    motionProxy.angleInterpolation(names, angleLists, times, isAbsolute)

    postureProxy.goToPosture("Stand", 0.5)

if __name__ == "__main__":
    main(sys.argv[1])