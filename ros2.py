# ros2 launch stretch_core stretch_driver.launch.py
# run this first in hello robot terminal

import hello_helpers.hello_misc as hm
import numpy as np

node = hm.HelloNode.quick_create('node1')

try:
    # Move the arm and gripper back to it’s ‘stow’ position.
    node.stow_the_robot()

    # Extend the telescoping arm all the way out and raise the lift all the way up at the
    # same time.
    node.move_to_pose({'joint_arm': 0.52}, blocking=False)
    node.move_to_pose({'joint_lift': 1.10}, blocking=True)

    # Once lifted, move all three of the wrist motors, one at a time (not all at
    # once). Any rotation amount is fine as long as it is visible. 

    # node.move_to_pose(
    #     {'joint_wrist_yaw': node.joint_state.position[node.joint_state.name.index('joint_wrist_yaw')] + np.radians(30)}, 
    #     blocking=True
    # )
    node.move_to_pose({'joint_wrist_yaw': np.radians(30)}, blocking=True)
    node.move_to_pose({'joint_wrist_roll': np.radians(30)}, blocking=True)
    node.move_to_pose({'joint_wrist_pitch': np.radians(30)}, blocking=True)

    # Then open the gripper and close it. 
    node.move_to_pose({'joint_gripper_finger_left': 100.0}, blocking=True)
    node.move_to_pose({'joint_gripper_finger_left': -100.0}, blocking=True)

    # Then rotate both of the two motors connected to the RealSense (head
    # camera). 
    node.move_to_pose({'joint_head_pan': np.radians(30)}, blocking=True) #TODO: check joint limit
    node.move_to_pose({'joint_head_tilt': np.radians(30)}, blocking=True)

    # Then reset everything back to the ‘stow’ position.
    node.stow_the_robot()

    # Once in stow, drive the robot forward 0.5 meters, rotate 180 degrees, then drive 0.5
    # meters forward (back to the starting position).

    # TODO
    node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)
    node.move_to_pose({'rotate_mobile_base': np.radians(180)}, blocking=True)
    node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)

    # t = node.get_robot_floor_pose_xya(floor_frame='odom')

finally:
    node.stop_the_robot()
    node.get_logger().info()