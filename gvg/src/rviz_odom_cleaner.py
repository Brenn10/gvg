#!/usr/bin/python
import rospy as rp
from nav_msgs.msg import Odometry

class Remover():
	def mangle(self,msg):
		empty36tuple=[0]*36
		msg.twist.covariance=empty36tuple
		msg.pose.covariance=empty36tuple
		self.pubber.publish(msg)
	def __init__(self):
		rp.init_node("rviz_cleaned_odom")

		rp.Subscriber("/indoor/gvg/odom_combined",Odometry,self.mangle)

		self.pubber = rp.Publisher("odom_clean_covar",Odometry,queue_size=10)

		rp.spin()
r=Remover()
