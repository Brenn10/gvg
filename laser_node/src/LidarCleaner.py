#!/usr/bin/python

import rospy
import math
from sensor_msgs.msg import LaserScan

class LidarCleaner():
    def laser_call(self,msg):
        checkList=msg.ranges
        L = list(msg.ranges)

        for i in range(10,len(checkList)-20):
            if(L[i]<1.5):
                L[i]=max((u if u < 1.5 else 0) for u in checkList[i-10:i+10])
        msg.ranges=L
        self.pub.publish(msg)

    def __init__(self):
        rospy.init_node("lidar_cleaner")
        rospy.Subscriber("/scan",LaserScan,self.laser_call)
        self.pub = rospy.Publisher("/indoor/base_scan",LaserScan,queue_size=10)
        rospy.spin()

l = LidarCleaner()
