#!/usr/bin/python
import os
import sys
import rospy
import pickle
import argparse
from gvg_mapper.msg import GVGNode,GVGEdgeMsg
from gvg_mapper.srv import LoadSavedMap

'''
MapSaver.py

Brennan Cain

Loads a map file from the output of MapSaver to the gvg mapper while running

'''
class MapLoader():

	## Check that the file is accessible
	#
	# @return Boolean flag if accessible
	def check_file(self):
		if os.path.exists(self.map_file) and os.access(self.map_file, os.R_OK):
			return True
		return False
		
	## Reads the file and gives the stuff
	#
	# @return Gives a tuple of the lists (nodes,edges)
	def read_to_lists(self):
		#read map file
		with open(self.map_file,"r") as f:
			nodes,edges = pickle.load(f)
		return nodes,edges

	## Runs the map loader
	#
	# get path, check if accessible, load, throw into the graph usign prebuilt LoadSavedMap
	def __init__(self,path):
		rospy.init_node("map_loader")

		n_pub = rospy.Publisher("/node",GVGNode,queue_size=100)
		e_pub = rospy.Publisher("/edge",GVGEdge,queue_size=100)
		# Get path
		self.map_file=path

		#Check if file good and available
		if(self.check_file()):

			#Prepare for uppload
			rospy.wait_for_service('/load_saved_map')

			try: 
				# push to service for loading
				load = rospy.ServiceProxy('/load_saved_map', LoadSavedMap)
				nodes,edges = self.read_to_lists()
				print(type(nodes))
				print(type(edges))
				for node in nodes:
					n_pub.publish(node)
				for edge in edges:
					e_pub.publish(edge)
				load(nodes,edges)
			except rospy.ServiceException, e: #Failed
				print("Failed to load map, exception thrown.")
		else: # Failed
			print("Failed to open file")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='')

