import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def plot_joint_data(h5_path, joint_name):
    with h5py.File(h5_path, "r") as f:
        joint_names = f.attrs["joint_names"].split(",")
        timestamps = f["timestamps"][:]
        joint_sensor = f["joint_sensor"][:]
        joint_command = f["joint_command"][:]

        if joint_name not in joint_names:
            print "Joint not found:", joint_name
            print "Available joints:", joint_names
            return

        idx = joint_names.index(joint_name)
        sensor_vals = joint_sensor[:, idx]
        command_vals = joint_command[:, idx]

        plt.figure(figsize=(10, 4))
        plt.plot(timestamps, sensor_vals, label="Sensor")
        plt.plot(timestamps, command_vals, label="Command", linestyle='--')
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (radians)")
        plt.title("Joint: {}".format(joint_name))
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python plot_motion_from_h5.py <h5_file_path> <joint_name>"
    else:
        h5_path = sys.argv[1]
        joint = sys.argv[2]
        plot_joint_data(h5_path, joint)