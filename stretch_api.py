import stretch_body.robot
import numpy as np

robot = stretch_body.robot.Robot()
robot.startup()

# Move the arm and gripper back to it’s ‘stow’ position.
robot.stow()

# Extend the telescoping arm all the way out and raise the lift all the way up at the
# same time. 
arm_limit = robot.arm.soft_motion_limits['hard'][-1]
arm_current = robot.arm.status['pos']
lift_limit = robot.lift.soft_motion_limits['hard'][-1]
lift_current = robot.lift.status['pos']

robot.arm.move_to(arm_limit) # 0.517 meters
robot.lift.move_to(lift_limit) # 1.098 meters
robot.push_command()
# robot.arm.wait_until_at_setpoint()
robot.wait_command()

# Once lifted, move all three of the wrist motors, one at a time (not all at
# once). Any rotation amount is fine as long as it is visible. 
robot.end_of_arm.move_to('wrist_yaw', np.radians(30)) #rads
robot.end_of_arm.move_to('wrist_roll', np.radians(30))
robot.end_of_arm.move_to('wrist_pitch', np.radians(30))
robot.wait_command()

# Then open the gripper and close it. 
robot.end_of_arm.move_to('stretch_gripper', 100) #-100~100
robot.wait_command()
robot.end_of_arm.move_to('stretch_gripper', -100) #-100~100
robot.wait_command()

# Then rotate both of the two motors connected to the RealSense (head
# camera). 
robot.head.move_to('head_pan', np.radians(30))
robot.head.move_to('head_tilt', np.radians(30))
robot.wait_command()

# Then reset everything back to the ‘stow’ position.
robot.stow()

# Once in stow, drive the robot forward 0.5 meters, rotate 180 degrees, then drive 0.5
# meters forward (back to the starting position).
robot.base.translate_by(0.5)
robot.push_command()
robot.wait_command()

robot.base.rotate_by(np.radians(180))
robot.push_command()
robot.wait_command()

robot.base.translate_by(0.5)
robot.push_command()
robot.wait_command()

