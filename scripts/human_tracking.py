#!/usr/bin/env python
import rospy
from visualization_msgs.msg import *
from geometry_msgs.msg import *
from tf2_msgs.msg import *
from nav_msgs.msg import *
from tf.transformations import *
from move_base_msgs.msg import *
import actionlib
import roslib
import tf
import math

turtlebot_x = 0
turtlebot_y = 0

control = 0
control_print = 0

last_x = 0
last_y = 0
camera_x = 0
camera_y = 0

person_x = 0
person_y = 0
person_w = 0
person_z = 0

turtlebot_orientation_x = 0
turtlebot_orientation_y = 0
turtlebot_orientation_z = 0
turtlebot_orientation_w = 0
angle_turtlebot = 0

def callback_turtlebot(data):
	#Read out the topic tf_turtlebot to get the exact position and orientation of the turtlebot in the map
	global turtlebot_x
	global turtlebot_y
	global turtlebot_orientation_x
	global turtlebot_orientation_y
	global turtlebot_orientation_z
	global turtlebot_orientation_w
	turtlebot_x = data.position.x
	turtlebot_y = data.position.y
	turtlebot_orientation_x = data.orientation.x
	turtlebot_orientation_y = data.orientation.y
	turtlebot_orientation_z = data.orientation.z
	turtlebot_orientation_w = data.orientation.w
	calculate_angle()

def calculate_angle():
	#convert angle of the turtlebot in the map from quaternions to radian
	global angle_turtlebot
	quaternion_turtlebot = (
		turtlebot_orientation_x,
		turtlebot_orientation_y,
		turtlebot_orientation_z,	
		turtlebot_orientation_w)
	euler = euler_from_quaternion(quaternion_turtlebot)
	angle_turtlebot = euler[2]

def send_goal():
	#Sending 2D nav goal
	print "New goal:\nx = %s \ny = %s \nz = %s \nw = %s"%(person_x,person_y,person_z,person_w)
	client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
	client.wait_for_server()
	goal = MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	goal.target_pose.header.stamp = rospy.Time.now()
	goal.target_pose.pose.position.x = person_x
	goal.target_pose.pose.position.y = person_y
	goal.target_pose.pose.orientation.w = person_w
	goal.target_pose.pose.orientation.z = person_z
	client.send_goal(goal)
	print("goal sent")

def calculation():
	global person_x
	global person_y
	global person_z
	global person_w
	
	if camera_x != 0:
		#---calculation position person in camera frame ---------	
		alpha_camera = math.atan(camera_y/camera_x)
		distance_person = math.sqrt((math.pow(camera_x,2)+math.pow(camera_y,2)))
		safe_distance = distance_person - 1
		safe_x = math.cos(alpha_camera) * safe_distance
		safe_y = math.sin(alpha_camera) * safe_distance
		# -------------------------------------------------------

		#---calculation exact position human in turtlebot map ---	
		person_x = turtlebot_x + math.cos(angle_turtlebot)*safe_x - math.sin(angle_turtlebot)*safe_y
		person_y = turtlebot_y + math.sin(angle_turtlebot)*safe_x + math.cos(angle_turtlebot)*safe_y
		yaw_person = angle_turtlebot - alpha_camera
		quaternion = quaternion_from_euler(0, 0, yaw_person)
		person_z = quaternion[2]
		person_w = quaternion[3]
		#--------------------------------------------------------		
	
def callback_camera(data):
	global control
	global control_print
	global last_x
	global last_y
	global camera_x
	global camera_y
	
	camera_x = 0
	camera_y = 0

	if  data.pose.position.x < 5 and data.pose.position.x != 0.0:

		camera_x = data.pose.position.x
		camera_y = data.pose.position.y
		change_x = math.fabs(last_x - camera_x)	
		change_y = math.fabs(last_y - camera_y)	
		control_print = 0
		
		if change_x < 0.1 or change_y < 0.1 or last_x == 0:
			calculation()
			last_x = camera_x
			last_y = camera_y

			distance_togo = math.fabs(turtlebot_x - person_x)
			if distance_togo > 0.2 and control == 0: 
				send_goal()
				control = control + 1
				print("if1")
			if distance_togo < 0.1 and control > 0: 
				send_goal()
				control = 0
				print("if2")
			elif distance_togo > 0.2 and control > 0:
				control = control + 1
				if control > 50:
					control = 0
	
	elif data.pose.position.x == 0.0 and control_print == 0:
		print('Searching for a person')	 
		control_print = 1
					
def tracker():
	rospy.init_node('tracker', anonymous=True)	
	rospy.Subscriber("/tf_turtlebot",Pose, callback_turtlebot)
	rospy.Subscriber("body_tracker/marker",Marker, callback_camera)		
	print('Searching for a person')
	rospy.spin()

if __name__ == '__main__':
	tracker()
	
