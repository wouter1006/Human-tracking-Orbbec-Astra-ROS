#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import *

if __name__ == '__main__':
    rospy.init_node('tf_listener')
    listener = tf.TransformListener()							#define datatype of listener
    pub = rospy.Publisher('tf_turtlebot', Pose,queue_size=1)	#create publisher
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))		#Get data from topic
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
	print(trans[1])
	tf = Pose()					#Set datatype of topic
	tf.position.x = trans[0]	#X position of turtlebot in map
	tf.position.y = trans[1]	#Y position of turtlebot in map
	tf.orientation.z = rot[2]	#Z orientation of turtlebot in map
	tf.orientation.w = rot[3]	#W orientation of turtlebot in map
	pub.publish(tf)				#Publish tf in tf_turtlebot topic
