import os
import h5py
import numpy as np
import csv

def save_trial(joint_sensor, joint_command, timestamps, task_name, root_dir="h5_data"):
    """
    Saves a trial for a given task_name into an HDF5 file in a task-named folder.
    Appends metadata to a shared metadata.csv.
    """
    # Make sure output folder exists
    task_dir = os.path.join(root_dir, task_name)
    if not os.path.exists(task_dir):
        os.makedirs(task_dir)

    # Get next trial number
    trial_num = 1
    while True:
        fname = "%s_trial_%03d.h5" % (task_name, trial_num)
        fpath = os.path.join(task_dir, fname)
        if not os.path.exists(fpath):
            break
        trial_num += 1

    # Save trial to HDF5
    with h5py.File(fpath, "w") as f:
        f.create_dataset("joint_sensor", data=joint_sensor)
        f.create_dataset("joint_command", data=joint_command)
        f.create_dataset("timestamps", data=timestamps)

        f.attrs["task_name"] = task_name
        f.attrs["trial"] = trial_num
        f.attrs["num_joints"] = joint_sensor.shape[1]
        f.attrs["joint_units"] = "radians"
        f.attrs["polling_interval_sec"] = round(timestamps[1] - timestamps[0], 4) if len(timestamps) > 1 else -1
        f.attrs["robot_model"] = "NAO v6"

    # Append metadata
    meta_path = os.path.join(root_dir, "metadata.csv")
    duration = timestamps[-1] - timestamps[0]
    row = [fname, task_name, trial_num, round(duration, 2), len(timestamps)]

    file_exists = os.path.exists(meta_path)
    with open(meta_path, "ab") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["filename", "task", "trial", "duration_sec", "frames"])
        writer.writerow(row)

    print("Saved trial #%d for task '%s' to %s" % (trial_num, task_name, fpath))