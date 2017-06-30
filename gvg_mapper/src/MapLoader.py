#!/usr/bin/python
import os
import sys
import rospy
from gvg_mapper.msg import GVGNode,GVGEdgeMsg
from gvg_mapper.srv import LoadSavedMap

'''
MapSaver.py

Brennan Cain

Loads a map file from the output of MapSaver to the gvg mapper while running

'''
class MapSaver():
	def check_file(self):
		if os.path.exists(self.map_file) and os.access(self.map_file, os.R_OK):
			return True
		return False
		

	def read_to_lists(self):
		nodes=[]
		edges=[]
		#read map file
		with open(self.map_file,"r") as f:
			while(obj = pickle.load(f)):
				if(type(obj)==type(GVGNode)):
					nodes.append(obj)
				elif(type(obj)==type(GVGEdgeMsg)):
					edges.append(obj)
				else:
					rospy.logwarn("Bad input)
		return nodes,edges

	def __init__(self,path):

		self.map_file=path

		if(self.check_file()):

			rospy.wait_for_service('load_saved_map')

			try:
				load = rospy.ServiceProxy('load_saved_map', LoadSavedMap)
				if(load(nodes,edges).success):
					rospy.logwarn("Successfully loaded map")
				else:
					rospy.logerr("Failed to load map")
			except rospy.ServiceException, e:
				rospy.logerr("Failed to load map, exception thrown.")
		else:
			rospy.logerr("Failed to open file")

if __name__ == "__main__":
	if len(sys.argv) > 1:
		filepath = ' '.join(sys.argv[1:])
		MapLoader(filepath)
	else:
		print("Please specify a file path)
		sys.exit(1)

